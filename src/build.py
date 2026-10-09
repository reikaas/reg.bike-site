#!/usr/bin/env python3
"""Generates index.html (nb), en/index.html and 404.html from one template.
Run from the repo root:  python3 src/build.py
No build dependencies beyond the Python standard library."""
from pathlib import Path
from urllib.parse import quote
import html

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://reg.bike"
MAIL = "post@reg.bike"

def mailto(subject, body):
    return f"mailto:{MAIL}?subject={quote(subject)}&amp;body={quote(body)}"

# ---------- icons (inline SVG, decorative) ----------
W, O = "#FFFFFF", "#FF6600"
ICON_REGISTER = f'''<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect x="6" y="4" width="17" height="24" rx="2.5" fill="none" stroke="{W}" stroke-width="2.2"/><path d="M10.5 10.5h8M10.5 15h8M10.5 19.5h4.5" stroke="{W}" stroke-width="2.2" stroke-linecap="round"/><path d="M19.5 25.5l7.8-7.8 2.4 2.4-7.8 7.8-3.2.8z" fill="{O}"/></svg>'''
ICON_STICKER = f'''<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect x="4" y="4" width="24" height="24" rx="4" fill="none" stroke="{W}" stroke-width="2.2"/><rect x="8.5" y="8.5" width="6" height="6" fill="{W}"/><rect x="17.5" y="8.5" width="6" height="6" fill="{W}"/><rect x="8.5" y="17.5" width="6" height="6" fill="{W}"/><path d="M17.5 17.5h2.5v2.5h-2.5zM21 21h2.5v2.5H21z" fill="{O}"/></svg>'''
ICON_SCAN = f'''<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect x="8" y="3" width="16" height="26" rx="3" fill="none" stroke="{W}" stroke-width="2.2"/><path d="M14 25.5h4" stroke="{W}" stroke-width="2" stroke-linecap="round"/><path d="M11.5 14.5l3 3 6-6.5" fill="none" stroke="{O}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
N = "#0E2442"
FACT_QR = f'''<svg viewBox="0 0 26 26" aria-hidden="true" focusable="false"><rect x="2" y="2" width="9" height="9" rx="1" fill="none" stroke="{N}" stroke-width="2"/><rect x="15" y="2" width="9" height="9" rx="1" fill="none" stroke="{N}" stroke-width="2"/><rect x="2" y="15" width="9" height="9" rx="1" fill="none" stroke="{N}" stroke-width="2"/><path d="M15 15h3v3h-3zM21 15h3v3h-3zM18 18h3v3h-3zM15 21h3v3h-3zM21 21h3v3h-3z" fill="{O}"/></svg>'''
FACT_DROP = f'''<svg viewBox="0 0 26 26" aria-hidden="true" focusable="false"><path d="M13 2.5C9 8 6 11.8 6 15.6a7 7 0 0 0 14 0C20 11.8 17 8 13 2.5z" fill="none" stroke="{N}" stroke-width="2" stroke-linejoin="round"/><path d="M9.8 15.8l2.3 2.3 4.3-4.8" fill="none" stroke="{O}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
FACT_PHONE = f'''<svg viewBox="0 0 26 26" aria-hidden="true" focusable="false"><rect x="6" y="2" width="14" height="22" rx="2.5" fill="none" stroke="{N}" stroke-width="2"/><circle cx="13" cy="11" r="3.4" fill="none" stroke="{O}" stroke-width="2"/><path d="M11 20.5h4" stroke="{N}" stroke-width="2" stroke-linecap="round"/></svg>'''
SHIELD = f'''<svg class="shield" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><path d="M32 4l22 8v17c0 14.5-9.4 25.6-22 31C19.4 54.6 10 43.5 10 29V12z" fill="{N}"/><rect x="23" y="29" width="18" height="14" rx="2.5" fill="#fff"/><path d="M26.5 29v-4.5a5.5 5.5 0 0 1 11 0V29" fill="none" stroke="#fff" stroke-width="3"/><circle cx="32" cy="35" r="2.2" fill="{O}"/></svg>'''
MAIL_ICON = '''<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><rect x="2" y="4" width="16" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M2.8 5.2L10 11l7.2-5.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>'''

