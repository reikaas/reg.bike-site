# reg.bike – landing page

Static "coming soon" page for **https://reg.bike**, the Norwegian bike registry. Served by GitHub Pages from the root of `main`.

- Pure HTML/CSS. No JavaScript, no cookies, no trackers, no third-party requests (fonts and images are self-hosted; a strict CSP is set via `<meta>`).
- Norwegian (bokmål) at `/`, English at `/en/`. `404.html` also catches scanned sticker URLs like `/id/K7M3-9QX2-C` until the app launches.
- Brand: direction B "Hjullås", navy `#0E2442`, safety orange `#FF6600` (orange buttons use navy text), IBM Plex (SIL OFL 1.1, see `fonts/OFL.txt`).

## Editing

Page copy lives in `src/build.py` (one template, two languages). After editing:

```sh
python3 src/build.py                      # regenerates index.html, en/index.html, 404.html
python src/og.py                          # (Playwright) regenerates og-image.png / og-image-en.png
python src/serve404.py 8765 & python src/shoot.py   # local preview + screenshots
```

## DNS (Porkbun) for GitHub Pages

| Type | Host | Answer |
|---|---|---|
| A | `reg.bike` (blank/@) | 185.199.108.153 |
| A | `reg.bike` | 185.199.109.153 |
| A | `reg.bike` | 185.199.110.153 |
| A | `reg.bike` | 185.199.111.153 |
| AAAA | `reg.bike` | 2606:50c0:8000::153 |
| AAAA | `reg.bike` | 2606:50c0:8001::153 |
| AAAA | `reg.bike` | 2606:50c0:8002::153 |
| AAAA | `reg.bike` | 2606:50c0:8003::153 |
| CNAME | `www` | reikaas.github.io |

Remove Porkbun's default parking records (ALIAS/CNAME to `pixie.porkbun.com`, wildcard `*`) first. Then tick **Enforce HTTPS** in Settings → Pages once the certificate is issued.

When the Go app goes live on its own server, point the apex/www records at that server instead and serve this page (or the app's own home page) from there.
