## Description:

Supports setup and day-to-day inventory management in a user-hosted XianMu IMS instance through MCP or REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaokingsoft](https://clawhub.ai/user/miaokingsoft)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to connect an agent to a self-hosted XianMu IMS instance for inventory setup, stock movements, audits, alerts, and related records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guide encourages approving security prompts without verifying what is being authorized.

Mitigation: Verify the installer source and checksum, publisher, MCP address, and requested action before approving; use the lowest required IMS permissions and protect the API token.

Risk: Document deletion is permanent.

Mitigation: Confirm the target and user intent before deleting a document.

## Reference(s):

- [XianMu IMS API reference](references/api.md)
- [XianMu IMS onboarding guide](references/onboarding.md)
- [XianMu IMS setup guide](references/setup.md)
- [XianMu IMS deployment documentation](https://ims.miaoking.com/docs/deploy.html)
- [XianMu IMS API documentation](https://ims.miaoking.com/docs/api.html)
- [GitHub source provenance](https://github.com/miaokingsoft/XianMuIMS/tree/main/skill/xianmu-ims)
- [ClawHub skill release](https://clawhub.ai/miaokingsoft/skills/xianmu-ims)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Natural language, API requests, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for operating a user-provided IMS instance; write actions require user confirmation as described in the skill.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
