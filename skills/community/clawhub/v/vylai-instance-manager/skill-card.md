## Description:

Manages Vylai GPU cloud platform instances by helping agents create GPU containers, query instance status, list GPU and application options, and delete resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckiehao](https://clawhub.ai/user/luckiehao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Vylai GPU cloud workloads from an agent session, including creating containers, checking status, finding app IDs and GPU types, and cleaning up instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete authenticated Vylai cloud instances immediately by task_id or deploy_name.

Mitigation: Require explicit human confirmation before running delete_instance.py, and query the target instance first to verify the intended task_id or deploy_name.

Risk: An autonomous agent with access to the Vylai token can act against the user's cloud account and consume account balance.

Mitigation: Use only a Vylai token and account balance whose permissions and spending exposure are acceptable for the agent session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckiehao/skills/vylai-instance-manager)
- [Vylai platform](https://vylai.com)
- [Vylai API token console](https://vylai.com/console/api)
- [API reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; scripts return JSON responses from Vylai APIs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Vylai API token in the environment for authenticated create, query, GPU listing, and delete operations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
