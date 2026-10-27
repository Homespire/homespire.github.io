"""Build the tour deck from the live-demo deck.

Usage (from the repo root):
    python3 _build/make_tour.py

Takes the chosen slides from join-homespire-live-demo-v2/index.html, removes
thumbnails and "click to enlarge" notes, adds a closing cover slide with a
non-clickable "Are you in?" button, puts testimonial buttons on the right,
points images at the live demo's folder, and writes join-homespire-tour-v2/index.html.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "join-homespire-live-demo-v2" / "index.html"
OUT = ROOT / "join-homespire-tour-v2" / "index.html"

# Slide numbers from the 30-slide live demo, in tour order
PICK = [1, 2, 3, 5, 6, 7, 9, 10, 13, 14, 17, 20, 21, 26, 27, 28, 29]

LIVE_URL = "https://homespire.github.io/join-homespire-live-demo-v2/"
TOUR_URL = "https://homespire.github.io/join-homespire-tour-v2/"
TOUR_TITLE = "Join Homespire: A Tour for Loan Officers"
TOUR_DESC = ("A quick tour of the technology, marketing, support and products "
             "behind Homespire Mortgage loan officers.")
TOUR_IMAGE = "https://homespire.github.io/join-homespire-live-demo-v2/images/v2/og-tour.jpg"

html = SRC.read_text(encoding="utf-8")
secs = list(re.finditer(r'(?:    <!-- SLIDE[^\n]*-->\n)?    <section class="slide.*?</section>\n', html, re.S))
assert len(secs) == 30, f"expected 30 slides, found {len(secs)}"
start, end = secs[0].start(), secs[-1].end()


def tidy(block):
    block = re.sub(r'\n\s*<div class="thumbs">.*?</div>', '', block, flags=re.S)
    block = re.sub(r' data-nav-(chapter|title)="[^"]*"', '', block)
    for a, b in (("Click any screen to enlarge. For illustrative purposes only.", "For illustrative purposes only."),
                 ("Click any screen to enlarge. Illustrative data.", "Illustrative data."),
                 ("Click to enlarge. For illustrative purposes only.", "For illustrative purposes only.")):
        block = block.replace(a, b)
    return block


chosen = [tidy(secs[i - 1].group(0)) for i in PICK]

# Closing slide: the cover again, with a non-clickable "Are you in?" button
cover = tidy(secs[0].group(0))
btn = re.search(r'<div onclick="nextSlide\(\)" style="([^"]*)"[^>]*>\s*Are you ready\?\s*</div>', cover, re.S)
assert btn, "cover button not found"
style = btn.group(1).replace("cursor: pointer;", "cursor: default;")
cover = cover.replace(btn.group(0), f'<div style="{style}">\n                        Are you in?\n                    </div>')
chosen.append(cover)

body = []
for i, block in enumerate(chosen, 1):
    block = re.sub(r'<!-- SLIDE \d+:', f'<!-- SLIDE {i}:', block, count=1)
    block = re.sub(r'(<section class="slide[^"]*") data-slide="\d+"', rf'\1 data-slide="{i}"', block, count=1)
    body.append(block)

html = html[:start] + "".join(body) + html[end:]

# Testimonial buttons sit on the right in the tour
html = html.replace('<body>', '<body data-testi-side="right">', 1)

# Share the live demo's images instead of keeping a second copy
html = html.replace('src="images/', 'src="../join-homespire-live-demo-v2/images/')
html = html.replace("img: 'images/", "img: '../join-homespire-live-demo-v2/images/")

# Link-preview tags point at the tour
html = (html.replace(LIVE_URL, TOUR_URL)
            .replace("og-live-demo.jpg", "og-tour.jpg")
            .replace(TOUR_URL + "images/", LIVE_URL + "images/"))
html = re.sub(r'(<meta property="og:title" content=")[^"]*', rf'\1{TOUR_TITLE}', html)
html = re.sub(r'(<meta name="twitter:title" content=")[^"]*', rf'\1{TOUR_TITLE}', html)
html = re.sub(r'(<meta (?:property="og:|name="twitter:)?description" content=")[^"]*', rf'\1{TOUR_DESC}', html)
html = re.sub(r'(<meta name="description" content=")[^"]*', rf'\1{TOUR_DESC}', html)
html = re.sub(r'<title>[^<]*</title>', f'<title>{TOUR_TITLE}</title>', html, count=1)

OUT.write_text(html, encoding="utf-8")
thumbs = html.count('<div class="thumbs">')
print(f"tour slides: {len(chosen)} | thumbs left: {thumbs} | nav attrs: {html.count('data-nav-title=')}")
