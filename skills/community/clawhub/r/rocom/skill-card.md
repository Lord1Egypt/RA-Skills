## Description:

Roco Kingdom World offline data tool. Local JSON queries for pets, skills, and items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imnotriv3r](https://clawhub.ai/user/imnotriv3r)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Roco Kingdom:World reference questions with local data for pets, skills, items, dungeons, regions, marks, natures, quests, and formations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled game reference data can become stale or differ from the live game.

Mitigation: Check the bundled data sync timestamp and validate time-sensitive gameplay recommendations against current game sources.

Risk: The artifact identifies Bilibili WIKI as the game data source with CC BY-NC-SA 4.0 terms, which may impose obligations separate from the release package license.

Mitigation: Review source-data terms before redistributing the bundled data or using it in contexts with license restrictions.

## Reference(s):

- [Rocom ClawHub skill page](https://clawhub.ai/imnotriv3r/skills/rocom)
- [Data Manifest](MANIFEST.md)
- [Game Knowledge Reference](references/game-knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text from local JSON lookups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and reads bundled static JSON data locally.]

## Skill Version(s):

1.5.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
