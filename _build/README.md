# Build notes for the Join Homespire decks

These files are not published (GitHub Pages skips folders that start with `_`).

- `join-homespire-live-demo-v2/index.html` is the source of truth. Edit it directly.
- `make_tour.py` rebuilds the tour from it. Run from the repo root after any live-demo change:

      python3 _build/make_tour.py

- `section-menu.css` / `section-menu.js`: the slide-out section menu (already inlined in the live demo).
- `og-card.html`: the 1200x630 link-preview card. Re-render with headless Chrome:

      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
        --allow-file-access-from-files --virtual-time-budget=4000 --window-size=1200,630 \
        --screenshot=og-live.png "file://$PWD/_build/og-card.html?v=live"

  Use `?v=tour` for the tour card, then save as JPG to
  `join-homespire-live-demo-v2/images/v2/og-live-demo.jpg` / `og-tour.jpg`.
