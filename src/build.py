"""Static site generator for bygoodnesstravels.com. Run: python3 src/build.py  -> writes docs/"""
import json
from datetime import date
from html import escape
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "docs"
SITE = "https://bygoodnesstravels.com"
NAME = "ByGoodness Travels"
PHONE, PHONE_DISPLAY, WA = "+97430995071", "+974 3099 5071", "https://wa.me/97430995071"
EMAIL, IG, IG_URL = "info@bygoodnesstravels.com", "@bygoodnesstravels", "https://www.instagram.com/bygoodnesstravels/"
TODAY = date.today().isoformat()

NAV = [
    ("/", "Home"), ("/about/", "About Us"), ("/flights-holidays/", "Flights & Holidays"),
    ("/visa-assistance/", "Visa Assistance"), ("/travel-services/", "Travel Services"),
    ("/consulting/", "Consulting"), ("/business/", "Business"), ("/contact/", "Contact Us"),
]
LEGAL = [("/privacy-policy/", "Privacy Policy"), ("/terms/", "Terms & Conditions"), ("/booking-policy/", "Booking & Cancellation Policy")]

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>'

ORG = {
    "@type": "TravelAgency", "@id": f"{SITE}/#org", "name": NAME, "url": f"{SITE}/",
    "logo": f"{SITE}/assets/img/icon-512.png", "image": f"{SITE}/assets/img/og.png",
    "slogan": "Explore · Connect · Grow",
    "description": "Travel planning, holiday packages, flight and hotel booking assistance, visa application guidance, tours, airport transfers and selected administrative support.",
    "telephone": PHONE, "email": EMAIL, "sameAs": [IG_URL],
    "address": {"@type": "PostalAddress", "addressCountry": "QA"},
    "areaServed": [{"@type": "Country", "name": "Qatar"}, "Worldwide"],
    "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "email": EMAIL, "contactType": "customer service",
                     "availableLanguage": ["English"]},
}


def ld(*objs):
    graph = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "@id": f"{SITE}/#site", "url": f"{SITE}/", "name": NAME, "publisher": {"@id": f"{SITE}/#org"}}, *objs]}
    return f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>'


def crumbs_ld(path, title):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
             {"@type": "ListItem", "position": 2, "name": title, "item": f"{SITE}{path}"}]
    return {"@type": "BreadcrumbList", "itemListElement": items}


def service_ld(path, name, desc):
    return {"@type": "Service", "name": name, "description": desc, "provider": {"@id": f"{SITE}/#org"},
            "areaServed": "Worldwide", "url": f"{SITE}{path}"}



# Library photographs (Hallmark library, Wikimedia Commons). Each sits in a data-slot so her own pictures replace it.
PHOTOS = {
    "lagoon": ("two fishermen hauling a net across white sand by a turquoise lagoon", 1920, 1261,
               '<a href="https://commons.wikimedia.org/wiki/File:Fishermen_at_Kavarathi,_Lakshadweep,_India_(edit).jpg">Shafeeq Thamarassery</a> (CC BY-SA 4.0)'),
    "jet-bridge": ("a traveller with a suitcase walking down a jet bridge", 1920, 2509,
                   '<a href="https://commons.wikimedia.org/wiki/File:Tocumen_International_Airport_alt.jpg">Wilfredor</a> (CC0)'),
    "hotel-suite": ("a four-poster bed with white drapes in a hotel suite", 1920, 1280,
                    '<a href="https://commons.wikimedia.org/wiki/File:Canopy_bed_of_Khan_Pool_Suite_in_Amantaka_luxury_Resort_%26_Hotel_in_Luang_Prabang_Laos.jpg">Basile Morin</a> (CC BY-SA 4.0)'),
    "souk-lanterns": ("metal lanterns glowing in a souk", 1440, 2017,
                      '<a href="https://commons.wikimedia.org/wiki/File:Oriental_hanging_lanterns._Souk_Haddadine,_Marrakech_Medina,_Morocco.jpg">Petar Milošević</a> (CC BY-SA 4.0)'),
    "dune": ("a tall orange dune in sun and shadow against a blue sky", 1920, 1280,
             '<a href="https://commons.wikimedia.org/wiki/File:006_Dune_45_in_Sossusvlei_at_sunrise_Photo_by_Giles_Laurent.jpg">Giles Laurent</a> (CC BY-SA 4.0)'),
    "pen": ("a fountain pen writing on white paper", 1920, 1408,
            '<a href="https://commons.wikimedia.org/wiki/File:Fountain_pen_writing_(literacy).jpg">Petar Milošević</a> (CC BY-SA 4.0)'),
    "beach-dusk": ("two people walking along a beach at dusk", 1920, 989,
                   '<a href="https://commons.wikimedia.org/wiki/File:Family_walking_at_the_evening,_cox%27s_bazar_.jpg">Ferdous</a> (CC BY-SA 3.0)'),
}


