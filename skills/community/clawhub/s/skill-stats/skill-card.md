## Description:

Query, analyze, and track skill usage information across Claude Code and OpenClaw, including call counts, success rates, last used times, redundant installations, duplicates, and available skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-306](https://clawhub.ai/user/leo-306)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect skill usage across Claude Code and OpenClaw environments, identify unused or low-value skills, and review call frequency, success rate, and recency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans broad local Claude Code and OpenClaw session histories.

Mitigation: Run it only in environments whose session histories you intend to analyze.

Risk: The skill persists behavioral metadata, including project paths, in local statistics files.

Mitigation: Review the retained data and clear or disable stored statistics when they are no longer needed.

Risk: The skill runs through an unpinned npm executable.

Mitigation: Prefer a release that pins tsx or run it in a controlled local environment with trusted package resolution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with command output tables and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with a required claude-code or openclaw context argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
