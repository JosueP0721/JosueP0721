#!/usr/bin/env python3
"""Reescribe el bloque <!--ACTIVIDAD:START--> ... <!--ACTIVIDAD:END--> del README.

Solo lee /users/<user>/events/public: GitHub no devuelve ahi nada de repos
privados. Ademas se descarta todo evento con public=false y todo repo cuyo dueno
este en EXCLUDE_OWNERS. Uso: python3 .github/scripts/actividad.py README.md
"""
import json
import os
import sys
import urllib.request
from datetime import datetime

START, END = "<!--ACTIVIDAD:START-->", "<!--ACTIVIDAD:END-->"
MAX_LINES = 5
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
FALLBACK = "<sub>Sin actividad pública reciente: casi todo mi código vive en repos privados.</sub>"


def fetch(user, token):
    req = urllib.request.Request(
        f"https://api.github.com/users/{user}/events/public?per_page=100",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "actividad-readme"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def describe(ev):
    repo = ev["repo"]["name"]
    url = f"https://github.com/{repo}"
    link = f"[{repo}]({url})"
    p = ev.get("payload") or {}
    t = ev["type"]
    if t == "PushEvent":
        return f"push a {link}", ("push", repo)
    if t == "PullRequestEvent":
        pr = p.get("pull_request") or {}
        n = pr.get("number") or p.get("number")
        ref = f"[#{n}]({url}/pull/{n})" if n else "un PR"
        action = p.get("action")
        if action == "opened":
            return f"abrió el PR {ref} en {link}", None
        if action == "closed" and pr.get("merged"):
            return f"mergeó el PR {ref} en {link}", None
        return None, None
    if t == "PullRequestReviewEvent":
        n = (p.get("pull_request") or {}).get("number")
        return (f"revisó el PR [#{n}]({url}/pull/{n}) en {link}" if n else None), None
    if t == "IssuesEvent" and p.get("action") == "opened":
        n = (p.get("issue") or {}).get("number")
        return (f"abrió el issue [#{n}]({url}/issues/{n}) en {link}" if n else None), None
    if t == "CreateEvent" and p.get("ref_type") == "repository":
        return f"creó {link}", None
    if t == "ReleaseEvent" and p.get("action") == "published":
        tag = (p.get("release") or {}).get("tag_name", "")
        return f"publicó {tag} en {link}".replace("publicó  en", "publicó un release en"), None
    return None, None


def build(events, exclude):
    lines, seen = [], set()
    for ev in events:
        if ev.get("public") is not True:
            continue
        owner = ev["repo"]["name"].split("/")[0].lower()
        if owner in exclude:
            continue
        text, key = describe(ev)
        if not text:
            continue
        d = datetime.strptime(ev["created_at"][:10], "%Y-%m-%d")
        if key:  # una sola linea de push por repo y dia
            key = key + (d.date(),)
            if key in seen:
                continue
            seen.add(key)
        lines.append(f"- `{d.day:02d} {MESES[d.month - 1]}` ▸ {text}")
        if len(lines) == MAX_LINES:
            break
    return "\n".join(lines) if lines else FALLBACK


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    user = os.environ.get("GH_USER", "JosueP0721")
    exclude = {o.strip().lower() for o in os.environ.get("EXCLUDE_OWNERS", "").split(",") if o.strip()}
    block = build(fetch(user, os.environ.get("GITHUB_TOKEN")), exclude)
    with open(path, encoding="utf-8") as f:
        readme = f.read()
    a, b = readme.index(START) + len(START), readme.index(END)
    new = readme[:a] + "\n" + block + "\n" + readme[b:]
    if "--dry-run" in sys.argv:
        print(block)
        return
    if new != readme:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)


if __name__ == "__main__":
    main()
