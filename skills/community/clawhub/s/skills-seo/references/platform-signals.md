# Platform Signals

Use this file when auditing discovery across public skill directories.

These notes are working heuristics, not contractual guarantees from the platforms. Use them to guide prioritization, and clearly label any inference or uncertainty in the final report.

## ClawHub

Treat ClawHub as a semantic search and browse platform.

- Retrieval: vector search over skill text and metadata.
- Extra boosts: exact or prefix matches on slug and display name.
- Ranking modifiers: popularity and download signals.
- Browse surfaces: highlighted, newest, recently updated, downloads, installs, stars.

What to optimize:

- Folder slug and public name should contain the exact task phrase users search for.
- `description` should cover the job, object, user intent, and common synonyms.
- The first visible section of `SKILL.md` should include realistic example prompts.
- Update the skill periodically if the platform rewards freshness.
- Encourage legitimate installs, stars, and external references; those can influence ranking and click confidence.

## skills.sh

Treat skills.sh as a leaderboard and listing-conversion platform.

- Public signals: installs, stars, repository source, and trust or security cues.
- Discovery: leaderboard exposure plus listing click-through.
- Practical effect: users often discover via ranking pages rather than deep semantic search.

What to optimize:

- Make the one-line description immediately understandable on list pages.
- Improve click-through with a concrete title, problem-oriented summary, and trust signals.
- Reduce friction to install or evaluate the skill.
- Add visible proof that the skill is maintained and specific, not template noise.

## Shared Rules

- Use searchable nouns and verbs in names and descriptions.
- Cover synonyms, alternate phrasings, abbreviations, and adjacent task language.
- Put high-value intent words near the start of the description.
- Include at least 3 realistic example prompts if the task space is broad.
- Prefer sharp positioning over broad claims.
- Avoid misleading keyword stuffing; retrieval quality drops if the body and examples do not support the terms.
