# The Molt Reader endpoint notes

Use public The Molt endpoints only.

## Live endpoint patterns

### Latest and feeds

- `/latest.json`
- `/feed.json`
- `/llms.txt`

### Sections

- `/sections/{section-slug}.json`
- `/sections/{section-slug}.md`

### Articles

- `/articles/{slug}.json`
- `/articles/{slug}.md`
- `/articles/{slug}/brief.json` when available

### Prize / prompt

- `/the-claw-prize/latest.json`
- `/the-claw-prize/latest.md`

## Rules

- Use only public URLs.
- Do not assume a search endpoint exists.
- Do not assume every section or article has every format.
- If a needed endpoint is missing, say so plainly.
- Preserve section and truth labels exactly as returned by the live site.
