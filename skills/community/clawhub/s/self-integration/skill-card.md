## Description: <br>
Connects an agent to external services through Membrane so it can create connections, find or build actions, and run API operations such as sending messages, creating tasks, syncing data, or managing records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bratchenko](https://clawhub.ai/user/bratchenko) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent connect to external apps through Membrane, authenticate connections, discover or build actions, and execute requested API operations across business tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act as a broad bridge into connected apps and run high-impact actions. <br>
Mitigation: Install only when this broad Membrane access is intended, use least-privileged Membrane tokens and connected accounts, and scope connected apps narrowly. <br>
Risk: Actions such as creating connections or connectors, posting content, syncing or exporting data, modifying records, or destructive operations may occur without clear built-in confirmation rules. <br>
Mitigation: Require explicit user confirmation before those actions are executed. <br>
Risk: The Membrane token is a high-privilege credential for connected app operations. <br>
Mitigation: Treat MEMBRANE_TOKEN as a secret and avoid exposing it in prompts, logs, generated files, or action inputs. <br>


## Reference(s): <br>
- [Membrane](https://getmembrane.com) <br>
- [Membrane Dashboard](https://console.getmembrane.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/bratchenko/self-integration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON request or response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMBRANE_TOKEN and may use MEMBRANE_API_URL to target the Membrane API.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
