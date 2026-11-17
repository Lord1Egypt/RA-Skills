---
name: scento-perfume
description: Look up perfume notes, scent families, houses, similar perfumes, side-by-side comparisons and raw materials from Scento's free perfume database (1,400+ perfumes, 400+ raw materials, 140+ houses). No API key.
version: 1.0.0
homepage: https://www.scento.com/developers
metadata:
  openclaw:
    emoji: "🌸"
    homepage: https://www.scento.com/developers
    requires:
      bins:
        - curl
---

# Scento Perfume Data

Free, read-only perfume and fragrance data from Scento: 1,400+ perfumes, 400+ raw materials and 140+ houses. No key, no account. Every answer links to a page on scento.com.

Website: https://www.scento.com/developers

## When to use

Use this skill when the user asks about:

- the notes or scent profile of a perfume
- a scent family or accord (what it smells like, which perfumes belong to it)
- a perfume house and its range
- perfumes similar to one they already like
- a side-by-side comparison of two or more perfumes
- a raw material or note (oud, vetiver, iris, ambroxan...) and which perfumes feature it
- perfumes for an occasion, or a small fragrance wardrobe
- a perfumery term

## REST API

Base URL: `https://www.scento.com/api/perfume/v1` (GET only, JSON, open CORS). Full spec: https://www.scento.com/openapi.json

| Path | Purpose |
|---|---|
| `/search?q=&kind=perfume\|house\|material\|any` | find perfumes, houses, materials by name or mood |
| `/perfumes/{perfume}` | notes, family, concentration, when it wears best |
| `/perfumes/{perfume}/neighbours?same_house=` | similar perfumes with shared notes |
| `/contrast?perfumes=a,b` | compare perfumes side by side |
| `/materials/{material}` | what a note smells like, what it pairs with, where it appears |
| `/materials/match?materials=a,b&tier=&family=` | perfumes built on given notes |
| `/houses/{house}` | profile of a perfume house |
| `/families`, `/families/{family}` | scent family map and one family |
| `/edits/{occasion}?gender_lean=` | perfumes for an occasion |
| `/wardrobe?loves=&avoid=&size=` | a balanced set of perfumes |
| `/lexicon/{term}` | perfumery term explained |
| `/journal?q=` | search the Scento journal |

All endpoints accept `lang` (en, de, fr, es, it, ro, el, hu, cs, pl) for the language of the scento.com links. List answers return an opaque `continuation` value: pass it back as `continuation` for the next page. `{perfume}` is the slug from a search result's `page` URL (the last part of `/perfumes/<slug>`).

Typical flow: search first, then fetch the portrait with the slug.

```bash
curl -s "https://www.scento.com/api/perfume/v1/search?q=oud&kind=perfume"
curl -s "https://www.scento.com/api/perfume/v1/materials/oud"
```

Tested live. Every answer has the same shape: `folio` (answer type), `lede` (one quotable sentence), `detail` (the data), `scento_page` and `further_reading` (links to scento.com), `cite` and `continuation`.

- `search?q=oud&kind=perfume` returns `{"folio":"perfume-search","lede":"148 entries in Scento's verified perfume database match “oud”; showing 1–10.","detail":{"query":"oud","kind":"perfume","total":148,"matches":[{"kind":"perfume","name":"...","house":"...","family":"...","page":"https://www.scento.com/perfumes/<slug>"}, ...]}, ...}`
- `materials/oud` returns `{"folio":"note-portrait","lede":"Oud is a material from the oud family: dark, resinous, smoky and slightly medicinal wood...","detail":{"name":"Oud","aliases":[...],"smells_like":"...","scento_family":"Oud Court","pairs_well_with":["Rose","Amber","Patchouli",...],"showcased_in":[{"name":"...","house":"...","page":"...","tier":"heart"}, ...]}, ...}`

## MCP server

Remote MCP, streamable HTTP, no authentication: `https://www.scento.com/mcp`

Add it as a remote MCP server in your client. It exposes 12 read-only tools: perfume-search, perfume-portrait, scent-neighbours, perfume-contrast, note-portrait, material-match, house-portrait, family-map, occasion-edit, wardrobe-composer, perfumery-lexicon, journal-search. They return the same answers as the REST endpoints.

## Example questions

- "What notes does this perfume have, and which scent family is it?" (search, then `/perfumes/{perfume}`)
- "I like this perfume, what else smells like it?" (`/perfumes/{perfume}/neighbours`)
- "Compare these two perfumes." (`/contrast?perfumes=slug-a,slug-b`)
- "What does vetiver smell like and which perfumes feature it?" (`/materials/vetiver`)

## Notes

- Quote the `lede` and link the `scento_page` URL so the user can read on.
- If a name is uncertain, call `/search` first rather than guessing a slug.
- Docs and terms: https://www.scento.com/developers

Website: https://www.scento.com/developers