# ---------- copy ----------
NB = dict(
    lang="nb", locale="nb_NO", alt_locale="en_GB", prefix="", url=f"{SITE}/", alt_url=f"{SITE}/en/",
    og_image=f"{SITE}/og-image.png",
    title="reg.bike – norsk sykkelregister · Kommer snart",
    desc="Registrer sykkelen gratis og få ditt eget QR-merke. Skriv det ut selv, eller bestill slitesterke merker i posten. Alle som finner sykkelen eller vil kjøpe den, kan sjekke om den er meldt stjålet. Kommer snart.",
    og_title="reg.bike · Din sykkel – registrert og sporbar.",
    og_alt="reg.bike-logoen og et QR-merke til sykkelen med teksten «Din sykkel – registrert og sporbar.»",
    skip="Gå til hovedinnholdet", home_label="reg.bike – til forsiden", nav_label="Hovedmeny",
    nav=[("#slik", "Slik fungerer det"), ("#fordeler", "Fordeler"), ("#merket", "Klistremerket"), ("#pris", "Pris"), ("#personvern", "Personvern")],
    other_lang="English", other_lang_code="en", other_href="en/", other_label="Read this page in English",
    nav_cta="Få beskjed",
    soon="Kommer snart", slogan="Din sykkel&nbsp;– registrert og sporbar.",
    h1="Registrer sykkelen. Få den igjen hvis den blir stjålet.",
    lead="reg.bike er et nytt norsk sykkelregister. Du registrerer rammenummeret og fester et QR-merke på sykkelen. Da kan alle som finner den eller vil kjøpe den, sjekke på sekunder om den er meldt stjålet.",
    cta="Få beskjed når vi åpner", cta2="Slik fungerer det",
    perks=["<strong>Gratis</strong> å registrere", "Skriv ut klistremerket <strong>gratis</strong> hjemme", "Eller bestill slitesterke merker i posten for en liten sum"],
    fine="Du trenger ingen app, bare kameraet på mobilen.",
    hero_img_alt="Eksempel på et stående reg.bike-merke til seterøret: «Registrert · Sporbar», sykkel-ID K7M3-9QX2-C, QR-kode og teksten «Funnet sykkelen? Skann og kontakt eieren».",
    how_k="Slik fungerer det", how_h="Tre steg, så er sykkelen merket",
    how_i="Registreringen tar et par minutter. Etter det gjør klistremerket jobben.",
    steps=[(ICON_REGISTER, "Registrer gratis", "Opprett en gratis konto og legg inn merke, modell, farge, rammenummer og bilder av sykkelen."),
           (ICON_STICKER, "Merk sykkelen", "Du får ditt eget QR-merke. Skriv det ut gratis hjemme, eller bestill slitesterke klistremerker i posten for en liten sum. Fest merket på rammen."),
           (ICON_SCAN, "Skann og sjekk", "Alle kan skanne merket eller slå opp koden og se med en gang om sykkelen er registrert eller meldt stjålet.")],
    ben_k="Fordeler", ben_h="Til nytte for eier, finner og kjøper",
    ben_i="Ett klistremerke på rammen gjør det enklere for alle tre.",
    cards=[("owner", "For deg som eier sykkelen", ["Rammenummer, bilder og kjennetegn samlet på ett sted", "Meld sykkelen stjålet – alle som skanner den, ser det med en gang", "Merket viser at sykkelen er registrert og kan spores", "Alle opplysningene er klare når du anmelder tyveriet"]),
           ("finder", "For deg som finner en sykkel", ["Skann merket med mobilkameraet – du trenger ingen app", "Se om sykkelen er meldt stjålet", "Send eieren en melding via reg.bike – eieren forblir anonym"]),
           ("buyer", "For deg som kjøper brukt", ["Sjekk koden eller rammenummeret før du betaler", "Se om sykkelen er meldt stjålet", "Tryggere handel for både kjøper og selger"])],
    st_k="Klistremerket", st_h="Et tydelig signal til tyven",
    st_i="Hver sykkel får sin egen kode. Merket finnes i to formater: stående, som passer på seterøret, og liggende.",
    st_cap1="Stående, 30&nbsp;×&nbsp;60&nbsp;mm", st_cap2="Liggende, 62&nbsp;×&nbsp;29&nbsp;mm",
    st_alt1="Stående reg.bike-merke med sykkel-ID og QR-kode",
    st_alt2="Liggende reg.bike-merke med teksten «Registrert sykkel», QR-kode, koden K7M3-9QX2-C og «Skann og se om den er stjålet»",
    st_note="Eksempel. Kodeformatet og utseendet kan endres før lansering.",
    facts=[(FACT_QR, "Unik kode for hver sykkel", "QR-koden åpner <span class=\"url\">reg.bike/id/&lt;kode&gt;</span>. Koden står også i klartekst, så du kan skrive den inn selv."),
           (FACT_DROP, "Skriv ut gratis eller bestill", "Skriv ut merket gratis hjemme, eller bestill slitesterke, værbestandige merker fra oss til en lav pris."),
           (FACT_PHONE, "Fungerer med alle mobiler", "Du trenger ingen app. Statusen vises rett i nettleseren:")],
    pill_ok="✓ Registrert", pill_bad="! Meldt stjålet",
    pc_k="Pris", pc_h="Hva koster det?",
    pc_i="Registreringen er gratis. Du betaler bare hvis du vil ha slitesterke klistremerker i posten.",
    prices=[("free", "Registrering", "Gratis", "Konto, rammenummer, bilder og en offentlig statusside for sykkelen."),
            ("free", "Skriv ut selv", "Gratis", "Last ned merket som PDF og skriv det ut på etikettark eller etikettskriver."),
            ("paid", "Merker i posten", "Liten sum", "Slitesterke, værbestandige klistremerker sendt hjem til deg. Vi setter prisen før lansering.")],
    pr_k="Personvern", pr_h="Eieren forblir anonym",
    pr_lead="Offentlige sider viser aldri eierens navn, e-post, telefonnummer eller adresse.",
    pr_list=["Den som skanner merket, ser bare sykkelens status og beskrivelse.",
             "Meldinger fra den som finner sykkelen, sendes videre til deg uten at kontaktinformasjonen din vises.",
             "Du velger selv om bildene av sykkelen skal vises offentlig.",
             "Denne siden bruker ikke informasjonskapsler, sporing eller analyseverktøy."],
    nt_h="Få beskjed når vi åpner",
    nt_p="reg.bike er under utvikling. Send oss en e-post, så sier vi fra når du kan registrere sykkelen din.",
    nt_btn="Gi meg beskjed på e-post", nt_or="Eller skriv til",
    nt_small="Vi bruker bare e-postadressen din til å si fra når vi åpner, og sletter den når du vil.",
    mail_subject="Gi meg beskjed når reg.bike åpner",
    mail_body="Hei!\n\nGi meg beskjed når jeg kan registrere sykkelen min på reg.bike.\n\n",
    ft_1="Norsk sykkelregister under utvikling.",
    ft_2="reg.bike er en privat tjeneste, ikke en offentlig myndighet.",
    ft_nav="Bunnmeny", ft_contact="Kontakt",
)
EN = dict(
    lang="en", locale="en_GB", alt_locale="nb_NO", prefix="../", url=f"{SITE}/en/", alt_url=f"{SITE}/",
    og_image=f"{SITE}/og-image-en.png",
    title="reg.bike – the Norwegian bike registry · Coming soon",
    desc="Register your bike for free and get a unique QR sticker. Print it yourself or order durable stickers by post. Anyone who finds your bike or wants to buy it can check whether it is registered or reported stolen. Coming soon.",
    og_title="reg.bike · Your bike – registered and traceable.",
    og_alt="reg.bike logo and a QR bike sticker with the words “Your bike – registered and traceable.”",
    skip="Skip to content", home_label="reg.bike – home", nav_label="Main menu",
    nav=[("#how", "How it works"), ("#benefits", "Benefits"), ("#sticker", "The sticker"), ("#pricing", "Pricing"), ("#privacy", "Privacy")],
    other_lang="Norsk", other_lang_code="nb", other_href="../", other_label="Les siden på norsk",
    nav_cta="Get notified",
    soon="Coming soon", slogan="Your bike&nbsp;– registered and traceable.",
    h1="Register your bike. Get it back.",
    lead="reg.bike is a new Norwegian bike registry. Register the frame number, put a QR sticker on your bike, and let anyone who finds it or is thinking of buying it check in seconds whether it has been reported stolen.",
    cta="Tell me when you launch", cta2="How it works",
    perks=["<strong>Free</strong> to register", "Print your sticker at home for <strong>free</strong>", "Or order durable stickers by post for a small fee"],
    fine="No app – a phone camera is all it takes.",
    hero_img_alt="Example of a portrait reg.bike sticker on a seat tube, showing bike ID K7M3-9QX2-C, a QR code and the text “Found this bike? Scan to contact the owner” in Norwegian.",
    how_k="How it works", how_h="Three steps from frame number to marked bike",
    how_i="Registering a bike takes a couple of minutes. The sticker does the rest.",
    steps=[(ICON_REGISTER, "Register for free", "Create a free account and add the make, model, colour, frame number and photos of your bike."),
           (ICON_STICKER, "Mark your bike", "You get a unique QR sticker. Print it at home for free, or order durable stickers by post for a small fee. Put it on the frame."),
           (ICON_SCAN, "Scan and check", "Anyone can scan the sticker or look up the code and see right away whether the bike is registered or reported stolen.")],
    ben_k="Benefits", ben_h="Useful for everyone who deals with bikes",
    ben_i="One sticker on the frame helps the owner, whoever finds the bike, and whoever wants to buy it.",
    cards=[("owner", "If you own the bike", ["Frame number, photos and details kept in one place", "Report it stolen, and everyone who scans it sees that right away", "The sticker shows the bike is registered and traceable", "Everything ready when you report the theft to the police"]),
           ("finder", "If you find a bike", ["Scan the sticker with your phone camera – no app needed", "See whether the bike has been reported stolen", "Message the owner through reg.bike without seeing who they are"]),
           ("buyer", "If you're buying used", ["Check the code or frame number before you pay", "See whether the bike has been reported stolen", "Safer deals for buyers and honest sellers alike"])],
    st_k="The sticker", st_h="A mark thieves notice",
    st_i="Every bike gets its own code. The sticker comes in a portrait format for the seat tube and a landscape format.",
    st_cap1="Portrait, 30&nbsp;×&nbsp;60&nbsp;mm", st_cap2="Landscape, 62&nbsp;×&nbsp;29&nbsp;mm",
    st_alt1="Portrait reg.bike sticker with bike ID and QR code",
    st_alt2="Landscape reg.bike sticker reading “Registered bike” in Norwegian, with a QR code, the code K7M3-9QX2-C and “Scan to see if it's stolen”",
    st_note="Example only. The code format and design may change before launch.",
    facts=[(FACT_QR, "A unique code for every bike", "The QR code opens <span class=\"url\">reg.bike/id/&lt;code&gt;</span>. The code is printed in plain text too, so it can be typed in."),
           (FACT_DROP, "Print free or order", "Print the sticker at home for free, or order durable, weatherproof stickers from us at a low price."),
           (FACT_PHONE, "Works with any phone camera", "No app to download. Whoever scans it sees the status right in the browser:")],
    pill_ok="✓ Registered", pill_bad="! Reported stolen",
    pc_k="Pricing", pc_h="What does it cost?",
    pc_i="Registration is free. You only pay if you want durable stickers sent by post.",
    prices=[("free", "Registration", "Free", "Account, frame number, photos and a public status page for your bike."),
            ("free", "Print it yourself", "Free", "Download the sticker as a PDF and print it on label sheets or a label printer."),
            ("paid", "Stickers by post", "Small fee", "Durable, weatherproof stickers sent to your door. We’ll set the price before launch.")],
    pr_k="Privacy", pr_h="The owner stays anonymous",
    pr_lead="Public pages never show the owner's name, email, phone number or address.",
    pr_list=["Whoever scans the sticker only sees the bike's status and description.",
             "Messages from someone who finds your bike are passed on to you without revealing your contact details.",
             "You choose whether photos of your bike are shown publicly.",
             "This website uses no cookies, tracking or analytics."],
    nt_h="Get notified when we launch",
    nt_p="reg.bike is in development. Send us an email and we'll let you know when you can register your bike.",
    nt_btn="Email me at launch", nt_or="Or write to",
    nt_small="We only use your email address to tell you about the launch, and we delete it whenever you ask.",
    mail_subject="Let me know when reg.bike launches",
    mail_body="Hi!\n\nPlease let me know when I can register my bike on reg.bike.\n\n",
    ft_1="Norwegian bike registry in development.",
    ft_2="reg.bike is a private service, not a public authority.",
    ft_nav="Footer", ft_contact="Contact",
)
# Section ids per language
IDS = {"nb": dict(how="slik", ben="fordeler", st="merket", pc="pris", pr="personvern", nt="beskjed"),
       "en": dict(how="how", ben="benefits", st="sticker", pc="pricing", pr="privacy", nt="notify")}

