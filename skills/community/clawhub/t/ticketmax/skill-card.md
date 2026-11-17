## Description:

Print markdown files to an ESC/POS thermal receipt printer over TCP, USB, or serial. Supports headings, bold, underline, tables, images, QR codes, paper cuts, and buzzer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yatesdr](https://clawhub.ai/user/yatesdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have agents prepare Markdown receipts, reports, alerts, and shift summaries that can be printed on ESC/POS thermal receipt printers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Go package with @latest can pull an unreviewed future release.

Mitigation: Pin a reviewed ticketmax version for controlled deployments.

Risk: An incorrect PRINTER_ADDR or -addr value can send output to the wrong printer or device.

Mitigation: Confirm the printer address and run a connectivity or test print before production use.

Risk: Agent-generated or externally supplied Markdown can trigger physical effects such as paper cuts and buzzer sounds.

Mitigation: Review Markdown before printing, especially content containing cut or beep comments.

## Reference(s):

- [Ticketmax homepage](https://github.com/yatesdr/ticketmax)
- [Ticketmax ClawHub skill page](https://clawhub.ai/yatesdr/skills/ticketmax)
- [Publisher profile](https://clawhub.ai/user/yatesdr)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and printer-oriented markup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated Markdown may include QR blocks, image references, paper-cut comments, and buzzer comments for physical printer output.]

## Skill Version(s):

0.1.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
