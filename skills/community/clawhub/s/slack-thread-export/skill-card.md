## Description:

Exports Slack thread messages from a logged-in Slack web tab into CSV or JSONL using an attached Chrome Browser Relay tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devdha](https://clawhub.ai/user/devdha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to export Slack thread activity from an authorized logged-in browser session by user, channel, or date range into reusable CSV/JSONL archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk export from a logged-in Slack session can expose sensitive workspace data.

Mitigation: Use only when authorized to export the relevant workspace data, keep user/channel/date scope narrow, and treat all CSV/JSONL outputs as sensitive.

Risk: Unsafe browser JavaScript construction in the authenticated page context can be risky with untrusted channel lists.

Mitigation: Avoid untrusted channel inputs until the publisher fixes JavaScript interpolation; prefer explicit, reviewed channel lists.

Risk: CSV exports can be unsafe to share if message text is not protected against spreadsheet formula handling.

Mitigation: Review exported CSVs before sharing and require the publisher to fix CSV formula handling for shared exports.

Risk: Broad Slack searches can be rate limited, time out, or produce partial exports.

Mitigation: Run preflight checks, split exports by channel and date range, and retry only failed channels using saved raw output.

## Reference(s):

- [Slack thread export notes](references/notes.md)
- [ClawHub skill page](https://clawhub.ai/devdha/skills/slack-thread-export)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; scripts can produce CSV, JSONL, failed-channel lists, and summary JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Slack export outputs can contain sensitive workspace data and should be handled according to the user's authorization and retention requirements.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