CSP = "default-src 'none'; img-src 'self' data:; style-src 'self'; font-src 'self'; manifest-src 'self'; base-uri 'none'; form-action 'none'"

def head(t, p, abs_assets=False, extra=""):
    a = "/" if abs_assets else p["prefix"]
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{t}</title>
{extra}<meta name="theme-color" content="#0E2442">
<link rel="preload" href="{a}fonts/IBMPlexSans-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a}style.css">
<link rel="icon" href="{a}favicon.ico" sizes="48x48">
<link rel="icon" href="{a}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{a}apple-touch-icon.png">
<link rel="manifest" href="{a}site.webmanifest">'''

def page(p):
    a = p["prefix"]; ids = IDS[p["lang"]]
    mt = mailto(p["mail_subject"], p["mail_body"])
    meta = f'''<meta name="description" content="{html.escape(p["desc"])}">
<link rel="canonical" href="{p["url"]}">
<link rel="alternate" hreflang="nb" href="{SITE}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="reg.bike">
<meta property="og:url" content="{p["url"]}">
<meta property="og:title" content="{html.escape(p["og_title"])}">
<meta property="og:description" content="{html.escape(p["desc"])}">
<meta property="og:locale" content="{p["locale"]}">
<meta property="og:locale:alternate" content="{p["alt_locale"]}">
<meta property="og:image" content="{p["og_image"]}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(p["og_alt"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(p["og_title"])}">
<meta name="twitter:description" content="{html.escape(p["desc"])}">
<meta name="twitter:image" content="{p["og_image"]}">
<meta name="twitter:image:alt" content="{html.escape(p["og_alt"])}">
'''
    nav = "\n".join(f'      <li class="hide-sm"><a href="{h}">{l}</a></li>' for h, l in p["nav"])
    steps = "\n".join(f'''      <li class="step"><span class="num" aria-hidden="true">0{i}</span><span class="icon">{ic}</span>
        <h3>{t}</h3><p>{b}</p></li>''' for i, (ic, t, b) in enumerate(p["steps"], 1))
    cards = "\n".join(f'''      <article class="card {cls}"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></article>''' for cls, t, items in p["cards"])
    facts = "\n".join(f'''        <li>{ic}<div><strong>{t}</strong>{b}</div></li>''' for ic, t, b in p["facts"])
    prl = "".join(f"<li>{x}</li>" for x in p["pr_list"])
    perks = "".join(f"<li>{x}</li>" for x in p["perks"])
    prices = "\n".join(f'''      <article class="price {cls}"><h3>{t}</h3><p class="amt">{a}</p><p>{b}</p></article>''' for cls, t, a, b in p["prices"])
    return f'''<!doctype html>
