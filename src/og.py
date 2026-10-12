"""Renders og-image.png (nb) and og-image-en.png (1200x630) with Playwright + system Chrome.
Run from repo root: /workspace/.pwvenv/bin/python src/og.py"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent.parent
TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:P;font-weight:700;src:url(fonts/IBMPlexSans-Bold.woff2)}
@font-face{font-family:P;font-weight:600;src:url(fonts/IBMPlexSans-SemiBold.woff2)}
@font-face{font-family:C;font-weight:700;src:url(fonts/IBMPlexSansCondensed-Bold.woff2)}
@font-face{font-family:M;font-weight:700;src:url(fonts/IBMPlexMono-Bold.woff2)}
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#0E2442;color:#fff;font-family:P,sans-serif;position:relative}
body{background:url(img/guilloche.svg) repeat-x 0 470px/240px 120px,radial-gradient(120% 140% at 80% 25%,#25406B 0,#0E2442 55%,#0A1B33 100%)}
.s1,.s2{position:absolute;top:-60px;height:760px;background:#FF6600;transform:skewX(-18deg)}.s1{left:752px;width:40px}.s2{left:724px;width:10px}
.l{position:absolute;left:72px;top:48px;width:640px}
.logo{height:64px;display:block}
.soon{display:inline-flex;align-items:center;gap:10px;margin-top:30px;padding:7px 18px 7px 14px;border:2px solid rgba(255,255,255,.35);border-radius:999px;font-weight:600;font-size:20px;letter-spacing:.08em;text-transform:uppercase}
.soon::before{content:"";width:12px;height:12px;border-radius:50%;background:#FF6600;box-shadow:0 0 0 4px rgba(255,102,0,.25)}
h1{font-family:C,P,sans-serif;text-transform:uppercase;font-size:56px;line-height:.98;margin:22px 0 16px}
h1 span{color:#FF6600}
p{font-size:24px;line-height:1.35;color:#D4DAE2;margin:0}
.url{position:absolute;left:84px;bottom:58px;font-family:M;font-size:26px;color:#fff}
.url b{color:#FF6600}
.bar{position:absolute;left:0;right:0;bottom:0;height:10px;background:#FF6600}
.tube{position:absolute;left:830px;top:-40px;width:250px;height:720px;border-radius:40px;background:linear-gradient(90deg,#0a1626 0%,#1f2f45 18%,#3b4d66 34%,#56677f 45%,#33465f 62%,#16243a 84%,#0a1626 100%)}
.st{position:absolute;left:878px;top:95px;width:154px;filter:drop-shadow(0 12px 20px rgba(0,0,0,.4))}
</style></head><body>
<div class="l"><img class="logo" src="img/lockup-reverse.svg">
<div class="soon">{soon}</div>
<h1>{h1}</h1><p>{p}</p></div>
<div class="url">https://reg<b>.</b>bike</div>
<div class="s2"></div><div class="s1"></div><div class="tube"></div><img class="st" src="img/sticker-portrait-30x60-color@2x.png">
<div class="bar"></div></body></html>"""
VARIANTS = {
  "og-image.png": dict(soon="Kommer snart", h1="Registrer sykkelen din.<br><span>Dokumenter eierskapet.</span>", p="Norsk sykkelregister med QR-merke.<br>Sjekk om en sykkel er meldt stjålet."),
  "og-image-en.png": dict(soon="Coming soon", h1="Register your bike.<br><span>Document your ownership.</span>", p="A Norwegian bike registry with QR stickers.<br>Check whether a bike is reported stolen."),
}
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for out, v in VARIANTS.items():
            html = TPL
            for k, val in v.items(): html = html.replace("{" + k + "}", val)
            tmp = ROOT / "_og_tmp.html"; tmp.write_text(html, encoding="utf-8")
            await pg.goto(tmp.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(ROOT / out)); tmp.unlink()
            print("wrote", out)
        await b.close()
asyncio.run(main())
