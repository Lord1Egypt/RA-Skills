# SEOwlsClaw — Persona Index

> Load this file first. Pick a persona, then load its individual file.  
> Each persona file contains: Identity · Writing Style · Tone · Vocabulary · AI Overview Rules · E-E-A-T Injection · Heading Formula · Depth Standards.

---

## Available Personas

| ID | File | Best For | Typical Tone |
|----|------|----------|--------------|
| `ecommerce-manager` | `PERSONAS/ecommerce-manager.md` | Product pages, sales, landing pages | Persuasive, urgent, benefit-first |
| `creative-writer` | `PERSONAS/creative-writer.md` | Blog storytelling, brand posts, social | Warm, imaginative, narrative |
| `blogger` | `PERSONAS/blogger.md` | Evergreen guides, educational SEO articles | Professional, structured, educational |
| `researcher` | `PERSONAS/researcher.md` | Competitor analysis, data-driven articles | Objective, analytical, fact-first |
| `vintage-expert` | `PERSONAS/vintage-expert.md` | Vintage camera listings, collector guides | Authoritative, detailed, collector-speak |
| `travel-photographer` | `PERSONAS/travel-photographer.md` | Travel gear guides, scenario-based blog posts | Practical, adventurous, context-aware |

---

## How to Apply a Persona

```bash
/persona ecommerce-manager
/persona vintage-expert --tone authoritative
/persona blogger --target ai-overview
/personas --show vintage-expert    # show full details
```

---

## Default Persona Fallback

If no `/persona` command is given before `/write`, the agent uses **`blogger`** as default.  
Reason: neutral, structured, safest for SEO output across all page types.

---

*Last updated: 2026-04-04 (v0.6)*