<html lang="{p["lang"]}">
<head>
{head(p["title"], p, extra=meta)}
</head>
<body>
<a class="skip" href="#main">{p["skip"]}</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{a or './'}" aria-label="{p["home_label"]}"><img src="{a}img/lockup.svg" alt="reg.bike" width="128" height="35"></a>
    <nav aria-label="{p["nav_label"]}">
     <ul class="nav">
{nav}
      <li><a class="lang" href="{p["other_href"]}" hreflang="{p["other_lang_code"]}" lang="{p["other_lang_code"]}" aria-label="{p["other_label"]}">{p["other_lang"]}</a></li>
      <li><a class="btn" href="#{ids["nt"]}">{p["nav_cta"]}</a></li>
     </ul>
    </nav>
  </div>
</header>
<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="wrap">
    <div>
      <p class="soon">{p["soon"]}</p>
      <p class="slogan">{p["slogan"]}</p>
      <h1 id="hero-title">{p["h1"]}</h1>
      <p class="lead">{p["lead"]}</p>
      <div class="actions">
        <a class="btn" href="{mt}">{MAIL_ICON}{p["cta"]}</a>
        <a class="btn ghost" href="#{ids["how"]}">{p["cta2"]}</a>
      </div>
      <ul class="perks">{perks}</ul>
      <p class="fine">{p["fine"]}</p>
    </div>
    <div class="tube">
      <picture>
        <source type="image/webp" srcset="{a}img/sticker-portrait-30x60-color.webp 1x, {a}img/sticker-portrait-30x60-color@2x.webp 2x">
        <img src="{a}img/sticker-portrait-30x60-color.png" srcset="{a}img/sticker-portrait-30x60-color@2x.png 2x" width="300" height="622" alt="{html.escape(p["hero_img_alt"])}" fetchpriority="high">
      </picture>
    </div>
  </div>
