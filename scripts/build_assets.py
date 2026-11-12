#!/usr/bin/env python3
"""Genera los SVG retro de ./assets para el README del perfil.

Uso:  python3 scripts/build_assets.py

Todo el texto grande se dibuja como pixeles (rects en un <path>), asi no depende
de fuentes externas (GitHub bloquea fuentes remotas dentro de un SVG). El texto
chico usa solo fuentes monoespaciadas del sistema. Las animaciones son CSS y SMIL
dentro de cada SVG; no hay JS. Solo usa la libreria estandar de Python.
"""
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"

# Paleta CRT (propia)
SCREEN = "#07100b"
GREEN = "#46f28c"
GREEN_DIM = "#2b9d5d"
AMBER = "#ffb43c"
CYAN = "#5ee7ff"
MAGENTA = "#ff6ad5"
INK = "#11161c"

# ------------------------------------------------------------------ pixel font
G = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "¿": ["..#..", ".....", "..#..", ".#...", "#....", "#...#", ".###."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    ".": [".....", ".....", ".....", ".....", ".....", ".....", "..#.."],
    ",": [".....", ".....", ".....", ".....", ".....", "..#..", ".#..."],
    ":": [".....", "..#..", ".....", ".....", ".....", "..#..", "....."],
    "·": [".....", ".....", ".....", "..#..", ".....", ".....", "....."],
    ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
    "-": [".....", ".....", ".....", ".###.", ".....", ".....", "....."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
}
ACCENTS = {"acute": ["...#.", "..#.."], "tilde": [".##.#", "#.##."]}
ACCENTED = {"Á": ("A", "acute"), "É": ("E", "acute"), "Í": ("I", "acute"),
            "Ó": ("O", "acute"), "Ú": ("U", "acute"), "Ñ": ("N", "tilde")}
ADV = 6  # 5 columnas + 1 de aire
SPACE_ADV = 4


def pixel_width(text, p):
    w = 0
    for ch in text:
        w += SPACE_ADV if ch == " " else ADV
    return (w - 1) * p


def pixel_path(text, x, y, p):
    """Devuelve el atributo d de un <path> con el texto en pixeles.
    y es el borde superior de las mayusculas; los acentos suben 3p."""
    d = []
    cx = 0
    for ch in text.upper():
        if ch == " ":
            cx += SPACE_ADV
            continue
        base, acc = ACCENTED.get(ch, (ch, None))
        rows = [(r, row) for r, row in enumerate(G[base])]
        if acc:
            rows += [(-3 + r, row) for r, row in enumerate(ACCENTS[acc])]
        for r, row in rows:
            for c, v in enumerate(row):
                if v == "#":
                    px = x + (cx + c) * p
                    py = y + r * p
                    d.append(f"M{px:g} {py:g}h{p:g}v{p:g}h-{p:g}z")
        cx += ADV
    return "".join(d)


def notched(x, y, w, h, n):
    """Rectangulo con esquinas escalonadas (look pixel)."""
    return (f"M{x+n:g} {y:g}H{x+w-n:g}V{y+n:g}H{x+w:g}V{y+h-n:g}H{x+w-n:g}V{y+h:g}"
            f"H{x+n:g}V{y+h-n:g}H{x:g}V{y+n:g}H{x+n:g}Z")


def mono_text(s, x, y, size, fill, cw=None, weight=None, anchor=None, extra=""):
    """Texto monoespaciado; con cw fija cada glifo en su columna (x por caracter)."""
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor else ""
    if cw:
        xs = " ".join(f"{x + i*cw:g}" for i in range(len(s)))
        return (f'<text x="{xs}" y="{y:g}" font-size="{size}" fill="{fill}"{w}{a} '
                f'font-family="{MONO}"{extra}>{escape(s)}</text>')
    return (f'<text x="{x:g}" y="{y:g}" font-size="{size}" fill="{fill}"{w}{a} '
            f'font-family="{MONO}"{extra}>{escape(s)}</text>')


def svg(w, h, body, title, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">\n'
            f'<title>{escape(title)}</title>\n'
            f'<style>{style}\n@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}</style>\n'
            f'{body}\n</svg>\n')


def write(name, content):
    path = os.path.join(ASSETS, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {name}  {len(content.encode()) / 1024:.1f} KB")


SCANLINES = ('<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse">'
             '<rect width="4" height="2" fill="#000" opacity=".28"/></pattern>')
GLOW = ('<filter id="glow" x="-10%" y="-30%" width="120%" height="160%">'
        '<feGaussianBlur stdDeviation="2.4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

# ------------------------------------------------------------------ header


def header(theme):
    W, H = 720, 500
    if theme == "dark":
        bezel, bezel_hi, bezel_lo, label = "#1c232c", "#2c3542", "#11161c", "#7d8a99"
    else:
        bezel, bezel_hi, bezel_lo, label = "#e7dfca", "#f6f1e3", "#c2b79c", "#6f6650"
    sx, sy, sw, sh = 26, 24, W - 52, 410
    T = 16.0  # ciclo de la animacion (s)
    size, cw, lh = 22, 13.2, 34
    tx = 54
    ty0 = 268

    def kt(t):
        return f"{t / T:.4f}"

    seq = [
        ("> ", "cat foco.txt", 0.5, 0.08),
        (None, "orquesto agentes de IA, no solo prompts", 1.9, None),
        ("> ", "agentes --en-paralelo", 2.7, 0.065),
        (None, "claude · codex · gemini · deepseek · grok", 4.5, None),
        ("> ", 'git commit -m "de punta a punta"', 5.3, 0.05),
    ]
    hide = 15.4
    body = []
    cursor_events = []  # (t, x, y)
    for i, (prompt, txt, t0, dt) in enumerate(seq):
        y = ty0 + i * lh
        if prompt is None:
            # salida: aparece de golpe
            body.append(f'<g opacity="0">{mono_text(txt, tx, y, size, CYAN if i == 3 else GREEN, cw)}'
                        f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
                        f'keyTimes="0;{kt(t0)};{kt(hide)}" values="0;1;0"/></g>')
            continue
        px = tx + len(prompt) * cw
        start = t0 + 0.35
        # prompt
        body.append(f'<g opacity="0">{mono_text(prompt, tx, y, size, AMBER, cw, weight="700")}'
                    f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
                    f'keyTimes="0;{kt(t0)};{kt(hide)}" values="0;1;0"/></g>')
        # comando escrito letra por letra (clip con ancho discreto)
        cid = f"type{i}"
        keys, vals = ["0"], ["0"]
        for k in range(1, len(txt) + 1):
            keys.append(kt(start + k * dt))
            vals.append(f"{k * cw:g}")
        keys.append(kt(hide))
        vals.append("0")
        body.append(f'<clipPath id="{cid}"><rect x="{px:g}" y="{y - size:g}" width="0" height="{size + 10}">'
                    f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
                    f'keyTimes="{";".join(keys)}" values="{";".join(vals)}"/></rect></clipPath>')
        body.append(f'<g clip-path="url(#{cid})">{mono_text(txt, px, y, size, GREEN, cw)}</g>')
        cursor_events.append((t0, px, y))
        for k in range(1, len(txt) + 1):
            cursor_events.append((start + k * dt, px + k * cw, y))
    # cursor: sigue la escritura
    keys = ["0"] + [kt(t) for t, _, _ in cursor_events]
    xs = [f"{cursor_events[0][1]:g}"] + [f"{x:g}" for _, x, _ in cursor_events]
    ys = [f"{cursor_events[0][2] - size + 3:g}"] + [f"{y - size + 3:g}" for _, _, y in cursor_events]
    cursor = (f'<rect class="blink" width="{cw:g}" height="{size + 2}" fill="{GREEN}">'
              f'<animate attributeName="x" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
              f'keyTimes="{";".join(keys)}" values="{";".join(xs)}"/>'
              f'<animate attributeName="y" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
              f'keyTimes="{";".join(keys)}" values="{";".join(ys)}"/></rect>')

    name_p = 8
    name = "JOSUÉ PALMA"
    name_y = 112
    style = (
        ".blink{animation:blink 1.05s steps(1) infinite}"
        "@keyframes blink{50%{opacity:0}}"
        ".flicker{animation:flicker 5s steps(1) infinite}"
        "@keyframes flicker{0%{opacity:1}42%{opacity:.93}43%{opacity:1}77%{opacity:.96}78%{opacity:1}}"
        ".roll{animation:roll 7s linear infinite}"
        "@keyframes roll{from{transform:translateY(-120px)}to{transform:translateY(" + str(sh + 40) + "px)}}"
        ".led{animation:led 2.4s ease-in-out infinite}"
        "@keyframes led{50%{opacity:.35}}"
    )
    vents = "".join(f'<rect x="{W - 230 + i*14}" y="{H - 44}" width="8" height="18" rx="2" fill="{bezel_lo}"/>'
                    for i in range(10))
    out = f"""<defs>{SCANLINES}{GLOW}
<radialGradient id="vig" cx="50%" cy="45%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".55"/></radialGradient>
<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset=".5" stop-color="{GREEN}" stop-opacity=".07"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
<clipPath id="scr"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="22"/></clipPath>
</defs>
<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="30" fill="{bezel}" stroke="{bezel_lo}" stroke-width="3"/>
<rect x="9" y="8" width="{W-18}" height="{H-18}" rx="25" fill="none" stroke="{bezel_hi}" stroke-width="2"/>
<rect x="{sx-6}" y="{sy-6}" width="{sw+12}" height="{sh+12}" rx="26" fill="{bezel_lo}"/>
<g clip-path="url(#scr)">
<g class="flicker">
<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{SCREEN}"/>
<path d="{pixel_path('PRODUCT ENGINEER', tx, 56, 3)}" fill="{AMBER}"/>
<g filter="url(#glow)"><path d="{pixel_path(name, tx, name_y, name_p)}" fill="{GREEN}"/></g>
<path d="{pixel_path('TRUJILLO, PERÚ', tx, 192, 3)}" fill="{GREEN_DIM}"/>
<path d="M{tx} 230h{sw - 2*(tx-sx)}" stroke="{GREEN_DIM}" stroke-width="2" stroke-dasharray="6 6" opacity=".7"/>
{''.join(body)}
{cursor}
</g>
<rect class="roll" x="{sx}" y="{sy}" width="{sw}" height="110" fill="url(#band)"/>
<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#sl)"/>
<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="url(#vig)"/>
</g>
<text x="40" y="{H - 28}" font-size="15" font-weight="700" letter-spacing="3" fill="{label}" font-family="{MONO}">JP-2026</text>
<text x="128" y="{H - 28}" font-size="13" letter-spacing="2" fill="{label}" font-family="{MONO}">CRT · 720 LINEAS</text>
{vents}
<circle class="led" cx="{W - 48}" cy="{H - 35}" r="6" fill="{GREEN}"/>
<circle cx="{W - 48}" cy="{H - 35}" r="9" fill="none" stroke="{bezel_lo}" stroke-width="2"/>"""
    return svg(W, H, out, "Josué Palma — Product Engineer · Trujillo, Perú. Orquesto agentes de IA, no solo prompts.", style)


# ------------------------------------------------------------------ section titles


def section(num, title):
    p = 4
    pad = 22
    arrow_w = pixel_width(">", p)
    num_w = pixel_width(num, p)
    title_w = pixel_width(title, p)
    cur_w = 5 * p
    gap = 3 * p
    W = pad + arrow_w + gap + num_w + gap * 2 + title_w + gap + cur_w + pad
    H = 7 * p + 2 * 18 + 6
    y = 18 + 3 + 2
    x = pad
    parts = [f'<path d="{notched(0, 0, W, H, 6)}" fill="{GREEN_DIM}"/>',
             f'<path d="{notched(3, 3, W - 6, H - 6, 5)}" fill="#0b130e"/>',
             f'<path d="{pixel_path(">", x, y, p)}" fill="{AMBER}"/>']
    x += arrow_w + gap
    parts.append(f'<path d="{pixel_path(num, x, y, p)}" fill="{AMBER}"/>')
    x += num_w + gap * 2
    parts.append(f'<g filter="url(#glow)"><path d="{pixel_path(title, x, y, p)}" fill="{GREEN}"/></g>')
    x += title_w + gap
    parts.append(f'<rect class="blink" x="{x}" y="{y}" width="{cur_w}" height="{7*p}" fill="{GREEN}"/>')
    parts.append(f'<rect x="3" y="3" width="{W-6}" height="{H-6}" fill="url(#sl)" opacity=".6"/>')
    style = ".blink{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
    return svg(W, H, f"<defs>{SCANLINES}{GLOW}</defs>" + "".join(parts), f"{num} · {title.capitalize()}", style)


# ------------------------------------------------------------------ contact


def button(label, face, text_color=INK):
    p = 3
    tw = pixel_width(label, p)
    W, H = tw + 40, 7 * p + 26 + 6
    parts = [f'<path d="{notched(0, 6, W, H - 6, 4)}" fill="{INK}"/>',
             f'<path d="{notched(0, 0, W, H - 6, 4)}" fill="{INK}"/>',
             f'<path d="{notched(3, 3, W - 6, H - 12, 3)}" fill="{face}"/>',
             f'<rect x="6" y="5" width="{W - 12}" height="3" fill="#fff" opacity=".45"/>',
             f'<path d="{pixel_path(label, 20, 13 + 1, p)}" fill="{text_color}"/>']
    return svg(W, H, "".join(parts), label.capitalize())




def badge(label, face, text_color=INK):
    """Insignia chica pixel para el strip de stack."""
    p = 2
    tw = pixel_width(label, p)
    W, H = tw + 22, 7 * p + 16 + 3
    parts = [f'<path d="{notched(0, 3, W, H - 3, 3)}" fill="{INK}"/>',
             f'<path d="{notched(0, 0, W, H - 3, 3)}" fill="{INK}"/>',
             f'<path d="{notched(2, 2, W - 4, H - 7, 2)}" fill="{face}"/>',
             f'<path d="{pixel_path(label, 11, 8, p)}" fill="{text_color}"/>']
    return svg(W, H, "".join(parts), label.title())


STACK = [
    ("lang", "LENGUAJES", [("typescript", "TYPESCRIPT"), ("javascript", "JAVASCRIPT"), ("python", "PYTHON")], AMBER),
    ("stack", "STACK", [("react", "REACT"), ("nextjs", "NEXT.JS"), ("react-native", "REACT NATIVE"),
                        ("expo", "EXPO"), ("nodejs", "NODE.JS"), ("nestjs", "NESTJS"),
                        ("tailwind", "TAILWIND"), ("postgresql", "POSTGRESQL"), ("supabase", "SUPABASE")], CYAN),
    ("ai", "AGENTES", [("claude", "CLAUDE"), ("codex", "CODEX"), ("gemini", "GEMINI"),
                       ("deepseek", "DEEPSEEK"), ("grok-bot", "GROK BOT")], GREEN),
]


def main():
    os.makedirs(os.path.join(ASSETS, "badges"), exist_ok=True)
    write("header-dark.svg", header("dark"))
    write("header-light.svg", header("light"))
    for slug, num, title in [("actividad", "01", "ACTIVIDAD"), ("contribuciones", "02", "CONTRIBUCIONES"),
                             ("reciente", "03", "RECIENTE"), ("stack", "04", "STACK")]:
        write(f"sec-{slug}.svg", section(num, title))
    write("btn-portafolio.svg", button("PORTAFOLIO", AMBER))
    write("btn-x.svg", button("X @JOSUEPALVH", "#e9e6dc"))
    for group, label, items, face in STACK:
        write(f"badges/{group}.svg", badge(label + " >", "#0b130e", face))
        for slug, text in items:
            write(f"badges/{slug}.svg", badge(text, face))


if __name__ == "__main__":
    main()
