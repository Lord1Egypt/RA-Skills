# SEOwlsClaw — SEO Rules Index (v0.9)

> Load `universal.md` first — it applies to every page type. Then load the file matching the
> active page type. Loaded at Step 2f of `BRAIN_ARCHITECTURE.md`, right before content
> generation (Step 3), so the brain writes to these rules instead of only being audited against
> them afterward.
>
> Each rule file contains: Do's · Don'ts · Required Elements · Recommended Elements · Keyword
> Placement Rules. `SEO_CHECKS/` still owns HARD FAIL/WARNING scoring, pass-rate math, and the
> audit report format — these files define the rule values it scores against.

---

## Available Rule Files

| File | Scope | Applies To |
|------|-------|------------|
| `SEO_RULES/universal.md` | All page types | Every `write`/`writehtml` call, loaded first |
| `SEO_RULES/landingpage.md` | `Landingpage` | Sale campaigns, promotions, newsletter launches |
| `SEO_RULES/blogpost.md` | `Blogpost` | Organic SEO articles, guides |
| `SEO_RULES/productnew.md` | `Productnew` | New physical/digital products |
| `SEO_RULES/productused.md` | `Productused` | Refurbished/second-hand items |
| `SEO_RULES/faq.md` | `FAQ` | Standalone FAQ pages |
| `SEO_RULES/socialphoto.md` | `Socialphoto` | Image posts, alt text |
| `SEO_RULES/socialvideo.md` | `Socialvideo` | YouTube/TikTok metadata |

---

## How Step 2f Loads These Files

```
Step 2f-1: Load SEO_RULES/universal.md → merge into seo_rules{}
Step 2f-2: Match page_type (from Step 1 parse or Step 0 intent detection) →
           load SEO_RULES/<page_type>.md → merge into seo_rules{}
Step 2f-3: seo_rules{} is available to Step 3 (Generate Variables) and to Step 6 (SEO Checks),
           which audits generated content against the same values instead of a separate copy.

Skip condition: same as Step 2d/2e — skipped entirely for seoplan/seobrief (no page content
generated, so no writing rules are needed).
```

---

*Last updated: 2026-08-24 (v0.9)*
*Maintainer: Chris — SEO_RULES registry, mirrors PERSONAS/_index.md*