</section>

<section class="section" id="{ids["how"]}" aria-labelledby="how-title">
  <div class="wrap">
    <p class="kicker">{p["how_k"]}</p>
    <h2 id="how-title">{p["how_h"]}</h2>
    <p class="intro">{p["how_i"]}</p>
    <ol class="steps">
{steps}
    </ol>
  </div>
</section>

<section class="section alt" id="{ids["ben"]}" aria-labelledby="ben-title">
  <div class="wrap">
    <p class="kicker">{p["ben_k"]}</p>
    <h2 id="ben-title">{p["ben_h"]}</h2>
    <p class="intro">{p["ben_i"]}</p>
    <div class="cards">
{cards}
    </div>
  </div>
</section>

<section class="section" id="{ids["st"]}" aria-labelledby="st-title">
  <div class="wrap sticker-grid">
    <div>
      <p class="kicker">{p["st_k"]}</p>
      <h2 id="st-title">{p["st_h"]}</h2>
      <p class="intro">{p["st_i"]}</p>
      <ul class="facts">
{facts}
      </ul>
      <div class="status" role="list">
        <div class="pill ok" role="listitem">{p["pill_ok"]}<code>K7M3-9QX2-C</code></div>
        <div class="pill bad" role="listitem">{p["pill_bad"]}<code>H4TR-2WN8-P</code></div>
      </div>
    </div>
    <div>
      <div class="sticker-show">
        <figure class="portrait">
          <picture><source type="image/webp" srcset="{a}img/sticker-portrait-30x60-color.webp 1x, {a}img/sticker-portrait-30x60-color@2x.webp 2x"><img src="{a}img/sticker-portrait-30x60-color.png" width="300" height="622" alt="{html.escape(p["st_alt1"])}" decoding="async"></picture>
          <figcaption>{p["st_cap1"]}</figcaption>
        </figure>
        <figure class="landscape">
          <picture><source type="image/webp" srcset="{a}img/sticker-62x29-color.webp 1x, {a}img/sticker-62x29-color@2x.webp 2x"><img src="{a}img/sticker-62x29-color.png" width="520" height="234" alt="{html.escape(p["st_alt2"])}" decoding="async"></picture>
          <figcaption>{p["st_cap2"]}</figcaption>
        </figure>
      </div>
      <p class="hint">{p["st_note"]}</p>
    </div>
  </div>
