## Description:

Creates loopable talking-avatar clips for a shop’s welcome, product, FAQ, and closing segments from an authorized portrait and approved speech or scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External shop operators use this skill to create labeled overnight loop clips from an authorized likeness, voice, portrait, and short scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization exceeds avatar-creation needs, and the shared Beatra connection can remain reusable until expiry or console revocation.

Mitigation: Prefer a release with narrower permissions and revoke the shared connection from the Beatra Console when it is no longer needed.

Risk: Uninstall handling may disconnect other Beatra skills that share the connection.

Mitigation: Avoid uninstalling while other Beatra skills are in use and prefer a release with corrected uninstall handling.

Risk: Selected media is sent to Beatra, approved generation consumes credits, and installation analytics are automatic.

Mitigation: Submit only authorized media, review the live admission and cost details before generation, and account for automatic installation analytics.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/unattended-live-avatar)
- [Beatra skill page](https://beatra.ai/skills/unattended-live-avatar)
- [Unattended live avatar workflow](references/workflow.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)

## Skill Output:

**Output Type(s):** [Video, Audio, Text]

**Output Format:** [Loopable talking-avatar video clips with concise delivery details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Welcome, product, FAQ, and close clips; delivery details include actual clip facts and credit usage.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
