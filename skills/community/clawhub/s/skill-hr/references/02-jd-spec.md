# Job description (JD) specification

## Required fields

Aligned with P01 output schema:

- `role_title` — Short label for incidents and search.
- `mission_statement` — Single-sentence purpose.
- `must_have_competencies` — Non-empty; observable.
- `deliverables` — Concrete artifacts.
- `success_criteria` — Checklist for P05.
- `complexity_tier` — `S` \| `M` \| `L`.
- `search_queries` — 3–5 short strings for P02a recall (see P01).
- `competency_tags` — 3–8 normalized tags for P02a (see P01).

## Optional but recommended

- `nice_to_have`, `tools_and_access`, `constraints`, `risk_notes`.

## Retrieval-oriented fields (required by P01; consumed by P02a)

Fed to **P02a** broad recall; keep stable and specific:

- **`search_queries`** — short phrases for lexical / host search over installed skills (artifact types, product names, verbs like “audit” vs “draft”).
- **`competency_tags`** — normalized tags, ideally prefixed by dimension from the competency model (e.g. `domain:security`, `artifact:xlsx`, `integration:browser`).

**Quality:** Queries should not duplicate `role_title` only; include **orthogonal** angles (deliverable format, stack, risk). Tags should be **exclusive enough** to separate commonly confused skills (e.g. SEO audit vs SEO article writing).

## JD quality checklist (before matching)

1. **Uniqueness** — Could a stranger pick the right skill from `role_title` + `mission_statement` alone?
2. **Measurability** — Each success criterion is yes/no or has an explicit metric.
3. **Scope** — `do_not_do` implied by constraints (if not, add to P03).
4. **Dependencies** — Credentials, API keys, VPN, or hardware called out in `risk_notes`.
5. **Alignment** — No competency listed that is not needed (trim bloat to improve matching).

## Anti-patterns

- **Tool-only JD** — "Use Claude" is not a competency; name the outcome.
- **Kitchen-sink JD** — Split into sequential JDs if multiple unrelated deliverables.

## Versioning

If the user changes requirements mid-flight, append **JD revision** in the incident body (`v2`, `v3`) rather than silently overwriting P01 output in older incidents.