</section>

<section class="section alt" id="{ids["pc"]}" aria-labelledby="pc-title">
  <div class="wrap">
    <p class="kicker">{p["pc_k"]}</p>
    <h2 id="pc-title">{p["pc_h"]}</h2>
    <p class="intro">{p["pc_i"]}</p>
    <div class="prices">
{prices}
    </div>
  </div>
</section>

<section class="section" id="{ids["pr"]}" aria-labelledby="pr-title">
  <div class="wrap">
    <div class="privacy">
      {SHIELD}
      <div>
        <p class="kicker">{p["pr_k"]}</p>
        <h2 id="pr-title">{p["pr_h"]}</h2>
        <p><strong>{p["pr_lead"]}</strong></p>
        <ul>{prl}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="{ids["nt"]}" aria-labelledby="nt-title">
  <div class="wrap">
    <div class="notify">
      <h2 id="nt-title">{p["nt_h"]}</h2>
      <p>{p["nt_p"]}</p>
      <a class="btn" href="{mt}">{MAIL_ICON}{p["nt_btn"]}</a>
      <p class="addr">{p["nt_or"]} <a href="mailto:{MAIL}">{MAIL}</a></p>
      <p class="small">{p["nt_small"]}</p>
    </div>
  </div>
</section>
</main>
<footer class="foot">
  <div class="wrap">
    <div>
      <img src="{a}img/lockup.svg" alt="reg.bike" width="110" height="30" loading="lazy">
      <p>{p["ft_1"]} {p["ft_2"]}</p>
      <p>© 2026 reg.bike</p>
    </div>
    <nav aria-label="{p["ft_nav"]}">
      <ul>
        <li><a href="mailto:{MAIL}">{p["ft_contact"]}: {MAIL}</a></li>
        <li><a href="#{ids["pr"]}">{p["pr_k"]}</a></li>
        <li><a href="{p["other_href"]}" hreflang="{p["other_lang_code"]}" lang="{p["other_lang_code"]}">{p["other_lang"]}</a></li>
      </ul>
    </nav>
  </div>