def photo(key, slot, want, sizes="100vw", hero=False, pos=None):
    alt, w, h, _ = PHOTOS[key]
    load = 'fetchpriority="high"' if hero else 'loading="lazy" decoding="async"'
    style = f' style="object-position: {pos}"' if pos else ""
    return (f'<div data-slot="{slot}" data-alt="{escape(want)}">'
            f'<img src="/assets/photos/{key}-1920.jpg" srcset="/assets/photos/{key}-960.jpg 960w, /assets/photos/{key}-1920.jpg {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{escape(alt)}" {load}{style}></div>')


def head(path, title, desc, extra_ld=(), preload_img=None):
    url = f"{SITE}{path}"
    pre = (f'<link rel="preload" as="image" href="/assets/photos/{preload_img}-1920.jpg" '
           f'imagesrcset="/assets/photos/{preload_img}-960.jpg 960w, /assets/photos/{preload_img}-1920.jpg 1920w" imagesizes="100vw" fetchpriority="high">\n') if preload_img else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#112B50">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/CormorantGaramond-VF.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Jost-VF.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="/assets/site.css?v=2">
{ld(*extra_ld)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(path)}
<main id="main">
"""


def header(path):
    cur = lambda h: ' aria-current="page"' if h == path else ""
    links = "".join(f'<a href="{h}"{cur(h)}>{escape(l)}</a>' for h, l in NAV[1:])
    return f"""<header class="site-head"><div class="container">
  <a class="brand" href="/" aria-label="{NAME} home"><img src="/assets/img/logo.svg" alt="{NAME}" width="300" height="88"></a>
  <div class="nav-end">
    <nav class="nav-links" id="nav" aria-label="Main">{links}</nav>
    <a class="btn btn-primary" href="{WA}" rel="noopener">WhatsApp us</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  </div>
</div></header>"""


CREDITS = ", ".join(p[3] for p in PHOTOS.values())


def footer():
    nav = "".join(f'<li><a href="{h}">{escape(l)}</a></li>' for h, l in NAV) + '<li><a href="/faq/">FAQ</a></li>'
    legal = "".join(f'<li><a href="{h}">{escape(l)}</a></li>' for h, l in LEGAL)
    return f"""</main>
<footer class="site-foot"><div class="container">
  <div class="sign-off">
    <p>Let us help you plan your next journey.</p>
    <p class="from">ByGoodness Travels. Your Journey. Your World. Our Commitment.</p>
  </div>
  <div class="foot-grid">
    <div style="display:grid;gap:var(--space-md);align-content:start">
      <img class="foot-logo" src="/assets/img/logo-white.svg" alt="{NAME}" width="300" height="88" loading="lazy">
      <p class="tagline">Explore<br>Connect<br>Grow</p>
      <p>Travel planning, holiday experiences, visa application assistance and selected administrative support.</p>
    </div>
    <div><h2>Pages</h2><ul>{nav}</ul></div>
    <div><h2>Contact</h2><ul>
      <li><a href="{WA}" rel="noopener">Phone / WhatsApp: {PHONE_DISPLAY}</a></li>
      <li><a href="mailto:{EMAIL}">Email: {EMAIL}</a></li>
      <li><a href="{IG_URL}" rel="noopener">Instagram: {IG}</a></li></ul>
      <h2 style="margin-top:var(--space-lg)">Policies</h2><ul>{legal}</ul></div>
  </div>
  <div class="colophon"><span>© {date.today().year} ByGoodness Travels. All rights reserved.</span><span data-credits>Photographs (Wikimedia Commons): {CREDITS}</span></div>
</div></footer>
<a class="wa-float" href="{WA}?text=Hello%20ByGoodness%20Travels%2C%20I%20would%20like%20to%20plan%20a%20trip." rel="noopener" aria-label="Chat on WhatsApp">{WA_ICON}<span>WhatsApp</span></a>
<script src="/assets/site.js?v=2" defer></script>
</body>
</html>
"""


def page_head(path, title, h1, lead):
    return f"""<section class="page-head"><div class="container">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">{escape(title)}</span></nav>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
</div></section>"""


def close(h, line, label, href="/contact/"):
    """The hire close: a plain contact, set large."""
    return f"""<section class="sec contact-close"><div class="container">
  <div class="head"><h2>{h}</h2><p class="lead">{line}</p></div>
  <div class="actions"><a class="btn btn-primary" href="{href}">{label}</a></div>
  <ul class="channels">
    <li><span class="label">Phone / WhatsApp</span><a href="{WA}" rel="noopener">{PHONE_DISPLAY}</a></li>
    <li><span class="label">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><span class="label">Instagram</span><a href="{IG_URL}" rel="noopener">{IG}</a></li>
  </ul>
