## Description:

Interact with Snipe-IT asset management via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bivex](https://clawhub.ai/user/bivex)

### License/Terms of Use:


## Use Case:

IT administrators and developers use this skill to produce Snipe-IT REST API shell commands for managing inventory assets, users, licenses, accessories, consumables, components, locations, departments, reports, and related records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce commands for POST, PATCH, PUT, DELETE, checkout, checkin, restore, backup download, and user deactivation actions against Snipe-IT records.

Mitigation: Require explicit approval before state-changing or backup-download commands and review generated request payloads before execution.

Risk: A broad Snipe-IT API token can modify or delete inventory and user records beyond the intended task.

Mitigation: Use a least-privileged API token for the target Snipe-IT instance and rotate it if it is exposed.

Risk: Using an untrusted Snipe-IT URL can expose API tokens and inventory data.

Mitigation: Use only a trusted HTTPS Snipe-IT URL and avoid placing tokens in shared logs, tickets, or prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bivex/skills/snipeit-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks and environment variable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SNIPEIT_URL, SNIPEIT_API_TOKEN, curl, and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
