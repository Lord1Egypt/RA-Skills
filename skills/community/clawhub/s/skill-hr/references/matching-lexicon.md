# Matching lexicon (P02a recall hints)

Use for **broad recall** only: keyword and synonym alignment between JD text and skill text. **P02b** must still score with the full rubric and evidence quotes—never promote a skill on lexicon match alone.

## Artifact families

| Family | Example tokens |
|--------|----------------|
| PDF | pdf, acroform, xfa, fillable form, extract fields |
| Spreadsheet | xlsx, xls, csv (when JD means formulas/pivot—not plain parse), workbook |
| Word | docx, tracked changes, redline, OOXML |
| Slides | pptx, deck, speaker notes, slide master |
| Image raster | png, jpeg, sprite, transparency, bitmap generation |
| Vector / code-native UI | svg path, html artifact, css-only layout |

## Integration surfaces

| Surface | Example tokens |
|---------|----------------|
| Browser automation | playwright, chromium, dom, e2e, screenshot |
| MCP | model context protocol, mcp server, tool schema, fastmcp |
| Feishu / Lark | feishu, lark, wiki url, bitable |
| Git | rebase, branch strategy, trunk-based, merge conflict |

## Competency adjacency (often confused)

| JD intent | Often-wrong neighbor | Discriminant |
|-----------|----------------------|--------------|
| On-page SEO **audit** | SEO **content writing** | audit vs draft longform |
| Security **review** | Security **implementation** | findings vs code changes |
| **Interview design** from resume | **Resume writing** for job seeker | hiring manager vs candidate |
| **Skill / HR ops** | Generic **coding** skill | registry, install, JD/match language |
| **Notebook** authoring | **Python script** only | ipynb structure vs .py |
| **MCP** server | **REST** API only | host tool discovery vs HTTP routes |

## Meta routing

- If `must_have_competencies` or `search_queries` mention **skill install**, **registry**, **which skill to use**, **fire/remove skill**: include **`skill-hr`** in P02a candidates (if installed).
- Otherwise: **exclude `skill-hr`** from scoring pool per `SKILL.md` self-routing.
