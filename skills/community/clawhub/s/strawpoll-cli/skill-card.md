## Description:

Create and manage StrawPoll polls, meeting polls, and ranking polls from the terminal using the strawpoll CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dedene](https://clawhub.ai/user/dedene)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and automation agents use this skill to create, inspect, update, delete, and report on StrawPoll multiple-choice, meeting, and ranking polls from a terminal or scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation examples use an upstream CLI package that may change over time.

Mitigation: Install only from a trusted upstream and prefer a pinned, reviewed version when available.

Risk: The skill requires access to a StrawPoll API key and can manage polls in the associated account.

Mitigation: Keep the API key scoped as narrowly as StrawPoll allows and avoid exposing it in logs, shared shells, or committed configuration.

Risk: Force delete and reset examples can remove or clear poll data without a confirmation prompt.

Mitigation: Confirm the exact poll ID before destructive commands and avoid --force unless the deletion or reset is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dedene/skills/strawpoll-cli)
- [Publisher profile](https://clawhub.ai/user/dedene)
- [strawpoll-cli homepage](https://github.com/dedene/strawpoll-cli)
- [StrawPoll](https://strawpoll.com/)
- [StrawPoll account settings](https://strawpoll.com/account/settings)
- [strawpoll-cli flag reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and CLI flag references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for human-readable, JSON, and TSV strawpoll output modes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
