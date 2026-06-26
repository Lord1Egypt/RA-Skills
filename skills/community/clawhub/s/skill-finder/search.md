# Search Strategies — Skill Finder

Reference for skill finder, find skills, Skills.sh search, and ClawHub search requests.

## Search Sources

| Source | Search | Inspect | Install | Notes |
|--------|--------|---------|---------|-------|
| `ClawHub Search` | `npx clawhub search "query"` | `npx clawhub inspect <slug>` | `npx clawhub install <slug>` | Best for curated registry results and built-in metadata |
| `Skills.sh Search` | `npx skills find [query]` | Inspect returned page/repo | `npx skills add <owner/repo@skill>` | Best for wider open-ecosystem discovery |

Default mode is `both`. Search a single source only if `~/skill-finder/memory.md` says `sources: clawhub` or `sources: skills.sh`, or the user overrides it.

## Commands

```bash
# ClawHub
npx clawhub search "query"
npx clawhub search "react testing"
npx clawhub inspect <slug>
npx clawhub inspect <slug> --files  # see all files
npx clawhub install <slug>
npx clawhub explore
npx clawhub list

# Skills.sh / skills CLI
npx skills find
npx skills find react performance
npx skills add vercel-labs/agent-skills@frontend-design
npx skills list
npx skills check
npx skills update
```

## Dual-Source Search Flow

For a new query:

1. Read `~/skill-finder/memory.md`
2. Check `Status.sources`
3. If mode is `both`, search both ecosystems with the same intent
4. Compare the strongest matches together before recommending
5. Keep the source and exact install command attached to each result

## Trigger Recognition

Search even when the user does not explicitly say "skill":

| User signal | What it usually means |
|-------------|------------------------|
| "How do I do X?" | A skill may already solve this |
| "Can you do this?" | Possible capability gap |
| "There must be a better way" | Search for a specialized workflow |
| "What should I install?" | Direct skill discovery request |
| "This current skill is weak" | Replacement search |

## Search by Need, Not Name

User says "I need help with PDFs" — don't just search "pdf".

Think about what they actually need:

| User Need | Better Search |
|-----------|--------------|
| Edit PDFs | `npx clawhub search "pdf edit"` + `npx skills find pdf edit` |
| Create PDFs | `npx clawhub search "pdf create"` + `npx skills find pdf generate` |
| Extract from PDFs | `npx clawhub search "pdf extract"` + `npx skills find pdf parse` |
| Fill PDF forms | `npx clawhub search "pdf form"` + `npx skills find pdf form` |

## Expand Search Terms

If first search yields poor results:

1. **Synonyms** — edit → modify, create → generate, check → validate
2. **Related tools** — pdf → document, docx → word
3. **Underlying task** — "pdf form" → "form filling"
4. **Domain name** — "stripe payments" → just "stripe"

## Interpret Results

Normalize each result into the same decision shape:
- Source
- Name / identifier
- What it does
- Install command
- Quality signals

Typical signals:
- `ClawHub`: name, description, downloads, author, update freshness
- `Skills.sh`: returned install string, source repo, skills.sh page, and project reputation

**Quick quality signals:**
- High downloads + recent update = well-maintained
- Clear description = probably well-structured
- Multiple skills by same author = established creator
- Recognizable repo or maintainer = safer bet in `Skills.sh`
- Vague description = likely low quality

## Multiple Results Strategy

When several skills match:

1. **Filter** — Apply quality criteria (see `evaluate.md`)
2. **Rank** — By fit to specific need, not just downloads
3. **Present top 3** — With reasoning for each
4. **Pick a winner** — Give a recommendation, not just options
5. **Let user choose** — Or ask clarifying questions

Example response:
> Found 3 options for React testing:
> 1. `react-testing` (ClawHub) — focuses on component tests, 5k downloads
> 2. `vercel-labs/agent-skills@frontend-design` (Skills.sh) — broader frontend workflow guidance
> 3. `testing` (ClawHub) — general testing, includes React section
>
> Which fits your project better?

## Query Refinement

| Situation | Action |
|-----------|--------|
| Too many results | Add specificity: "python" → "python async" |
| No results | Broaden: "fastapi oauth2" → "api auth" |
| Wrong domain | Clarify: "testing" → "unit testing" vs "e2e testing" |
| Tool-specific | Try tool name directly: "stripe", "twilio" |
| One source is empty | Keep the other source, but say that only one ecosystem produced matches |

## Search Operators

The search is semantic (meaning-based), not keyword-exact.

- `"react hooks"` finds skills about React patterns
- `"api testing"` finds REST, GraphQL testing skills
- `"deploy docker"` finds containerization + deployment

No special operators needed — describe what you want in natural language.
