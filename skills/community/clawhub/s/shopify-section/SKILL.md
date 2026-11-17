---
name: shopify-section
description: Turn a section of any live website into a Shopify theme section (.liquid) the user adds to their store. Use when the user runs a Shopify store and wants a hero, pricing, header, footer, features, testimonials, FAQ or CTA "like <url>", or asks for a Liquid section, a Shopify section file or a theme section copied from a website.
homepage: https://miromiro.app/api/website-to-shopify-section-api
metadata: {"openclaw": {"emoji": "🛍️", "homepage": "https://miromiro.app/api/website-to-shopify-section-api", "primaryEnv": "MIROMIRO_API_KEY"}}
---

# Website section → Shopify Liquid section

MiroMiro reads the live page, resolves its real CSS (colors, fonts, spacing, responsive and
hover styles) and returns a complete Shopify theme section file. The user saves it in their
theme and adds it to any page from the theme editor.

## 1. Get the section

**With the MiroMiro tools connected** (Claude, ChatGPT, Cursor, Codex): call `extract_code`
with `url`, `framework: "shopify"` and, when the user named a part of the page, `section`.

**Without them** (OpenClaw and other agents): call the REST API with the user's key.

```bash
curl -s "https://miromiro.app/api/v1/code?url=allbirds.com&section=hero&framework=shopify" \
  -H "Authorization: Bearer $MIROMIRO_API_KEY"
```

No key yet? The user gets one free at https://miromiro.app/api/onboarding (300 credits a
month, no card). Ask them for it; never invent one.

`section` is one of `hero`, `header`, `footer`, `pricing`, `features`, `testimonials`,
`faq`, `cta`. Omit it for the hero. Never guess a CSS selector: the response lists the
page's other sections in `sections`, each with a ready `selector` for a second call.

A call costs 25 credits. If the result is thin or carries a `hint`, retry the same URL once
with `render=true` (+5 credits) so the page's JavaScript runs first. Never render first.

## 2. Hand over the file

`code` is the whole `.liquid` file. Give it to the user **complete and unmodified**. Name it
after the section, e.g. `sections/stripe-pricing.liquid`. `css` is null on purpose: the
styles are inside the file.

## 3. Tell them how to add it

1. Shopify admin → **Online Store → Themes** → on the theme, **⋯ → Edit code**.
2. In the **sections** folder, **Add a new section**, give it the file's name, replace the
   placeholder content with the whole file, **Save**.
3. **Customize** the theme, open a page, **Add section**, pick the new one.

Do **not** paste it into a *Custom Liquid* block: that block is capped at 50 KB and cannot
hold the section's schema. It has to be a file in the sections folder.

If you are working in a local theme repo (Shopify CLI), write the file to
`sections/<name>.liquid` yourself and tell the user to run `shopify theme push` or
`shopify theme dev`.

## 4. Set expectations

- The section arrives as **one styled HTML block** inside the Liquid file. Text and images
  are changed in the file's HTML.
- Responsive and hover styles are included, and the CSS is scoped so it cannot clash with
  the theme.
- The text and images belong to the site it came from. Unless it is the user's own site,
  tell them to replace the copy, logo and photos with their own before publishing.

## Good to know

- `theme: "dark"` returns the site's dark version when it has one; the response's `theme`
  field says which you got.
- Need a different format of the same section? Call again with `framework` set to
  `tailwind`, `html`, `jsx`, `vue` or `elementor` (a new 25-credit extraction).
- Docs: https://miromiro.app/api/docs
