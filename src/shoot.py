"""Screenshots via Playwright: python src/shoot.py [base_url] [outdir]"""
import sys, asyncio
from playwright.async_api import async_playwright
base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
out = sys.argv[2] if len(sys.argv) > 2 else "/workspace/bike-registry/screenshots/landing"
pages = [("home", "/"), ("en", "/en/"), ("404", "/id/K7M3-9QX2-C")]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for dev, vp, mobile in [("desktop", {"width": 1440, "height": 900}, False), ("mobile", {"width": 390, "height": 844}, True)]:
            ctx = await b.new_context(viewport=vp, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)
            pg = await ctx.new_page()
            msgs = []
            pg.on("console", lambda m: msgs.append(m.text))
            pg.on("requestfailed", lambda r: msgs.append("FAILED " + r.url))
            for name, path in pages:
                await pg.goto(base + path, wait_until="networkidle")
                await pg.evaluate("document.fonts.ready")
                # trigger lazy images, then return to top
                await pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo({top:y,behavior:'instant'});await new Promise(r=>setTimeout(r,60))}window.scrollTo({top:0,behavior:'instant'});await new Promise(r=>setTimeout(r,200))}")
                await pg.wait_for_load_state("networkidle")
                await pg.screenshot(path=f"{out}/{dev}-{name}-full.png", full_page=True)
                await pg.screenshot(path=f"{out}/{dev}-{name}.png")
                sw = await pg.evaluate("document.documentElement.scrollWidth")
                print(dev, name, "scrollWidth", sw, "vp", vp["width"])
            print(dev, "console/failed:", msgs)
            await ctx.close()
        await b.close()
asyncio.run(main())
