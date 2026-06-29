# HEURISTICS.md — the smell catalog for the taste pass

These are the judgment criteria for the three LLM-scored categories, plus the AI-tell
patterns you may use to adjust the script's regex-based AI Tells score. Heavily derived
from Matt Pocock's architecture skills (deletion test, deep/shallow modules) and from
field-observed traits of unreviewed AI-generated code.

Every finding cites `file:line`. If you can't point at a line, it's not a finding.

---

## Category: Architecture & Modularity (judgment, weight 25%)

**The deletion test.** For any module/abstraction layer, imagine deleting it. If the
complexity just vanishes — callers could trivially do the thing themselves — it was a
pass-through layer and counts as slop. If complexity would reappear scattered across N
callers, the module was earning its keep.

Smells to hunt:

- **Shallow modules** — interface nearly as complex as the implementation. A `UserService`
  whose every method is one line calling `UserRepository` with the same arguments. AI loves
  generating these because layered architecture *looks* professional.
- **Pass-through chains** — controller → service → manager → repository where 2 of the 4
  hops add nothing. Cite the chain.
- **Horizontal slicing taken to absurdity** — to understand one feature you must open 8
  files across 8 directories, each contributing 5 lines.
- **Layering violations** — UI importing the database client directly, a util importing a
  page component, config importing business logic. Use the import graph in `metrics.json`
  to find candidates, then read to confirm.
- **Abstraction for an audience of one** — interfaces/base classes with exactly one
  implementation and no plausible second one. One adapter is a hypothetical seam, not a real one.
- **Wrong-sized files** — one 1,200-line `index.ts` doing everything, or 40 files averaging
  9 lines. Both are failures to find module boundaries.
- **Copy-paste architecture** — three near-identical components/endpoints that should be one
  parameterized thing (the duplication metric finds candidates; you judge whether the
  duplication is structural).

What does NOT count: small projects legitimately having no layers; a flat structure in a
200-line tool is correct design, not missing design. Judge fitness-for-size.

## Category: Naming & Domain Language (judgment, weight 10%)

- **Generic vocabulary** — `handler`, `manager`, `processor`, `helper`, `util`, `data`,
  `info`, `item`, `temp`, `doStuff`, `handleClick2`. Names that describe nothing.
- **No domain language** — the business clearly has concepts (orders, invoices, listings)
  but the code calls everything `data` and `items`. Good code names things what the
  *domain* calls them.
- **The same concept under multiple names** — `user` / `account` / `profile` / `member`
  used interchangeably for one thing. Strong signal nobody owned the vocabulary.
- **Numbered or adjective-suffixed duplicates** — `utils2.ts`, `helpersNew.ts`,
  `finalFinalConfig.js`, `ComponentV2` coexisting with `Component`.
- **Misleading names** — `validateUser()` that also writes to the database; `constants.ts`
  full of mutable state.

## Category: Consistency (judgment, weight 10%)

The question: *was anyone steering?* Mixed conventions are the clearest fingerprint of
many uncorrelated generation sessions pasted together.

- Mixed async styles (`.then()` chains and `async/await` interleaved in the same file/module)
- Mixed naming cases (`snake_case` and `camelCase` for the same kind of identifier)
- Three different ways to call the same API (raw `fetch`, an axios wrapper, AND a generated client)
- Mixed module systems (`require` and `import` in sibling files without a build reason)
- Multiple state-management or styling approaches doing the same job
  (CSS modules + styled-components + inline Tailwind on sibling components)
- Error handling that changes philosophy per file: some throw, some return `{error}`,
  some swallow silently
- Formatting chaos with no formatter config present

## AI Tells (script + your ±15 adjustment, weight 15%)

The script counts regex-detectable tells. Use your reading to adjust ±15 points — these
are the tells regexes can't reliably catch:

- **Narrating comments** — comments that restate the next line: `// Loop through the users`,
  `// Return the result`. The #1 tell.
- **Tutorial voice** — `// First, we need to...`, `// Note that...`, `// As you can see...`.
  Code written *at* an imagined reader.
- **Hedge/apology comments** — `// In a real application you would...`,
  `// For simplicity, we...`, `// This is a simplified version...`. The model admitting
  it shipped a demo.
- **Placeholder residue** — `// TODO: implement actual logic`, `YOUR_API_KEY_HERE`,
  `example.com` endpoints in production paths, lorem ipsum in shipped UI.
- **Ritual try/catch** — every function wrapped in try/catch that just `console.error`s and
  rethrows or returns null. Error *theater*, not error handling.
- **Defensive null-checking of impossible states** — checking `if (!array)` on a value
  produced two lines earlier.
- **Emoji-section-header comments** in source files (`// 🚀 Main Logic`).
- **The triple-redundant ending** — a comment, a console.log, and a return all saying the
  same thing.
- **README inflation** — badges for CI that doesn't exist, "Features" lists describing
  unimplemented things, the word "robust" or "production-ready" describing a 1-file demo.

Counter-evidence (push the score DOWN): comments that explain *why* rather than *what*,
domain-specific tricks, references to real issues/tickets, TODO items with names/dates,
deliberate suppressions with justification (`// eslint-disable-next-line ... because X`).

## Script-owned categories (do not re-score by hand; trust metrics.json)

- **Coupling & Dependencies (15%)** — circular imports, god files everything touches.
- **Duplication (15%)** — cross-file duplicated line windows.
- **Dead Weight (10%)** — orphan files nothing imports, commented-out code blocks.

You may flag *individual* findings in these categories (e.g. name the worst cycle as a
finding so it appears in the report with a fix-it prompt), but the category scores come
from the script.
