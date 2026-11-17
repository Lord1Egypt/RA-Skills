## Description:

Trend is a local command-line content toolkit that records drafts, edits, optimization notes, schedules, hashtags, hooks, calls to action, rewrites, translations, tone notes, headlines, and outlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use Trend to capture content workflow notes from a local shell, then review, search, summarize, and export those logs. The release should be reviewed before use because server security evidence identifies it as a persistent local content logger rather than a true trend, sentiment, popularity, or alerting tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs are persistently stored under ~/.local/share/trend and may be included in exported JSON, CSV, or TXT files.

Mitigation: Avoid entering confidential drafts or sensitive content unless local storage and export handling are acceptable.

Risk: CSV exports may contain user-provided text that can be risky when opened in spreadsheet software.

Mitigation: Review exported CSV content before opening it in spreadsheet tools or sharing it downstream.

## Reference(s):

- [ClawHub Trend skill page](https://clawhub.ai/xueyetianya/skills/trend)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text shell output with local JSON, CSV, and TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores command inputs and generated exports under ~/.local/share/trend.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
