## Description:

Turn seller-supplied sales voicemail scripts into one spoken voicemail clip per labeled slot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and sales teams use this skill to turn already-written voicemail copy into labeled callback, after-hours, follow-up, and related voicemail clips for import into a phone system or dialer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra device token can spend credits and access capabilities beyond voicemail generation.

Mitigation: Install only when that access is acceptable, keep the credential private, and revoke or disconnect the device when Beatra access is no longer needed.

Risk: Automatic updates are enabled by default and can replace package-owned files after verification.

Mitigation: Disable automatic updates with the documented update command when manual review is required before replacement.

Risk: Voice cloning and voice sample upload can expose sensitive likeness data.

Mitigation: Upload only authorized voice samples after confirming likeness rights and trust in the Beatra service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/sales-voicemail-pack)
- [Beatra skill homepage](https://beatra.ai/skills/sales-voicemail-pack)
- [Sales voicemail workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; generated Beatra tasks return audio artifact metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill plans labeled voicemail slots before paid generation and uses per-request identities for clone and speech task recovery.]

## Skill Version(s):

0.1.2 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