</div></section>"""


def ticks(items, cls=""):
    return f'<ul class="ticks {cls}">' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def items(pairs, n=3):
    return f'<div class="items" style="--n:{n}">' + "".join(
        f"<div><h3>{escape(h)}</h3><p>{escape(p)}</p></div>" for h, p in pairs) + "</div>"


def steps(pairs):
    return '<ol class="steps">' + "".join(f"<li><h3>{escape(h)}</h3><p>{escape(p)}</p></li>" for h, p in pairs) + "</ol>"


SERVICES = [
    ("/flights-holidays/", "Flights & Travel Bookings", "Get assistance with flight enquiries, itinerary planning and travel arrangements tailored to your destination, schedule and budget."),
    ("/flights-holidays/", "Holiday Packages & Tours", "Explore exciting destinations through thoughtfully planned holidays, city tours, sightseeing experiences and customised travel packages."),
    ("/visa-assistance/", "Visa Application Assistance", "Receive guidance on visa application requirements, supporting documents and application preparation for your intended destination. Visa decisions remain with the relevant immigration authorities."),
    ("/travel-services/", "Hotel & Accommodation Reservations", "Find accommodation options suited to your travel preferences, itinerary and budget."),
    ("/travel-services/", "Airport Transfers & Travel Support", "Arrange airport pick-ups, drop-offs and selected travel-related services to help make your journey more convenient."),
    ("/consulting/", "Consulting & Administrative Services", "Access assistance with selected administrative processes, business support and documentation-related services, subject to applicable requirements."),
]
LINK_LABEL = {"/flights-holidays/": "Flights and holidays", "/visa-assistance/": "Visa assistance", "/travel-services/": "Hotels, tours and transfers", "/consulting/": "Consulting services"}

FAQ = [
    ("Can I request a customised travel package?", "Yes. You can tell us your preferred destination, dates, number of travellers, budget and the services you would like included. We can then discuss suitable available options."),
    ("Can you assist with visa applications?", "We provide application guidance and document preparation assistance for selected destinations. Eligibility and final decisions rest with the relevant immigration authorities."),
    ("Are flights and hotels included in every package?", "No. Inclusions vary by package. Please review the quotation and written booking confirmation to understand what is included and excluded."),
    ("Can I request a quotation before making a payment?", "Yes. You can contact us with your requirements and request a quotation. Any applicable service fees, supplier charges, payment deadlines and cancellation conditions should be explained before you confirm."),
    ("Are travel packages subject to availability?", "Yes. Prices, flights, hotel rooms, tours and other services may change until bookings are confirmed, subject to the relevant supplier’s terms."),
    ("How do I contact ByGoodness Travels?", f"You can reach us by WhatsApp at {PHONE_DISPLAY}, email {EMAIL} or Instagram {IG}."),
]


def faq_html(qs):
    return '<div class="faq">' + "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in qs) + "</div>"


HOW = [("Tell us your plans", "Share your destination, travel dates, number of travellers and budget."),
       ("Receive your options", "We will review your requirements and provide suitable available options."),
       ("Confirm your arrangements", "Review the itinerary, inclusions, exclusions and payment terms before proceeding."),
       ("Prepare for your journey", "Receive the relevant booking details and travel information for your confirmed arrangements.")]

pages = {}

# ---------------- HOME ----------------
rows = "".join(
    f'<li><h3>{escape(t)}</h3><p>{escape(d)}</p><a class="text-link" href="{h}">{LINK_LABEL[h]}</a></li>'
    for h, t, d in SERVICES)
pages["/"] = head("/", "ByGoodness Travels | Travel Agency, Holiday Packages & Visa Assistance",
                  "Plan flights, holiday packages, hotels, tours, airport transfers and visa application assistance with ByGoodness Travels. Personalised travel support. WhatsApp +974 3099 5071.",
                  preload_img="lagoon") + f"""
<section class="hero">
  {photo("lagoon", "hero", "A wide photograph of a destination ByGoodness Travels has arranged, calm area low and left for the headline", hero=True, pos="62% 55%")}
  <div class="container">
    <h1>Your Journey.<br>Your World.<br>Our Commitment.</h1>
    <p class="lead">Flights, holidays, visas and transfers, planned around your needs.</p>
    <div class="actions"><a class="btn btn-primary" href="/contact/">Plan your trip</a><a class="btn btn-quiet" href="#services">Explore our services</a></div>
  </div>
</section>

<section class="sec-l statement"><div class="container">
  <p>At ByGoodness Travels, we help make travel planning simpler through personalised travel services, holiday experiences and practical support for your travel needs.</p>
  <div class="follow">
    <p>Whether you are planning a family holiday, a business trip, an international getaway or exploring new opportunities abroad, we are here to help you take the next step with greater confidence.</p>
    <a class="btn btn-quiet" href="/about/">About us</a>
  </div>
