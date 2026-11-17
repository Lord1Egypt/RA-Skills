## Description:

Turn user-supplied open windows into a four-to-eight still wealth open calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to plan and generate a pack of still images that present user-supplied fund open windows, with one calendar still per named window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a shared Beatra device credential with broad media, artifact, task, and spending-related authority.

Mitigation: Review the Beatra approval page before allowing access and revoke the device in the Beatra Console when the installation is no longer trusted.

Risk: The bundled client can silently self-update package code.

Mitigation: Disable automatic updates with the documented update command when review-before-update control is required.

Risk: Billable image generation can consume Beatra credits for each approved calendar still.

Mitigation: Confirm the live model price and one paid call per window before generation, then report the returned net charged credits.

Risk: Generated calendar stills can contain unreadable or incorrect small text and are not certified financial guidance.

Mitigation: Review visible text against the confirmed pack list and treat uncertain text as a correction item before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/wealth-open-cal-set)
- [Beatra skill homepage](https://beatra.ai/skills/wealth-open-cal-set)
- [Wealth open calendar pack workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and shell command snippets, plus generated image artifacts from Beatra tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one still image per approved open window, capped at eight stills; reports task IDs, dimensions, formats, resolved models, and net charged credits.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
