# bygoodnesstravels.com

Static website for **ByGoodness Travels** — Explore · Connect · Grow.

- `src/build.py` — page content and templates (edit text here), generates `docs/`
- `docs/` — the published site (GitHub Pages serves this folder)
- `docs/assets/site.css`, `docs/assets/site.js` — styles and scripts
- `docs/email/signature.html` — staff email signature (hosted so images load for recipients)

## Edit and publish

```bash
python3 src/build.py      # regenerate pages after editing src/build.py
git add -A && git commit -m "Update site" && git push
```

GitHub Pages redeploys automatically within a minute or two.