</div></section>

<section class="sec rows-wrap" id="services"><div class="container grid12">
  <div class="head"><h2>Discover what we can do for you</h2><p class="lead">From flight bookings and hotel reservations to visa application assistance, tours and tailored travel packages.</p></div>
  <ul class="rows">{rows}</ul>
</div></section>

<section class="sec showcase"><div class="container">
  <figure>{photo("dune", "showcase", "A landscape from a tour or excursion ByGoodness Travels offers, wide 21:9 crop")}
    <figcaption>Desert excursions, city tours, cultural landmarks and relaxing getaways, arranged as part of your itinerary.</figcaption></figure>
  <div class="pair">
    <figure>{photo("hotel-suite", "photo-2", "A hotel room or resort the agency books, 4:3", sizes="(max-width: 40rem) 100vw, 66vw")}<figcaption>Hotel and accommodation reservations</figcaption></figure>
    <figure>{photo("souk-lanterns", "photo-3", "A market, old town or cultural visit, portrait 3:4", sizes="(max-width: 40rem) 100vw, 33vw")}<figcaption>City tours and sightseeing</figcaption></figure>
  </div>
</div></section>

<section class="sec-l tint"><div class="container">
  <div class="head"><h2>How it works</h2></div>
  {steps(HOW)}
</div></section>

<section class="sec rows-wrap"><div class="container grid12">
  <div class="head"><h2>Frequently asked questions</h2><p class="lead"><a class="text-link" href="/faq/">All questions and answers</a></p></div>
  {faq_html(FAQ[:3])}
</div></section>
""" + close("Your next destination starts here",
            "Tell us your destination, preferred dates, number of travellers and budget. We will help you explore suitable options.",
            "Request a travel quote") + footer()

# ---------------- ABOUT ----------------
p = "/about/"
pages[p] = head(p, "About Us | ByGoodness Travels",
                "ByGoodness Travels is a travel and business support brand helping individuals, families and organisations with travel arrangements and selected administrative needs.",
                [crumbs_ld(p, "About Us")]) + page_head(p, "About Us", "Welcome to ByGoodness Travels",
    "A travel and business support brand for individuals, families and organisations.") + f"""
<section class="sec"><div class="container grid12 with-photo">
  <div class="copy prose">
    <p class="lead">ByGoodness Travels is a travel and business support brand committed to helping individuals, families and organisations navigate travel arrangements and selected administrative needs with greater ease.</p>
    <p>We believe that travel is more than moving from one place to another. It creates opportunities to discover cultures, reconnect with loved ones, build relationships, pursue business interests and experience the world from new perspectives.</p>
    <p>Our approach combines personalised assistance, clear communication and attention to detail. We aim to understand each client’s needs and provide practical options that align with their travel plans.</p>
    <p>Whether you are preparing for an international holiday, arranging a business trip or seeking guidance on selected administrative services, we strive to make the process clearer and more convenient.</p>
  </div>
  <figure>{photo("beach-dusk", "about", "A photograph from one of her own trips or a client journey, portrait 4:5", sizes="(max-width: 60rem) 100vw, 40vw", pos="72% 45%")}</figure>
</div></section>

<section class="sec-l on-ink"><div class="container pair-text">
  <div><h2>Our Mission</h2><p>To provide dependable, customer-focused travel and administrative support that helps people explore opportunities, discover destinations and plan their journeys with confidence.</p></div>
  <div><h2>Our Vision</h2><p>To grow into a trusted international travel and business support brand recognised for professionalism, personalised service and meaningful customer relationships.</p></div>
</div></section>

<section class="sec-l"><div class="container">
  <div class="head"><h2>Our core values</h2></div>
  {items([
    ("Integrity", "We value honest communication, transparency and responsible service delivery."),
    ("Customer Commitment", "We listen to our clients and work to understand their individual needs."),
    ("Professionalism", "We approach every enquiry with care, organisation and attention to detail."),
    ("Reliability", "We aim to communicate clearly, provide agreed services and keep clients informed throughout the process."),
    ("Global Perspective", "We embrace the opportunities that travel, cultural exchange and international connections can create."),
    ("Our Promise", "Clear information, personalised attention and practical assistance at every stage of your enquiry, so you can prepare for your journey with greater peace of mind."),
  ], 3)}
</div></section>
""" + close("Let us help you plan your next journey", "Tell us where you would like to go and what you need.", "Contact us") + footer()

# ---------------- FLIGHTS & HOLIDAYS ----------------
p = "/flights-holidays/"
desc = "Flight booking assistance, holiday and family packages, city tours, hotels, airport transfers, tailor-made itineraries and group travel planning with ByGoodness Travels."
pages[p] = head(p, "Flights & Holiday Packages | ByGoodness Travels", desc,
                [crumbs_ld(p, "Flights & Holidays"), service_ld(p, "Flights & Holiday Packages", desc)]) + page_head(
    p, "Flights & Holidays", "Discover your next adventure",
    "Every journey begins with a destination in mind. We help turn your plans into a well-organised itinerary.") + f"""
