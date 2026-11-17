## Description:

Score helps agents record game scores, rankings, leaderboards, history, and related activity in local plaintext logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Score to record game or competition activity from the command line, review recent entries, search local logs, and export saved records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local logs can contain sensitive personal details if users enter them.

Mitigation: Record only non-sensitive game and activity data; do not store secrets or sensitive personal information.

Risk: Exports can gather all saved entries into a single file.

Mitigation: Review exported json, csv, or txt files before sharing and remove exports when they are no longer needed.

Risk: Analytics are limited to recording, searching, and counting text entries.

Mitigation: Review results before using them as authoritative brackets, rankings, or player statistics.

## Reference(s):

- [Score ClawHub page](https://clawhub.ai/bytesagain3/skills/score)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Plain text CLI output with local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext logs and json, csv, or txt exports under ~/.local/share/score/.]

## Skill Version(s):

2.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
