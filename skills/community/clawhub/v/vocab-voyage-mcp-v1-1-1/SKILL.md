# Vocab Voyage Vocabulary Prep Skill

Use Vocab Voyage when a user needs standardized test vocabulary practice, definitions, quizzes, course word lists, or a study plan for ISEE, SSAT, SAT, PSAT, GRE, GMAT, LSAT, or academic vocabulary.

## Tools and APIs

- OpenAPI: https://vocab.voyage/openapi.json
- Public API: https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/vocab-api
- MCP: https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server
- Docs: https://vocab.voyage/developers

## Example prompts

- Define “aberrant” and give a test-prep example.
- Generate a 5-question SAT vocabulary quiz.
- List Vocab Voyage courses for ISEE and SSAT.
- Build a 7-day GRE vocabulary study plan preview.

## Interactive widgets

Vocab Voyage's MCP server returns 17 interactive widgets alongside JSON. On hosts that support `text/html;profile=mcp-app` resources (Claude Desktop, ChatGPT Apps SDK, OpenClaw), tools render as embedded UI: word-of-the-day card, flashcards deck, quiz, 7-day study plan, personal progress dashboard, 11 mini-games (word_match, spelling_bee, speed_round, synonym_showdown, word_scramble, fill_in_blank, context_clues, word_guess, picture_match, crossword, word_search), and a session debrief from Sparkle. Taps inside widgets persist to the user's account via `record_word_result`, `record_session_complete`, `mark_word_known`, and `award_game_xp`. Browse the full catalog with deep-link "Start in Claude/ChatGPT" buttons at https://vocab.voyage/mcp/tools. Source: https://github.com/jaideepdhanoa/vocab-voyage-mcp.

Tool count: 20 (7 public vocab, 4 widget-aware, 6 persistence, 3 sparkle-brain). Prompt count: 6 (vocab_kickoff, test_prep_quiz, session_debrief, ...).

## Tool catalog (auto-generated)

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

## Widget catalog (auto-generated)

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