</footer>
</body>
</html>
'''

def notfound():
    p = dict(prefix="/")
    return f'''<!doctype html>
<html lang="nb">
<head>
{head("Siden finnes ikke · reg.bike", p, abs_assets=True, extra='<meta name="robots" content="noindex">\n')}
</head>
<body>
<header class="top"><div class="wrap bar"><a class="brand" href="/" aria-label="reg.bike – til forsiden"><img src="/img/lockup.svg" alt="reg.bike" width="128" height="35"></a>
<nav aria-label="Språk"><ul class="nav"><li><a class="lang" href="/en/" hreflang="en" lang="en">English</a></li></ul></nav></div></header>
<main id="main" class="wrap nf">
  <div class="box">
    <p class="code">404</p>
    <h1>Siden finnes ikke (ennå)</h1>
    <p><strong>Skannet du et reg.bike-merke?</strong> Registeret åpner snart. Da ser du sykkelens status her når du skanner merket.</p>
    <p lang="en" class="hint">Page not found. Scanned a reg.bike sticker? The registry opens soon, and scanning will then show the bike's status here.</p>
    <div class="actions">
      <a class="btn" href="/">Til forsiden</a>
      <a class="btn secondary" href="/#beskjed">Få beskjed når vi åpner</a>
    </div>
  </div>
</main>
<footer class="foot"><div class="wrap"><p>© 2026 reg.bike · <a href="mailto:{MAIL}">{MAIL}</a></p></div></footer>
</body>
</html>
'''

if __name__ == "__main__":
    (ROOT / "index.html").write_text(page(NB), encoding="utf-8")
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "en" / "index.html").write_text(page(EN), encoding="utf-8")
    (ROOT / "404.html").write_text(notfound(), encoding="utf-8")
    print("built index.html, en/index.html, 404.html")
