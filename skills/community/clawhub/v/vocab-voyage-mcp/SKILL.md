# Vocab Voyage — MCP Skill

Vocabulary tutor and standardized test prep tools for **ISEE, SSAT, SAT, PSAT, GRE, GMAT, LSAT** and general academic vocabulary. Hosted MCP server — no install required.

## When to use

Invoke Vocab Voyage when a user needs:

- A definition with part of speech, example sentence, synonyms, antonyms
- A multiple-choice vocabulary quiz scoped to a specific test
- A list of vocabulary words from a specific test-prep course
- A 7-day study plan preview
- An explanation of what a word means inside a specific sentence
- The Word of the Day (general or test-scoped)

## Endpoints

- **MCP server**: `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server`
- **Public REST API**: `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/vocab-api`
- **Natural-language `/ask`**: `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/nlweb-ask` (POST `{"query": "..."}`, supports SSE via `prefer.streaming: true`)
- **OpenAPI spec**: https://vocab.voyage/openapi.json
- **Server card**: https://vocab.voyage/.well-known/mcp/server-card.json
- **Agent card**: https://vocab.voyage/.well-known/agent-card.json
- **Auth + scopes reference**: https://vocab.voyage/developers/auth
- **Live demo + docs**: https://vocab.voyage/mcp

## Tools

| Tool | Purpose |
|---|---|
| `get_word_of_the_day` | Today's vocab word, optionally scoped to a test family |
| `get_definition` | Definition, part of speech, example, synonyms/antonyms |
| `generate_quiz` | Multiple-choice quiz (1–10 questions) for a test family |
| `get_course_word_list` | Sample words from a specific course |
| `list_courses` | All 13 test-prep courses with slugs and descriptions |
| `explain_word_in_context` | Explain a word inside a specific sentence |
| `study_plan_preview` | 7-day, 5-words-per-day sample plan |

## MCP Apps UI widgets

For agents that support MCP Apps, three tools attach a renderable widget via `_meta.ui.resourceUri`:

| Tool | Widget |
|---|---|
| `get_definition` | `ui://vocab-voyage/definition` — definition card with example + synonyms |
| `generate_quiz` | `ui://vocab-voyage/quiz` — interactive multiple-choice quiz |
| `study_plan_preview` | `ui://vocab-voyage/study-plan` — 7-day plan grid |

Manifest: https://vocab.voyage/.well-known/mcp/apps.json

## Authentication

Anonymous access works for every public tool — no token required.

For personalized tools (mastery, streaks, profile-aware sessions), pass a personal MCP token:

```
Authorization: Bearer vv_mcp_…
```

### Where to get a token

1. Sign in at https://vocab.voyage/auth
2. Open https://vocab.voyage/mcp
3. Click **Generate token**, choose scopes, copy the `vv_mcp_…` value (shown once)

Full reference, rotation, and revocation: https://vocab.voyage/developers/auth

### Scopes

| Scope | Grants |
|---|---|
| `mcp.read` | Read MCP metadata and public tool results. Required for any MCP usage. |
| `mcp.tools` | Invoke public MCP tools (definition, quiz, courses, study plan). |
| `profile.read` | Read connected user's display name, account type, preferred course. |
| `progress.read` | Read mastery, streaks, and recent sessions for the connected user. |

## Rate limits

- Anonymous: **60 req/min per IP**
- Authenticated: **600 req/hour per user**

## Example prompts

- Define "aberrant" and give a test-prep example.
- Generate a 5-question SAT vocabulary quiz.
- List Vocab Voyage courses for ISEE and SSAT.
- Build a 7-day GRE vocabulary study plan preview.
- Explain "table" in the sentence: "Let's table this discussion."

## Error format

All errors are structured JSON:

```json
{ "error_code": "string", "message": "string", "hint": "string", "retry_after": 0 }
```

Common `error_code` values: `unauthorized`, `insufficient_scope`, `token_revoked`, `rate_limited`, `invalid_request`, `not_found`, `server_error`.
