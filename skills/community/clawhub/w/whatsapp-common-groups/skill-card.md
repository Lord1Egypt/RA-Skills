## Description:

Find groups shared between contacts and check group membership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Users who manage a local OpenClaw WhatsApp state use this skill to find group memberships for a contact, verify whether a phone number is in a group, or enumerate known group members.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private WhatsApp group and contact relationship data from local credential-state files.

Mitigation: Install and run it only where the operator is authorized to inspect that local WhatsApp state, and review results before sharing them.

Risk: The bulk all-members command can enumerate private contact metadata across groups.

Mitigation: Prefer targeted find and check commands; use all-members only when bulk enumeration is explicitly intended and keep result limits narrow.

Risk: Weak scoping can cause the skill to inspect more local WhatsApp state than intended.

Mitigation: Run it with a deliberately scoped OPENCLAW_STATE_DIR and restrict access to credential-state directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcosrippel/skills/whatsapp-common-groups)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON printed by command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include phone numbers, group identifiers, group names, membership status, and aggregate group counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
