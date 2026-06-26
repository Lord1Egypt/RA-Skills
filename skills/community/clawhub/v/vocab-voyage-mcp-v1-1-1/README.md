# Vocab Voyage MCP Server

The official public mirror of the [Vocab Voyage](https://vocab.voyage) Model Context Protocol server — **20 tools + 17 interactive widgets** for vocabulary learning and standardized test prep (ISEE, SSAT, SAT, PSAT, GRE, GMAT, LSAT).

- 20 MCP tools (including flashcards, 11 mini-games, progress tracking, and Sparkle coaching)
- 17 interactive widgets (quiz, flashcards, study plan, progress dashboard, session debrief, and more)
- Hosted — no install required
- Optional personal tokens for personalized features

- 🔗 Server URL: `https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server`
- 📚 Browse tools: <https://vocab.voyage/mcp/tools>
- 🛠 Auth & scopes: <https://vocab.voyage/developers/auth>
- 🪪 License: MIT

## Install

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vocab-voyage": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server"]
    }
  }
}
```

### ChatGPT Apps SDK / Cursor / Cline

Add a custom remote MCP server with the URL above and (optionally) a
`Bearer vv_mcp_…` token generated from
<https://vocab.voyage/developers/auth>.

### OpenClaw

```bash
openclaw skills install vocab-voyage
```

## Tools

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

## Widgets

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

## Examples

- [`examples/curl-quiz.sh`](./examples/curl-quiz.sh) — generate a 5-question SAT quiz with `curl`
- [`examples/node-flashcards.mjs`](./examples/node-flashcards.mjs) — fetch a flashcard deck from Node 18+
- [`examples/python-progress.py`](./examples/python-progress.py) — call the auth-only `get_my_progress` tool from Python

## Manifests

The discovery + directory submission files live flat at the repo root so MCP
directories can `git clone` and link straight to them:

- `server-card.json` — MCP server card (canonical)
- `apps.json` — interactive widget catalog
- `agent-card.json` — A2A agent card
- `mcp.json` — MCP discovery doc
- `server.json` — MCP Registry submission manifest
- `smithery.yaml` — Smithery directory listing
- `clawhub.json` — ClawHub directory listing
- `SKILL.md` — OpenClaw skill descriptor
- `SUBMISSION_LINKS.md` — canonical `?ref=` slug list + Friday attribution query

All of the above are regenerated on every release by
`scripts/build-mcp-repo.mjs` upstream — do not hand-edit them here.

## Sync

This repository is automatically refreshed from the upstream Vocab Voyage
codebase. See [`.github/workflows/sync.yml`](./.github/workflows/sync.yml)
for the contract. PRs that change manifests will be closed and applied
upstream instead.

## License

[MIT](./LICENSE) © Vocab Voyage