<section class="sec"><div class="container grid12 with-photo">
  <div class="copy">
    <div class="head" style="margin:0"><h2>Our travel services</h2><p class="lead">We assist with travel enquiries and arrangements for individuals, couples, families, groups and business travellers.</p></div>
    {ticks(["Flight enquiries and booking assistance", "Return and one-way travel arrangements", "Hotel and accommodation reservations", "Holiday and family travel packages", "City tours and sightseeing experiences", "Airport transfers", "Tailor-made itineraries", "Group travel planning"])}
  </div>
  <figure>{photo("jet-bridge", "flights", "A travel photograph: boarding, an airport or a client departing, portrait 4:5", sizes="(max-width: 60rem) 100vw, 40vw")}</figure>
</div></section>

<section class="sec-l tint rows-wrap"><div class="container grid12">
  <div class="head"><h2>Travel your way</h2></div>
  <ul class="rows">{"".join(f"<li><h3>{escape(h)}</h3><p>{escape(d)}</p></li>" for h, d in [
    ("Family Holidays", "Create meaningful memories with travel plans designed around your family’s preferences and needs."),
    ("Leisure & Getaway Trips", "Explore new destinations, relax and enjoy experiences beyond your everyday routine."),
    ("Business Travel", "Get assistance coordinating travel arrangements for meetings, conferences and other professional engagements."),
    ("Group Travel", "Planning a trip with friends, colleagues or a larger group? Contact us to discuss your destination, dates and requirements."),
    ("Custom Travel Packages", "Have a destination in mind? We can help you explore available flights, accommodation, tours and other services to build a package around your preferences."),
  ])}</ul>
</div></section>

<section class="sec-l"><div class="container">
  <div class="head"><h2>How it works</h2></div>
  {steps(HOW)}
</div></section>
""" + close("Ready for a holiday?", "Share your destination, dates, number of travellers and budget.", "Request a holiday package", "/contact/?service=holiday") + footer()

# ---------------- VISA ----------------
p = "/visa-assistance/"
desc = "Visa application assistance: requirement guidance, document checklists, supporting documents and application preparation for selected destinations. Visa decisions rest with the authorities."
pages[p] = head(p, "Visa Application Assistance | ByGoodness Travels", desc,
                [crumbs_ld(p, "Visa Assistance"), service_ld(p, "Visa Application Assistance", desc)]) + page_head(
    p, "Visa Assistance", "Prepare for your international journey",
    "Assistance with visa application preparation and travel documentation for selected destinations.") + f"""
<section class="sec"><div class="container grid12 with-photo">
  <div class="copy">
    <p class="lead" style="color:var(--color-ink)">Understanding visa requirements can be an important part of planning international travel.</p>
    <div class="head" style="margin:0"><h2>Our support may include</h2></div>
    {ticks(["General guidance on application requirements", "Document checklists and application preparation", "Assistance organising supporting documents", "Travel itinerary and accommodation documentation where applicable", "Guidance on application procedures and submission requirements", "Travel preparation information"], "one")}
  </div>
  <figure>{photo("pen", "visa", "Documents being prepared at a desk, no readable personal details, portrait 4:5", sizes="(max-width: 60rem) 100vw, 40vw", pos="30% 50%")}</figure>
</div></section>

<section class="sec-l tint"><div class="container grid12">
  <div style="grid-column:1 / span 5"><h2>Our approach</h2></div>
  <div class="prose" style="grid-column:7 / span 6">
    <p class="lead">Every destination has its own immigration rules, eligibility criteria and application procedures. Requirements may also differ depending on your nationality, residence status, travel purpose and personal circumstances.</p>
    <p>We help clients understand the applicable process and prepare their applications as carefully as possible.</p>
    <p class="note"><strong>Important:</strong> Visa approval is determined solely by the relevant embassy, consulate or immigration authority. We do not guarantee visa approval, processing times or entry into any country. Government fees, service charges, appointments and supporting documents will be explained where applicable before a service is confirmed.</p>
  </div>
</div></section>
""" + close("Planning an international trip?", "Tell us your destination, nationality and travel purpose.", "Enquire about visa assistance", "/contact/?service=visa") + footer()

# ---------------- HOTELS, TOURS & TRANSFERS ----------------
p = "/travel-services/"
desc = "Hotel reservations, city tours and excursions, airport transfers and destination experiences arranged around your itinerary by ByGoodness Travels."
pages[p] = head(p, "Hotels, Tours & Airport Transfers | ByGoodness Travels", desc,
                [crumbs_ld(p, "Travel Services"), service_ld(p, "Hotels, Tours & Airport Transfers", desc)]) + page_head(
    p, "Travel Services", "Experience more at every destination",
    "A memorable trip involves more than a flight. We help with accommodation, sightseeing and ground transport.") + f"""
