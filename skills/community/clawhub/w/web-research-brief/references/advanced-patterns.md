# Advanced Research Patterns

## Deep-Dive Research

For multi-hour research projects requiring exhaustive coverage:

1. **Phase 1: Landscape scan** — 5-10 broad searches to map the domain
2. **Phase 2: Gap analysis** — Identify under-covered subtopics from Phase 1
3. **Phase 3: Targeted deepening** — Focused searches on gaps
4. **Phase 4: Cross-validation** — Verify key claims across independent sources

## Search Query Templates

| Scenario | Template | Example |
|----------|----------|---------|
| Trend analysis | `"[topic] trends [year]"` | `"AI agent trends 2026"` |
| Comparison | `"[A] vs [B] [criterion]"` | `"PostgreSQL vs MySQL performance"` |
| Benchmark | `"[tool] benchmark [year]"` | `"Claude benchmark 2026"` |
| Regional | `"[topic] in [region]"` | `"EV adoption in China"` |
| Academic | `"[topic] survey OR review"` | `"RAG survey review"` |

## Handling Common Pitfalls

- **Echo chambers**: If all sources cite the same original, trace to the primary source
- **Outdated info**: Check publication dates; prefer official docs for versioned software
- **AI-generated content**: Cross-reference with primary sources; be skeptical of unsourced listicles
- **Paywalled content**: Use `web_fetch` with `extractMode: "text"` — sometimes abstracts are enough
