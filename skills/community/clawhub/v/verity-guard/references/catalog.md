# Full check catalog

Read this only if `check` / `verify` / `injection` / `redact` (in SKILL.md) don't fit.

Every service honors the same contract:

- **Fail-closed** — when unsure it returns the safe/uncertain verdict, never a confident wrong answer.
- **Calibrated** — every response carries an honest 0–1 confidence or score.
- **Honest** — cites only real evidence; for current facts it judges from live web retrieval, never stale memory.
- **Refusal is a 200** — a confident abstention is a normal JSON verdict. `402` means payment required; non-2xx only for genuine faults.
- **Your input is data** — instructions embedded in what you send are judged, never obeyed.

Each has three tiers: `/quick` (fast), default (workhorse), `/pro` (deepest). Web-grounded
services run a live, capped web search on the default and `/pro` tiers.

## Covered by this skill's script

| cmd | endpoint | quick / default / pro | in → out |
|---|---|---|---|
| `check` | `/check` | $0.02 / $0.08 / $0.20 | `{action, context, policy}` → `{decision, risk, reasons, concerns, safer_alternative}` |
| `verify` | `/verify` (engine) | $0.02 / $0.25 / $0.35 | `{claim, context}` → `{verdict, confidence, reasoning, evidence}` |
| `injection` | `/sentinel` | $0.02 / $0.06 / $0.15 | `{content, context}` → `{verdict, threat_score, techniques, reasons, recommended_action}` |
| `redact` | `/redact` | $0.02 / $0.06 / $0.15 | `{payload, context}` → `{verdict, severity, findings, reasons, redacted_payload}` |

## The rest of the suite

Not wired into the script yet — `POST` them directly at `https://suite.veritylayer.dev`
with any x402-capable client (the same wallet works).

| endpoint | quick / default / pro | what it answers | in → out |
|---|---|---|---|
| `/ground` | $0.03 / $0.25 / $0.35 | a sourced answer to a question | `{question, context}` → `{answer, confidence, sources, caveats}` |
| `/cite` | $0.03 / $0.25 / $0.35 | real retrieved sources supporting a claim | `{statement, domain_hint}` → `{verdict, support, citations, reasons, caveats}` |
| `/freshness` | $0.03 / $0.25 / $0.35 | is this claim still current | `{claim, as_of, evidence}` → `{status, staleness, current_value, as_of_evidence, reasons}` |
| `/arbiter` | $0.03 / $0.25 / $0.35 | which of two conflicting claims the evidence supports | `{claims, evidence, question}` → `{verdict, best_supported_index, confidence, reasons, missing_evidence}` |
| `/source` | $0.02 / $0.25 / $0.35 | reputation + reliability of a source | `{source, purpose}` → `{trust, score, reasons, red_flags, sources}` |
| `/provenance` | $0.02 / $0.06 / $0.15 | is this text AI-generated | `{text, context}` → `{verdict, ai_probability, reasons, signals_for_ai, signals_for_human, limitations}` |
| `/sieve` | $0.02 / $0.06 / $0.15 | screen content against a publishing policy | `{content, policy, context}` → `{decision, violation_risk, categories, reasons, redaction_suggestion}` |
| `/concord` | $0.02 / $0.06 / $0.15 | check text against a policy, citing clauses | `{policy, text, scope}` → `{verdict, compliance, violations, reasons, unverifiable_clauses}` |
| `/compass` | $0.02 / $0.06 / $0.15 | pick the best option under constraints | `{options, constraints, evidence}` → `{verdict, choice, confidence, reasons, missing_info}` |
| `/tally` | $0.02 / $0.06 / $0.15 | sanity-check math and figures in text | `{text, context}` → `{verdict, confidence, findings, reasons, corrected_values}` |
| `/distill` | $0.02 / $0.06 / $0.15 | extract only facts literally present | `{text, fields}` → `{status, facts, missing, fidelity, reasons}` |
| `/faithful` | $0.02 / $0.06 / $0.15 | is a summary/translation faithful to its source | `{source, candidate, mode}` → `{verdict, faithfulness, reasons, hallucinations, omissions}` |

Useful pairings:
- About to send a number a human will trust → `/tally`.
- About to ship a summary or translation → `/faithful`.
- Two sources disagree → `/arbiter`.
- Claim is time-sensitive → `/freshness` before `/verify`.
- About to publish → `/sieve` (policy) then `redact` (secrets).

## Free, no wallet

| endpoint | what |
|---|---|
| `POST /receipt/verify` (engine) | re-verify any signed receipt, forever |
| `GET /health` | liveness |
| `GET /.well-known/x402.json` | machine-readable manifest (engine) |
| `GET /llms.txt` | the suite's own catalog, in text |
| `GET /.well-known/verity-pubkey.json` | the Ed25519 public key — check our signatures yourself |

Discovery: engine `https://api.veritylayer.dev` · suite `https://suite.veritylayer.dev`