<section class="sec showcase"><div class="container">
  <figure>{photo("hotel-suite", "hotels", "A hotel or resort the agency books, wide 21:9 crop")}<figcaption>All services are subject to availability, supplier terms and confirmation at the time of booking.</figcaption></figure>
</div></section>

<section class="sec"><div class="container">
  {items([
    ("Hotel Reservations", "Explore accommodation options based on your destination, preferred dates, room requirements and budget."),
    ("City Tours & Excursions", "Discover local attractions, cultural landmarks, shopping areas and sightseeing experiences through available tour options."),
    ("Airport Transfers", "Enquire about airport pick-ups and drop-offs to help coordinate your arrival and departure."),
    ("Destination Experiences", "Tell us what you would like to experience, whether it is a cultural excursion, a family-friendly attraction, a city discovery tour or a relaxing getaway."),
  ], 2)}
</div></section>
""" + close("Plan your destination experience", "Tell us where you are going and what you would like to see.", "Plan your experience", "/contact/?service=tours") + footer()

# ---------------- CONSULTING ----------------
p = "/consulting/"
desc = "Business registration guidance, document preparation, administrative support and general consultancy for selected processes, subject to applicable regulations."
pages[p] = head(p, "Consulting & Administrative Services | ByGoodness Travels", desc,
                [crumbs_ld(p, "Consulting"), service_ld(p, "Consulting & Administrative Services", desc)]) + page_head(
    p, "Consulting", "Practical support for your administrative needs",
    "Assistance with selected administrative processes and business support services.") + f"""
<section class="sec"><div class="container">
  <div class="head"><h2>What we can help with</h2><p class="lead">Depending on the service requested and applicable regulations, our offerings may include:</p></div>
  {ticks(["Business registration guidance and documentation assistance", "Administrative and document preparation support", "Guidance on selected government application processes", "Assistance with identifying relevant application requirements", "General administrative consultancy", "Selected business support and international service enquiries"])}
</div></section>

<section class="sec-l tint"><div class="container grid12">
  <div style="grid-column:1 / span 5"><h2>Clear steps, organised paperwork</h2></div>
  <div class="prose" style="grid-column:7 / span 6">
    <p class="lead">We aim to help clients understand the steps involved, identify the documentation required and organise their applications more efficiently.</p>
    <p class="note">Some services require direct engagement with government agencies, licensed professionals or authorised service providers. Our assistance does not replace official decisions, legal advice or services that must be performed by an authorised professional.</p>
  </div>
</div></section>
""" + close("Tell us what you need", "Describe the process or document you need help with.", "Discuss your requirements", "/contact/?service=consulting") + footer()

# ---------------- BUSINESS ----------------
p = "/business/"
desc = "Enquiries about selected business support services, international professional travel and general trading opportunities with ByGoodness Travels."
pages[p] = head(p, "Business & International Opportunities | ByGoodness Travels", desc,
                [crumbs_ld(p, "Business"), service_ld(p, "Business & International Opportunities", desc)]) + page_head(
    p, "Business", "Connect with new possibilities",
    "International travel and business can open doors to new relationships, experiences and opportunities.") + f"""
<section class="sec-l statement"><div class="container">
  <p>ByGoodness Travels welcomes enquiries relating to selected business support services, international travel for professional purposes and general trading opportunities within our scope of operations.</p>
  <div class="follow"><p>We can help you discuss your requirements, identify the type of assistance needed and understand the next steps for your enquiry.</p></div>
</div></section>

<section class="sec-l tint"><div class="container">
  <div class="head"><h2>For business-related requests, please provide</h2></div>
  {items([("Your project", "A brief description of what you are working on."), ("Destination or market", "Where the project or travel is intended."), ("Timeline", "When you need the support."), ("Form of support", "The type of assistance you would prefer.")], 4)}
  <p class="note" style="margin-top:var(--space-2xl)">All opportunities are subject to verification, eligibility, availability and applicable laws. Employment, recruitment, investment or business outcomes are not guaranteed.</p>
</div></section>
""" + close("Start a business enquiry", "Send a short description of your project, market and timeline.", "Make a business enquiry", "/contact/?service=business") + footer()

# ---------------- CONTACT ----------------
p = "/contact/"
opts = ["Flights & travel bookings", "Holiday package or tour", "Visa application assistance", "Hotel & accommodation", "Airport transfer", "Consulting & administrative services", "Business enquiry", "Other"]
pages[p] = head(p, "Contact Us | ByGoodness Travels",
                f"Contact ByGoodness Travels for flights, holiday packages, visa application assistance and administrative support. WhatsApp {PHONE_DISPLAY} or email {EMAIL}.",
                [crumbs_ld(p, "Contact Us"), {"@type": "ContactPage", "url": f"{SITE}{p}", "name": "Contact ByGoodness Travels", "about": {"@id": f"{SITE}/#org"}}]) + page_head(
    p, "Contact Us", "Let’s plan something great together",
    "Have a destination in mind? Need visa or administrative support? We would be happy to hear from you.") + f"""
