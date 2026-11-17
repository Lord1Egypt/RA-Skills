## Description:

Undercover Is Who helps an agent act as the judge for the Chinese "Who Is Undercover" party game by assigning words, hosting description and voting phases, tallying votes, deciding wins, and producing a final recap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loongfay](https://clawhub.ai/user/loongfay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and game hosts use this skill to run a structured "Who Is Undercover" game in Chinese-speaking groups, with the agent managing hidden roles, player descriptions, private voting, eliminations, and end-of-game review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores player names, message-sender IDs, roles, words, descriptions, votes, and game reviews in a local SQLite game record.

Mitigation: Use it only with groups that consent to local game records, avoid exporting records before the game ends, and delete the generated database when records are no longer needed.

Risk: Premature disclosure of roles, secret words, or vote details can compromise game integrity.

Mitigation: Follow the scripted status checks, generated private messages, and public progress messages so hidden role and vote information is revealed only at the intended game stage.

## Reference(s):

- [Word Pair Library](references/word_pairs.md)
- [ClawHub Skill Page](https://clawhub.ai/loongfay/skills/undercover-is-who)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and text with JSON command outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local game state and can export a Markdown game record.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
