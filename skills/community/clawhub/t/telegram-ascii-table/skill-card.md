## Description:

Format tabular data as ASCII box tables for Telegram. Stdin-only input eliminates shell injection risks. Handles smart column sizing, text wrapping, and proper padding for monospace display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nalg](https://clawhub.ai/user/nalg)

### License/Terms of Use:


## Use Case:

Developers, operators, and support teams use this skill to turn pipe-delimited stdin data into monospace tables suitable for Telegram messages. It is useful for sharing compact status, task, or inventory data in desktop or mobile-friendly table layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input provided through stdin is printed back as table output, so sensitive data can be exposed if copied into Telegram or retained in terminal logs.

Mitigation: Use only data approved for the target chat and review the rendered table before sharing it.

Risk: The packaged script may not be directly executable in every environment.

Mitigation: Run it with python3 or set executable permissions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nalg/skills/telegram-ascii-table)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text ASCII or Unicode table output, commonly wrapped in Markdown code blocks for Telegram]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads pipe-delimited rows from stdin; supports desktop, mobile, and custom-width output modes.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