<section class="sec"><div class="container grid12 contact-grid">
  <div class="side">
    <h2 style="font-size:var(--text-2xl)">ByGoodness Travels</h2>
    <ul class="channels" style="grid-template-columns:minmax(0,1fr);margin:0">
      <li><span class="label">Phone / WhatsApp</span><a href="{WA}" rel="noopener">{PHONE_DISPLAY}</a></li>
      <li><span class="label">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span class="label">Instagram</span><a href="{IG_URL}" rel="noopener">{IG}</a></li>
    </ul>
    <p class="lead">Once we receive your enquiry, we will review your requirements and respond using the contact details you provide.</p>
  </div>
  <form class="enquiry" id="enquiry" data-endpoint="" novalidate>
    <h2 class="field full" style="font-size:var(--text-2xl)">Send us an enquiry</h2>
    <div class="field"><label for="f-name">Full name</label><input id="f-name" name="Name" autocomplete="name" required></div>
    <div class="field"><label for="f-email">Email address</label><input id="f-email" name="Email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-phone">Phone or WhatsApp</label><input id="f-phone" name="Phone / WhatsApp" type="tel" autocomplete="tel" required></div>
    <div class="field"><label for="f-service">Service required</label><select id="f-service" name="Service" required><option value="">Choose a service</option>{"".join(f"<option>{escape(o)}</option>" for o in opts)}</select></div>
    <div class="field"><label for="f-dest">Destination or country <small>(if applicable)</small></label><input id="f-dest" name="Destination / country"></div>
    <div class="field"><label for="f-dates">Preferred travel dates <small>(if applicable)</small></label><input id="f-dates" name="Travel dates" placeholder="e.g. 12 to 20 December"></div>
    <div class="field"><label for="f-trav">Number of travellers <small>(if applicable)</small></label><input id="f-trav" name="Travellers" inputmode="numeric"></div>
    <div class="field"><label for="f-budget">Estimated budget <small>(if applicable)</small></label><input id="f-budget" name="Budget" placeholder="e.g. QAR 8,000"></div>
    <div class="field full"><label for="f-msg">Additional information</label><textarea id="f-msg" name="Details"></textarea></div>
    <div class="actions">
      <button class="btn btn-primary" type="submit" data-via="whatsapp">Send via WhatsApp</button>
      <button class="btn btn-quiet" type="submit" data-via="email">Send via email</button>
    </div>
    <p class="form-status" role="status" aria-live="polite"></p>
    <p class="form-note">Your enquiry opens in WhatsApp or your email app, ready for you to send. See our <a class="text-link" href="/privacy-policy/">Privacy Policy</a>.</p>
  </form>
</div></section>
""" + footer()

# ---------------- FAQ ----------------
p = "/faq/"
faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
pages[p] = head(p, "Frequently Asked Questions | ByGoodness Travels",
                "Answers about custom travel packages, visa application assistance, package inclusions, quotations, availability and how to contact ByGoodness Travels.",
                [crumbs_ld(p, "FAQ"), faq_ld]) + page_head(p, "FAQ", "Frequently asked questions",
    "Packages, quotations, visas and how to reach us.") + f"""
<section class="sec rows-wrap"><div class="container grid12">
  <div class="head"><h2>Before you book</h2><p class="lead">Still unsure? Message us on WhatsApp.</p></div>
  {faq_html(FAQ)}
</div></section>
""" + close("Still have a question?", "Message us and we will get back to you.", "Contact us") + footer()


# ---------------- LEGAL ----------------
def legal(path, title, desc, intro, sections):
    body = "".join(f"<h2>{escape(h)}</h2>" + "".join(
        (f"<ul>{''.join(f'<li>{escape(x)}</li>' for x in t)}</ul>" if isinstance(t, list) else f"<p>{escape(t)}</p>") for t in ps)
        for h, ps in sections)
    pages[path] = head(path, f"{title} | ByGoodness Travels", desc, [crumbs_ld(path, title)]) + page_head(
        path, title, escape(title), escape(intro)) + f"""
