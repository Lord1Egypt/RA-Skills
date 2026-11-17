## Description:

Voc namespace for Netsnek e.U. vocabulary and language learning tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

External learners and developers use Voc to reserve and invoke a vocabulary-learning namespace that currently returns brand, deck, and stats placeholder information while future flashcard and spaced-repetition functionality is planned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing language may cause the skill to be invoked for vocabulary-related requests when the user expected a general answer.

Mitigation: Invoke Voc explicitly or confirm before running its helper commands when tighter control is needed.

Risk: The skill requires exec permission to run helper scripts.

Mitigation: Review the helper script output and permissions before deployment; current evidence says the scripts only print placeholder information.

Risk: License signals conflict between the manifest and script output.

Mitigation: Confirm the authoritative release terms before publishing or redistributing the skill.

## Reference(s):

- [Voc ClawHub Page](https://clawhub.ai/kleberbaum/skills/voc)
- [Netsnek Website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text responses with optional shell command output and JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts currently print brand, deck, and stats placeholder information.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
