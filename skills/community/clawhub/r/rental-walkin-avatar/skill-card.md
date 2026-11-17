## Description:

Turn seller-supplied floor-plan facts, authored walk-in lines, and authorized stills into short talking clips for rental listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate sellers, listing teams, and their agents use this skill to plan and generate one walk-in talking clip per authorized still from confirmed room facts and prewritten lines. It supports staged approval for voice cloning, speech synthesis, and image-to-video generation before paid work is submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package uses a shared broad Beatra account token.

Mitigation: Install only when that account access is acceptable, keep the credential private, and review Beatra account permissions and revocation options before use.

Risk: The package can perform paid Beatra operations after agent-mediated approval.

Mitigation: Review each clone, speech, and video approval card, confirm live pricing and balance before submission, and rely on request identities to avoid duplicate paid work during recovery.

Risk: The bundled client silently self-updates package code by default.

Mitigation: Review the automatic update behavior and disable silent checks with `python3 scripts/mcp_client.py update --auto off` when manual update control is required.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/rental-walkin-avatar)
- [Beatra skill page](https://beatra.ai/skills/rental-walkin-avatar)
- [Walk-in talking-clip workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [MCP connection](artifact/references/mcp-connection.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and generated media file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces separate 2 to 15 second clips when source assets, rights, balance, and paid generation stages are approved.]

## Skill Version(s):

0.1.2 (source: server release and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