<section class="sec"><div class="container legal"><p class="updated">Last updated: {date.today().strftime('%d %B %Y')}</p>{body}</div></section>
""" + footer()


legal("/privacy-policy/", "Privacy Policy", "How ByGoodness Travels collects, uses and protects the personal information you share with us.",
      "How we collect, use and protect the information you share with us.", [
    ("Information we collect", ["The details you send when you contact us, such as your name, email address, phone or WhatsApp number, travel dates, destination, number of travellers, budget and the information you include in your message.",
                                ["Identity and travel documents you choose to share for bookings or visa application assistance."]]),
    ("How we use it", [["To respond to your enquiry and prepare quotations.", "To arrange the services you confirm, including sharing necessary details with airlines, hotels, tour operators, transfer providers and other suppliers.", "To help prepare application documents you request.", "To meet legal, accounting and regulatory obligations."]]),
    ("Sharing", ["We share personal information only with suppliers and authorities as needed to provide the services you request, or where required by law. We do not sell your personal information."]),
    ("Retention and security", ["We keep information only as long as needed for the purposes above and take reasonable steps to protect it."]),
    ("Your choices", [f"You may ask to access, correct or delete your personal information by contacting {EMAIL}."]),
    ("Website", ["This website does not use advertising cookies. When you send an enquiry, it opens in WhatsApp or your email app, and those services apply their own privacy terms."]),
])
legal("/terms/", "Terms & Conditions", "Terms and conditions for using the ByGoodness Travels website and services.",
      "The terms that apply when you use our website and services.", [
    ("Our services", ["ByGoodness Travels provides travel planning, booking assistance, visa application guidance and selected administrative and business support services. Details of each service, including fees, inclusions and exclusions, are confirmed in writing before you proceed."]),
    ("Quotations and prices", ["Quotations are based on availability at the time they are prepared. Prices, flights, hotel rooms, tours and other services may change until bookings are confirmed."]),
    ("Supplier terms", ["Airlines, hotels, tour operators and other suppliers apply their own terms and conditions, which form part of your booking."]),
    ("Visa and government services", ["Visa approval and government decisions are made solely by the relevant authorities. We do not guarantee approval, processing times or entry into any country."]),
    ("Your responsibilities", [["Provide accurate and complete information and documents.", "Hold a valid passport, visas and any health or entry documents required for your trip.", "Review your quotation and booking confirmation carefully."]]),
    ("Liability", ["We act with reasonable care in arranging services. We are not responsible for the acts or omissions of independent suppliers or authorities, or for events beyond our reasonable control."]),
    ("Contact", [f"Questions about these terms: {EMAIL} or WhatsApp {PHONE_DISPLAY}."]),
])
legal("/booking-policy/", "Booking & Cancellation Policy", "How bookings, payments, changes and cancellations work with ByGoodness Travels.",
      "How bookings, payments, changes and cancellations work.", [
    ("Making a booking", ["A booking is confirmed only after you accept the quotation, the applicable terms and payment conditions, and we issue a written confirmation."]),
    ("Payments", ["Payment amounts, deadlines and accepted methods are stated in your quotation. Some suppliers require full payment at the time of booking."]),
    ("Changes", ["Change requests depend on supplier rules and availability. Supplier change fees and fare differences may apply, as well as our service fee where stated."]),
    ("Cancellations and refunds", ["Cancellation conditions are set by each supplier and are explained before you confirm. Refunds, where available, follow the supplier’s rules and timelines. Service fees for work already completed, such as visa application preparation, may be non-refundable where stated."]),
    ("Travel insurance", ["We recommend that you take out suitable travel insurance when you book."]),
    ("Contact", [f"To change or cancel a booking, contact us by WhatsApp {PHONE_DISPLAY} or email {EMAIL}."]),
])

# ---------------- 404 ----------------
pages["/404.html"] = head("/404.html", "Page not found | ByGoodness Travels", "The page you are looking for could not be found.").replace(
    '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">') + page_head(
    "/404.html", "Page not found", "This page is not on our map", "It may have moved. Go back to the homepage or get in touch.") + """
<section class="sec-s"><div class="container"><div class="actions"><a class="btn btn-primary" href="/">Go to the homepage</a><a class="btn btn-quiet" href="/contact/">Contact us</a></div></div></section>
""" + footer()

# ---------------- write ----------------
for path, html in pages.items():
    out = DIST / ("404.html" if path == "/404.html" else path.strip("/") + "/index.html" if path != "/" else "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)

urls = [p for p in pages if p != "/404.html"]
prio = {"/": "1.0", "/contact/": "0.9"}
(DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(u, '0.3' if u in dict(LEGAL) else '0.8')}</priority></url>\n" for u in urls) + "</urlset>\n")
(DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /email/\n\nSitemap: {SITE}/sitemap.xml\n")
(DIST / "site.webmanifest").write_text(json.dumps({"name": NAME, "short_name": "ByGoodness", "icons": [{"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}, {"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}], "theme_color": "#112B50", "background_color": "#FBF8F2", "display": "standalone", "start_url": "/"}))
(DIST / "CNAME").write_text("bygoodnesstravels.com\n")  # GitHub Pages custom domain
print(len(pages), "pages")
