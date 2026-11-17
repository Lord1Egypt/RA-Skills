# Brand Profile — Reusable Style, Voice & Building Blocks

> Read this to use or create a `brand-profile.md` — a single file the user keeps so every future
> email is consistent and fast to build (the "one-click" experience). Offer to create it after the
> first email, when you've already learned some of the brand's choices.

## Table of Contents
1. Why a brand profile
2. The brand-profile.md format
3. How the skill uses it
4. Offering to create one

---

## 1. Why a brand profile

Without it, every email re-asks for colors, fonts, logo, socials, and tone. With it, the user
attaches one file and the skill produces on-brand emails immediately — no questionnaire. It also
stores the **approved, pre-checked building blocks** the task asks for, so the AI assembles emails
from trusted parts instead of improvising each time.

## 2. The brand-profile.md format

All fields optional; the skill falls back to defaults for anything missing.

```markdown
# Brand Profile

## Identity
company_name: "Acme Coffee"
logo_url: "https://files.sendpulse.com/.../logo.png"   # prefer a File Manager URL
logo_width: 140
website: "https://acme.coffee"

## Colors
primary_color: "#0055CC"
accent_color: "#FF6600"
background_color: "#EEEEEE"
content_bg: "#FFFFFF"
text_color: "#333333"
muted_color: "#808080"

## Typography
font_stack: 'Arial, "Helvetica Neue", Helvetica, sans-serif'
heading_font_stack: 'Georgia, serif'
border_radius: 6

## Voice & tone
tone: "warm, plain-spoken, lightly witty; never pushy"
formality: "casual second person (ты/you)"
do: ["short sentences", "lead with reader benefit", "concrete specifics"]
dont: ["corporate jargon", "ALL CAPS", "fake urgency", "AI buzzwords"]
languages: ["en", "uk", "ru"]   # languages you send in

## Contacts & social (reusable footer block)
address: "12 Market St, Kyiv, Ukraine"
support_email: "hello@acme.coffee"
social_facebook: "https://facebook.com/acme"
social_instagram: "https://instagram.com/acme"
social_telegram: "https://t.me/acme"

## UTM convention
utm_source: "sendpulse"
utm_medium: "email"
utm_campaign_format: "<season>_<promo>_<year>"   # e.g. spring_sale_2026

## Approved building blocks (pre-checked, reusable)
# Paste verified HTML snippets the AI should reuse verbatim, e.g. the exact header,
# footer with socials, and standard CTA. Reference them by name here:
blocks:
  - name: "header"        # logo + nav, approved
  - name: "footer"        # socials + address + unsubscribe, approved
  - name: "cta_primary"   # brand button style

## Image library (File Manager URLs to reuse)
images:
  - role: "logo"     url: "https://files.sendpulse.com/.../logo.png"
  - role: "hero_bg"  url: "https://files.sendpulse.com/.../hero.jpg"
```

## 3. How the skill uses it

- **Read it first** when attached; skip all branding questions it answers.
- Apply colors, fonts, radius to the html-rules.md patterns.
- Reuse the **approved blocks verbatim** (header/footer/CTA) — assemble emails from trusted parts.
- Reuse **File Manager image URLs** instead of placeholders.
- Match the **tone/voice** rules in copywriting (see content-copywriting.md).
- Apply the **UTM convention** automatically (see variables-analytics.md).
- Use the listed **languages** to know which locales to support (see i18n.md).

## 4. Offering to create one

After delivering the first email, offer:
> "Want me to save these choices as a **brand-profile.md**? Next time you just attach it and I'll
> build on-brand emails with no setup questions. I can also bank your approved header/footer and
> your UTM format so everything stays consistent."

Then generate the file from what you learned, ask for the few missing fields (socials, address,
UTM format), and save it to the working folder.
