## Description:

Connects an agent to OKKI CRM so it can query customers, create follow-up records, manage orders, and keep activity limited to the configured OKKI channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

CRM operators and support or sales agents use this skill to retrieve OKKI customer, product, lead, follow-up, user, and order information, and to perform CRM write actions with confirmation based on operation risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write CRM data, including creating leads, companies, follow-up records, orders, and emails.

Mitigation: Use the documented risk tiers: execute read-only actions directly, require first-use confirmation for medium-risk actions, and require confirmation every time for high-risk write or email actions.

Risk: CRM commands may trigger outside the intended OKKI workflow if channel gating or keyword triggers are configured incorrectly.

Mitigation: Confirm that execution is limited to the configured #okki channel and narrow or remove broad keyword triggers before deployment.

Risk: Authentication and live CRM behavior depend on an external OKKI client and token storage that are not bundled in the artifact.

Mitigation: Review the external OKKI client, configuration path, and token cache handling before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cjboy007/skills/ssa-okki-crm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and concise text with optional shell commands or Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer and user IDs should be withheld from normal customer-facing output according to the skill instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
