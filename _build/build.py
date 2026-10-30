#!/usr/bin/env python3
"""Builds portfolio v3 from the fragments in _build/src.

Fragments start with a header comment (title, description, image). Case fragments
use two shorthands that this script expands:

    <chapter id="problem" title="The problem" sub="Optional one-line summary"> ... </chapter>

The site header, breadcrumb, "next project" block and footer are added here.
Run: python3 _build/build.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_build" / "src"
MARK = (ROOT / "_build" / "mark.svg").read_text(encoding="utf-8")
BASE_URL = "https://oliveiraanibal.github.io/2027-portfolio/"
EMAIL = "oliveira.anibal@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/oliveiraanibal/"
NAME = "Aníbal Oliveira"
ROLE = "Senior UX Product Designer"

# Reading order for "next project": the four featured cases, the concept, then project notes.
ORDER = [
    ("case-study-feedzai", "Feedzai RiskOps Studio"),
    ("case-study-kb", "KB RetroTool"),
    ("case-study-shell", "Shell Mobility offers"),
    ("case-study-lichtmonitor", "lichtMONITOR"),
    ("case-study-maya", "Maya, L5 Trip Concierge"),
    ("case-study-sancus", "Sancus AI"),
    ("case-study-tds", "Tridonic Design System"),
    ("case-study-continente", "Continente Online"),
    ("case-study-weblicious", "WebLicious"),
]

GTAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-BQ8R2S5PRK"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-BQ8R2S5PRK');</script>"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:ital,wght@0,300..700;1,400&amp;display=swap" rel="stylesheet">')


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text.strip()


def expand(body):
    def chap(m):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        sub = f'<span class="sub">{attrs["sub"]}</span>' if attrs.get("sub") else ""
        return (f'<section class="chapter" id="{attrs["id"]}"><div class="grid">'
                f'<div class="side"><h2>{attrs["title"]}{sub}</h2></div>'
                f'<div class="main">{m.group(2)}</div></div></section>')
    body = re.sub(r"<chapter\s+([^>]*)>(.*?)</chapter>", chap, body, flags=re.S)
    return body.replace("{{EMAIL}}", EMAIL).replace("{{LINKEDIN}}", LINKEDIN)


def head(meta, slug):
    title = meta["title"]
    full = title if title.startswith(NAME) else f"{title} | {NAME}"
    e = html.escape
    url = BASE_URL + ("" if slug == "index" else slug + ".html")
    img = BASE_URL + meta.get("image", "imgs/og.jpg")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{GTAG}
<script>{THEME_INIT}</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(meta.get('description', ''))}">
<meta name="author" content="{NAME}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(meta.get('description', ''))}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
<link rel="stylesheet" href="v3.css">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
</head>
"""


THEME_INIT = "try{var t=localStorage.getItem('theme');if(!t&&matchMedia('(prefers-color-scheme: dark)').matches)t='dark';if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}"
TOGGLE = ('<button class="theme-toggle" type="button" aria-label="Switch to dark theme" title="Switch theme">'
  '<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>'
  '<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>')


def top(current):
    def cur(n):
        return ' aria-current="page"' if n == current else ""
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
  <a class="brand" href="index.html">{MARK}<span class="nm">{NAME}</span></a>
  <div class="tools">
  <nav class="nav" aria-label="Main">
    <a href="index.html#work"{cur('work')}>Work</a>
    <a href="about.html"{cur('about')}>About</a>
    <a href="index.html#contact">Contact</a>
  </nav>
  {TOGGLE}
  </div>
</div></header>
"""


def foot():
    return f"""<footer class="foot"><div class="wrap">
  <span>{NAME}, {ROLE}. Porto, working remotely.</span>
  <nav aria-label="Contact"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></nav>
</div></footer>
<script src="v3.js" defer></script>
</body>
</html>
"""


def case_page(slug, meta, body):
    slugs = [s for s, _ in ORDER]
    i = slugs.index(slug)
    nxt = ORDER[(i + 1) % len(ORDER)]
    kind = meta.get("kind", "Case study")
    end = f"""
<div class="wrap"><section class="next">
  <a href="{nxt[0]}.html"><span class="label">Next project</span><strong>{nxt[1]}</strong></a>
  <p class="also">Want the longer version? <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</section></div>"""
    return (head(meta, slug) + top("work") + f"""<main id="main">
<div class="wrap">
  <p class="crumb"><a href="index.html#work">Work</a> / {html.escape(kind)}</p>
{body}
</div>
{end}
</main>
""" + foot())


def main():
    for path in sorted(SRC.glob("*.html")):
        slug = path.stem
        meta, body = parse(path)
        body = expand(body)
        if slug.startswith("case-study-"):
            out = case_page(slug, meta, body)
        else:
            out = head(meta, slug) + top("work" if slug == "index" else "about") + f'<main id="main">\n{body}\n</main>\n' + foot()
        (ROOT / f"{slug}.html").write_text(out, encoding="utf-8")
        print("built", slug)


if __name__ == "__main__":
    main()
