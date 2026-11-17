## Description:

Find the best cross-timezone meeting windows with DST-safe conversion and ranked output (Optimal, Stretch, Avoid). Use when users ask for overlap windows across 2+ cities/timezones, want results anchored to one timezone, or need Telegram-friendly scheduling output with 24h + 12h time formats and +1 day markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeadland](https://clawhub.ai/user/jeadland)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to find ranked meeting windows across two or more cities or IANA timezones, with results anchored to a chosen timezone. It is suited for producing decision-ready scheduling output with local times, next-day markers, and reasons for less comfortable windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid numeric values for meeting duration, slot step, or result count can hang the local meeting-window script.

Mitigation: Use positive values for --duration, --step, and --top until input validation is added.

Risk: The skill can save a user's timezone, preferred meeting hours, and flexibility settings in its disclosed local OpenClaw config file.

Mitigation: Confirm setup or update requests before changing settings, and install only when this local settings storage is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style scheduling recommendations with optional shell commands and local JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs ranked Optimal, Stretch, and Avoid sections with 24-hour and 12-hour times, participant local times, +1 day markers, and reasons for Stretch or Avoid windows.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
