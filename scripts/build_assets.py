"""Generate the profile README artwork (light + dark variants).

Run:  python scripts/build_assets.py
Writes assets/album/*.svg. Edit TRACKS / CREDITS below, then re-run.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "album"

# GitHub-like neutrals + one record-label accent, used sparingly.
THEMES = {
    "dark": dict(ink="#E6EDF3", soft="#B1BAC4", muted="#7D8590", rule="#30363D",
                 disc="#0B0D10", groove="#1F242B", sheen="#3A414B",
                 accent="#F0766B", label_ink="#0D1117"),
    "light": dict(ink="#1F2328", soft="#424A53", muted="#6E7781", rule="#D0D7DE",
                  disc="#16181C", groove="#2A2F36", sheen="#5A626D",
                  accent="#D4493F", label_ink="#FFFFFF"),
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif"

TRACKS = [  # (title, one line, tags, action)
    ("Debug Dungeon", "Three code puzzles, patch shards, and a real final boss.",
     "JAVASCRIPT · BROWSER GAME", "PLAY"),
    ("Clutch Lab", "A CS2 match journal that finds duel patterns and one thing to practise.",
     "WEB APP · PUBLIC SOURCE", "PLAY"),
    ("FoodSnap & Body", "Photo meal journal with nutrition estimates and weight trends.",
     "PERSONAL APP · IN PROGRESS", "SOURCE"),
    ("Intelligent Workflow", "C++ and MySQL task manager: roles, assignments, status, reports.",
     "C++ · MYSQL · ACADEMIC", "SOURCE"),
]

CREDITS = [
    ("CODE", "C++  ·  Python  ·  JavaScript  ·  HTML  ·  CSS"),
    ("DATA", "SQL  ·  MySQL  ·  Google Sheets"),
    ("AUTOMATION", "UiPath  ·  n8n  ·  Pabbly Connect"),
    ("SYSTEMS", "ROS Noetic  ·  Gazebo  ·  Linux  ·  VMware"),
    ("DESIGN & ANALYSIS", "UI/UX  ·  Systems Analysis  ·  Documentation  ·  Testing"),
    ("WORKSPACE & GIS", "Obsidian  ·  Google Calendar  ·  Git/GitHub  ·  QGIS  ·  ArcGIS"),
]

REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def svg(w, h, title, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" fill="none" role="img" aria-label="{escape(title)}">\n'
            f'<title>{escape(title)}</title>\n<style>{style}{REDUCED}</style>\n{body}\n</svg>\n')


def t(x, y, s, size, fill, font=MONO, anchor="start", ls=0, weight=400, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<text{c} x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}" '
            f'fill="{fill}">{escape(s)}</text>')


def eq_bars(x, y, c, n=4, h=14, w=3, gap=3, dur=(2.2, 2.8, 1.9, 2.5)):
    """Equalizer bars: the universal 'this is playing' signal."""
    out = []
    for i in range(n):
        bx = x + i * (w + gap)
        out.append(f'<rect class="eq" style="animation-duration:{dur[i % len(dur)]}s;'
                   f'animation-delay:-{i * 0.23:.2f}s" x="{bx}" y="{y - h}" width="{w}" '
                   f'height="{h}" fill="{c}"/>')
    return "".join(out)


EQ_CSS = (".eq{transform-box:fill-box;transform-origin:bottom;animation:eq 2s ease-in-out infinite alternate}"
          "@keyframes eq{0%{transform:scaleY(.4)}100%{transform:scaleY(1)}}")


SONG_SECONDS = 210  # 3:30, the length of one loop of the timeline


def digit_column(x, y, fill, values, size=11, lh=16):
    """One odometer digit: a column of 0-9 that jumps (step-end) to the value for each second."""
    loop = len(values)
    frames, last = [], None
    for sec, v in enumerate(values):
        if v != last:
            frames.append(f"{sec / loop * 100:.4f}%{{transform:translateY({-v * lh}px)}}")
            last = v
    frames.append(f"100%{{transform:translateY({-values[-1] * lh}px)}}")
    name = f"d{x}"
    digits = "".join(t(x, y + d * lh, str(d), size, fill) for d in range(10))
    css = (f".{name}{{animation:{name} {loop}s step-end infinite}}"
           f"@keyframes {name}{{{''.join(frames)}}}")
    return f'<g clip-path="url(#clip{x})"><g class="{name}">{digits}</g></g>', \
        f'<clipPath id="clip{x}"><rect x="{x - 1}" y="{y - size}" width="10" height="{size + 4}"/></clipPath>', css


def timeline(p, y=318, w=600):
    secs = range(SONG_SECONDS)
    cols = [(0, [s // 60 for s in secs]), (14, [(s % 60) // 10 for s in secs]), (21, [s % 10 for s in secs])]
    parts, clips, css = [], [], []
    for x, vals in cols:
        g, c, k = digit_column(x, y + 26, p["soft"], vals)
        parts.append(g); clips.append(c); css.append(k)
    m, ss = divmod(SONG_SECONDS, 60)
    svgp = [
        f'<defs>{"".join(clips)}</defs>',
        f'<path d="M0 {y}H{w}" stroke="{p["rule"]}" stroke-width="3" stroke-linecap="round"/>',
        f'<path class="seek" d="M0 {y}H{w}" stroke="{p["ink"]}" stroke-width="3" stroke-linecap="round"/>',
        f'<circle class="knob" cx="0" cy="{y}" r="6" fill="{p["ink"]}"/>',
        *parts, t(7, y + 26, ":", 11, p["soft"]),
        t(w, y + 26, f"{m}:{ss:02d}", 11, p["muted"], anchor="end"),
    ]
    css.append(f".seek{{stroke-dasharray:{w};stroke-dashoffset:{w};animation:seek {SONG_SECONDS}s linear infinite}}"
               f"@keyframes seek{{to{{stroke-dashoffset:0}}}}"
               f".knob{{animation:knob {SONG_SECONDS}s linear infinite}}"
               f"@keyframes knob{{to{{transform:translateX({w}px)}}}}")
    return "".join(svgp), "".join(css)


def hero(p):
    cx, cy, r = 800, 178, 118
    grooves = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{rr}" stroke="{p["groove"]}" stroke-width="1"/>'
        for rr in range(48, r - 4, 7))
    disc = (
        f'<g class="spin">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{p["disc"]}" stroke="{p["rule"]}"/>'
        f'{grooves}'
        # light catching the grooves: makes the rotation readable
        f'<path d="M{cx + 30} {cy - 92} A96 96 0 0 1 {cx + 92} {cy - 28}" stroke="{p["sheen"]}" stroke-width="2" stroke-linecap="round"/>'
        f'<path d="M{cx - 30} {cy + 92} A96 96 0 0 1 {cx - 92} {cy + 28}" stroke="{p["sheen"]}" stroke-width="2" stroke-linecap="round" opacity=".6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="40" fill="{p["accent"]}"/>'
        + t(cx, cy - 12, "ASSUMIE", 8, p["label_ink"], anchor="middle", ls=2.4, weight=700)
        + t(cx, cy + 20, "SIDE A · 33⅓", 6.5, p["label_ink"], anchor="middle", ls=1.4)
        + f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{p["disc"]}"/></g>')
    # tonearm resting on the outer grooves
    arm = (f'<g stroke="{p["muted"]}" stroke-linecap="round">'
           f'<circle cx="958" cy="52" r="11" fill="none" stroke-width="1.5"/>'
           f'<circle cx="958" cy="52" r="3" fill="{p["muted"]}" stroke="none"/>'
           f'<path d="M958 52 L930 196 L896 236" stroke-width="3"/>'
           f'<rect x="884" y="230" width="16" height="10" rx="2" transform="rotate(38 892 235)" '
           f'fill="{p["muted"]}" stroke="none"/></g>')
    tl, tl_css = timeline(p)
    body = [
        t(0, 22, "ASSUMIE  —  SIDE A", 11, p["muted"], ls=3),
        t(600, 22, "SOFTWARE · PROJECTS · SINGING", 10, p["muted"], anchor="end", ls=2.2),
        f'<path d="M0 40H600" stroke="{p["rule"]}"/>',
        t(-3, 118, "Esther Lee", 54, p["ink"], font=SANS, weight=600, ls=-1.6),
        t(-3, 178, "Qian Hui", 54, p["ink"], font=SANS, weight=600, ls=-1.6),
        t(0, 214, "Software development student · UTeM · Melaka, Malaysia", 15, p["soft"], font=SANS),
        # now playing line
        eq_bars(0, 278, p["accent"]),
        t(32, 277, "NOW PLAYING", 11, p["accent"], ls=2.4, weight=700),
        t(150, 277, "small, useful things — one side project at a time", 14, p["soft"], font=SANS),
        tl,
        disc, arm,
    ]
    style = (".spin{transform-box:fill-box;transform-origin:center;animation:spin 20s linear infinite}"
             "@keyframes spin{to{transform:rotate(360deg)}}" + tl_css + EQ_CSS)
    return svg(1000, 350, "Esther Lee Qian Hui, software development student at UTeM. "
               "A vinyl record spins next to a now-playing line.",
               f'<g transform="translate(4 0)">{"".join(body)}</g>', style)


def section_head(p, left, right):
    body = (t(0, 22, left, 11, p["muted"], ls=3) + t(1000, 22, right, 11, p["muted"], anchor="end", ls=3)
            + f'<path d="M0 40H1000" stroke="{p["rule"]}"/>')
    return svg(1000, 42, f"{left.title()}", body)


def track(p, i, title, line, tags, action):
    num = (eq_bars(2, 44, p["accent"], h=16) if i == 0
           else t(0, 43, f"{i + 1:02d}", 14, p["muted"], ls=1))
    arrow = "▶  PLAY" if action == "PLAY" else "↗  SOURCE"
    body = (num
            + t(64, 36, title, 21, p["ink"], font=SANS, weight=600, ls=-0.2)
            + t(64, 60, line, 14, p["soft"], font=SANS)
            + t(1000, 36, arrow, 11, p["accent"] if action == "PLAY" else p["ink"], anchor="end", ls=2, weight=700)
            + t(1000, 60, tags, 10, p["muted"], anchor="end", ls=1.8)
            + f'<path d="M0 83H1000" stroke="{p["rule"]}"/>')
    return svg(1000, 84, f"Track {i + 1}: {title}. {line} {tags.title()}. Click to {action.lower()}.",
               body, EQ_CSS if i == 0 else "")


def credits(p):
    rows = []
    for i, (k, v) in enumerate(CREDITS):
        y = 34 + i * 40
        rows.append(t(0, y, k, 10, p["muted"], ls=2))
        rows.append(t(230, y, v, 15, p["ink"], font=SANS))
        if i < len(CREDITS) - 1:
            rows.append(f'<path d="M0 {y + 15}H1000" stroke="{p["rule"]}" opacity=".6"/>')
    return svg(1000, 250, "Instruments and tools: " + "; ".join(f"{k}: {v.replace('  ·  ', ', ')}"
                                                                   for k, v in CREDITS), "".join(rows))


def outro(p):
    # a still waveform: the record has stopped
    import math
    bars = []
    for i in range(72):
        h = 3 + 22 * abs(math.sin(i * 0.37) * math.sin(i * 0.11 + 1))
        bars.append(f'<rect x="{214 + i * 8}" y="{40 - h / 2:.1f}" width="3" height="{h:.1f}" '
                    f'rx="1.5" fill="{p["rule"]}"/>')
    body = ("".join(bars)
            + t(500, 92, "THANKS FOR LISTENING", 11, p["muted"], anchor="middle", ls=3.4))
    return svg(1000, 100, "Thanks for listening.", body)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, p in THEMES.items():
        files = {
            "hero": hero(p),
            "head-tracklist": section_head(p, "TRACKLIST", f"{len(TRACKS):02d} TRACKS · STILL RECORDING"),
            "head-liner": section_head(p, "LINER NOTES", "INSTRUMENTS & TOOLS"),
            "liner": credits(p),
            "outro": outro(p),
        }
        for i, tr in enumerate(TRACKS):
            files[f"track-{i + 1:02d}"] = track(p, i, *tr)
        for stem, content in files.items():
            (OUT / f"{stem}-{name}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
