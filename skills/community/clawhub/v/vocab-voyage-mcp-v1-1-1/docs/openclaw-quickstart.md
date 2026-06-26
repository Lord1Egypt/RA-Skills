# Vocab Voyage — OpenClaw Quickstart

Add Vocab Voyage's vocabulary tools to OpenClaw in under a minute. No account required for public tools (60 requests/min anonymous). Sign in for personalized study queue, missed words, and adaptive plans (600 requests/hour authenticated).

- Server endpoint: `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server`
- Transport: streamable-http
- Homepage: <https://vocab.voyage/mcp>

---

## Install (2 paths)

### Option 1 — ClawHub (recommended)

```bash
openclaw skills install vocab-voyage
```

This pulls the published skill from ClawHub (<https://clawhub.ai/jaideepdhanoa/vocab-voyage-mcp>) and registers it with your local OpenClaw runtime.

### Option 2 — Manual skill folder

Create the file `~/.openclaw/skills/vocab-voyage/SKILL.md` with the following contents:

```markdown
---
name: vocab-voyage
description: Vocabulary tools for SAT, ISEE, SSAT, GRE, GMAT, LSAT, PSAT prep — word of the day, definitions, quizzes, study plans.
metadata: { "openclaw": { "emoji": "📚", "homepage": "https://vocab.voyage" } }
---

This skill connects to the Vocab Voyage MCP server.

Server URL: https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server
Transport: streamable-http
Auth: optional Bearer token (vv_mcp_…) for personalized tools

Use this skill when the user asks for vocabulary definitions, quizzes, word of the day, or test prep word lists. Available tools: get_word_of_the_day, get_definition, generate_quiz, list_courses, get_course_word_list, explain_word_in_context, study_plan_preview.
```

Restart OpenClaw — the skill auto-loads from `~/.openclaw/skills`.

---

## Verify

```bash
openclaw skills list
```

You should see `vocab-voyage` in the output. If you do not, confirm the skill folder path and restart OpenClaw.

---

## Available tools

<!-- mcp:tools:start -->
Tool count: 20.

- `get_word_of_the_day` — Returns today's vocabulary Word of the Day, optionally scoped to a test family.
- `get_definition` (widget-aware) — Look up the definition, part of speech, example sentence, and synonyms/antonyms for a word.
- `generate_quiz` (widget-aware) — Generate a multiple-choice vocabulary quiz for a test family (1–10 questions).
- `get_course_word_list` — Get a sample of vocabulary words from a specific Vocab Voyage course.
- `list_courses` — Lists all 13 Vocab Voyage courses with their slugs and descriptions.
- `explain_word_in_context` — Explain what a word means inside a specific sentence.
- `study_plan_preview` (widget-aware) — Returns a sample 7-day study plan (5 words/day) for a given test family.
- `get_flashcards` (widget-aware) — Returns a tap-to-flip flashcard deck. Per-card answers persist via record_word_result.
- `get_my_progress` (widget-aware) — Auth-only personal dashboard: streak, XP, mastery split, next-up words, recent misses.
- `play_game` — Launches one of 11 vocabulary mini-games (word_match, spelling_bee, speed_round, synonym_showdown, word_scramble, fill_in_blank, context_clues, word_guess, picture_match, crossword, word_search). Per-answer events flow to record_word_result; round XP via award_game_xp.
- `get_sparkle_guidance` (widget-aware) — Lifecycle-aware coaching: returns a phase-appropriate greeting (16 phases) and a recommended next tool/action. Renders the session-debrief widget when relevant.
- `set_persona` — Switch agent bias between student, parent, tutor, or explorer.
- `get_recommended_next_action` — Returns a one-line recommendation for what the user should do next.
- `list_starter_prompts` — Lists the 6 MCP prompts (vocab_kickoff, test_prep_quiz, session_debrief, …) for hosts that don't surface prompts/list.
- `record_word_result` — Auth: log a per-card answer (correct or incorrect).
- `record_session_complete` — Auth: log session totals and award XP.
- `award_game_xp` — Auth: grant bonus XP from a completed mini-game round.
- `mark_word_known` — Auth: add a word to the user's queue or mastered list.
- `mark_word_difficult` — Auth: flag a word as needing more review.
- `update_adaptive_level` — Auth: adjust the user's adaptive difficulty floor/ceiling.
<!-- mcp:tools:end -->

## Interactive widgets

On hosts that support `text/html;profile=mcp-app` (Claude Desktop, ChatGPT Apps SDK, OpenClaw recent builds), Vocab Voyage tools render as embedded UI widgets — taps inside the widget call back into MCP tools and persist to the same tables as the web app.

Example prompt that triggers the flashcards widget:

> "Open the Vocab Voyage flashcards widget and quiz me on 10 SAT words I haven't seen before."

<!-- mcp:widgets:start -->
Widget count: 17.

- `ui://vocab-voyage/word-of-the-day` — Word of the Day (learn, 560x360) via `get_word_of_the_day`
- `ui://vocab-voyage/flashcards` — Flashcards (learn, 560x460) via `get_flashcards`
- `ui://vocab-voyage/quiz` — Quiz (learn, 560x520) via `generate_quiz`
- `ui://vocab-voyage/study-plan` — Study Plan (learn, 600x600) via `study_plan_preview`
- `ui://vocab-voyage/progress` — My Progress (progress, 600x640) via `get_my_progress`
- `ui://vocab-voyage/game/word_match` — Game · Word Match (play, 620x640) via `play_game`
- `ui://vocab-voyage/game/spelling_bee` — Game · Spelling Bee (play, 560x580) via `play_game`
- `ui://vocab-voyage/game/speed_round` — Game · Speed Round (play, 560x600) via `play_game`
- `ui://vocab-voyage/game/synonym_showdown` — Game · Synonym Showdown (play, 560x580) via `play_game`
- `ui://vocab-voyage/game/word_scramble` — Game · Word Scramble (play, 560x580) via `play_game`
- `ui://vocab-voyage/game/fill_in_blank` — Game · Fill in the Blank (play, 560x600) via `play_game`
- `ui://vocab-voyage/game/context_clues` — Game · Context Clues (play, 600x620) via `play_game`
- `ui://vocab-voyage/game/word_guess` — Game · Word Guess (play, 560x600) via `play_game`
- `ui://vocab-voyage/game/picture_match` — Game · Picture Match (play, 600x620) via `play_game`
- `ui://vocab-voyage/game/crossword` — Game · Crossword (play, 640x720) via `play_game`
- `ui://vocab-voyage/game/word_search` — Game · Word Search (play, 640x720) via `play_game`
- `ui://vocab-voyage/session-debrief` — Session Debrief (coach, 600x640) via `get_sparkle_guidance`
<!-- mcp:widgets:end -->

---

## Example prompts

### Word of the Day

- "What's today's SAT word of the day?"
- "Give me an ISEE word of the day with an example sentence I'd hear in 7th grade."
- "Show me today's GRE word of the day and use it in a science context."

### Quiz

- "Quiz me on 5 SAT vocabulary words."
- "Generate a 10-question GRE vocab quiz, then grade my answers as I go."
- "Give me a 5-question SSAT Upper Level quiz and explain every wrong answer."

### Mixed workflows

- "Define 'aberrant' and then quiz me on 3 similar SAT words."
- "Build me a 7-day SSAT study plan and start with today's word."
- "List the LSAT courses, sample 10 words from the hardest one, and quiz me on them."

---

## Optional auth (personalized tools)

Sign in at <https://vocab.voyage/mcp>, generate a personal MCP token (begins with `vv_mcp_`), and pass it as a bearer token. OpenClaw will forward it to authenticated tools that need your study queue or progress data.

```
Authorization: Bearer vv_mcp_YOUR_TOKEN
```

Token scopes: `mcp.read`, `mcp.tools`, `profile.read`, `progress.read`. See <https://vocab.voyage/developers/auth> for the full reference.

---

## Troubleshooting

- **Skill not appearing** — restart OpenClaw and re-run `openclaw skills list`. Confirm the file is at `~/.openclaw/skills/vocab-voyage/SKILL.md` (not nested in a subfolder).
- **`rate_limited` errors** — anonymous calls are capped at 60/min per IP. Authenticated tokens raise the cap to 600/hour. Honor the `Retry-After` header.
- **`unauthorized` errors on a personalized tool** — the tool requires a `vv_mcp_` token. Generate one at <https://vocab.voyage/mcp>.
- **`insufficient_scope` errors** — re-issue the token and include the scope listed in the `required_scopes` array of the error.
- **Server unreachable** — check <https://vocab.voyage/status> for live operational guidance.

---

## Links

- Install hub: <https://vocab.voyage/mcp>
- Auth & scopes: <https://vocab.voyage/developers/auth>
- Developer docs: <https://vocab.voyage/developers>
- Status: <https://vocab.voyage/status>
- ClawHub listing: <https://clawhub.ai/jaideepdhanoa/vocab-voyage-mcp>