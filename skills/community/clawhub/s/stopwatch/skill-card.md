## Description:

Advertised for stopwatch, timer, and lap tracking workflows, this release's artifacts implement a Bash-based local logging, search, stats, and export utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and command-line users can use the artifacts as a local timestamped logging utility with recent-history, search, statistics, and export commands. Review it as a logging tool rather than a stopwatch, timer, lap tracker, or countdown utility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised stopwatch, timer, lap, and countdown behavior does not match the persistent logging behavior described by the release security evidence.

Mitigation: Evaluate and deploy it only as a local logging and record-search utility; choose a different skill if stopwatch or countdown behavior is required.

Risk: Command arguments are retained in local log files and can later be exported or searched.

Mitigation: Do not enter secrets or sensitive notes, and review or clear ~/.local/share/stopwatch before sharing a system or exporting records.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ckchzh/skills/stopwatch)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, JSON, configuration]

**Output Format:** [Plain text CLI output, with optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local log and export files under ~/.local/share/stopwatch.]

## Skill Version(s):

2.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
