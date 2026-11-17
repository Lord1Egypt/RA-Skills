# Regular project review

A tidy-up pass through the whole app, done on purpose, when there is spare Claude allowance. It is not for when a deadline is near.

## Warn first

A review uses a lot of the student's Claude Pro allowance (it reads the whole project). Run it when they have room, not right before they need Claude for something else. One area per session, never everything at once.

## How to run one

1. Ask which area. Recommend the one not done longest:
   - **Tests:** what logic has no test? Add tests for the important gaps (sign-in, payments, data rules first).
   - **Structure:** files that grew too big, code in the wrong folder, confusing names.
   - **Duplicates:** the same logic written two or three times.
   - **AI slop:** dead code, comments that repeat the code, made-up helpers nobody calls, over-careful checks for cases that cannot happen.
   - **Security:** every table has privacy rules and an entry in `supabase/isolation.json`, every API route checks who is calling, no key in the browser, dependencies up to date. Run `verify.mjs <appDir>` first.
2. Use your strongest model for judgement: what is a real problem, what is a risk, what to fix first. You may use helper agents one model cheaper for mechanical work only: listing files, counting, finding duplicates, running the test suite. Their results are leads to check, not answers.
3. Write the findings as a short list ordered by what matters for users. Show it. Ask which to do.
4. Do the chosen ones as small pull requests, one theme each, on branches. Each has tests, green checks, and a plain-English description. Risky areas follow `automerge.md` and wait for the student.
5. Never mass-rewrite. If something needs a big change, describe it and plan it as its own feature.
6. Finish with: what was found, what was fixed, what was left on purpose, what to look at next time.

## How often

Roughly monthly for an app with real users, or before a big launch step (taking payments, opening sign-ups). For the whole app at once (before a big release, or after another agent added a lot of code), the review skill (`/shipyard:review`) covers every area with helper agents and reviews its own fixes; it uses much more of the plan. A lighter option: ask Claude to review just the last month's merged pull requests.

## Scheduling

If the student's Claude plan offers scheduled tasks in the desktop app, they can set a monthly reminder to run this. Do not promise it exists; check what their plan shows. A calendar reminder works everywhere.
