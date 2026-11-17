## Description:

Guides OpenClaw agents through Ternivo Connect social-media account checks, publishing, scheduling, delivery verification, diagnostics, and engagement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homesteadliving](https://clawhub.ai/user/homesteadliving)

### License/Terms of Use:

MIT-0

## Use Case:

Social-media teams and their OpenClaw agents use this skill to check connected accounts and capabilities, prepare and publish or schedule posts, verify delivery, and investigate failures or engagement activity through Ternivo Connect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing or scheduling from the wrong organization or without the required approval.

Mitigation: Confirm the OAuth workspace and organization approval settings; check account health, capabilities, and preflight status before any write.

Risk: Mistaking provider acceptance for successful public delivery.

Mitigation: Check post status or delivery receipts and report success only after terminal verified delivery.

## Reference(s):

- [Ternivo Social Delivery](https://ternivo.app/social-delivery)
- [Ternivo Connect on ClawHub](https://clawhub.ai/homesteadliving/skills/ternivo-connect)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports delivery as successful only after a verified terminal receipt; provides actionable diagnostics when intervention is needed.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
