## Description:

Team Discuss helps agents run structured multi-round discussions with dialectic analysis, randomized or rotated speaking order, shared state, and optional sub-agent participation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chyher](https://clawhub.ai/user/chyher)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to coordinate multi-perspective discussions for technology choices, architecture reviews, product decisions, policy analysis, and other topics that benefit from structured debate and consensus tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discussion content can be saved in local files.

Mitigation: Review the configured storage path and file permissions before using the skill with private or regulated information.

Risk: Configured discussions may send prompts and prior messages to participating sub-agents.

Mitigation: Avoid secrets, private customer data, legal details, medical details, or other regulated information unless the agent trust boundaries have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chyher/skills/team-discuss)
- [Publisher profile](https://clawhub.ai/user/chyher)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Quick start demo discussion](artifact/discussions/quick-start-demo.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with Python and shell snippets, plus local JSON discussion records when examples are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include discussion status, round summaries, consensus level, dialectic quality signals, and persisted local transcript data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
