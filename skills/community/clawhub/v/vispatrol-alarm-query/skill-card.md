## Description:

Queries VisPatrol alarm records and matching snapshots on trusted Windows hosts after the user approves access to the local %TEMP%/vpup.json session file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baymax1957](https://clawhub.ai/user/baymax1957)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators responsible for trusted Windows VisPatrol deployments use this skill to query alarm records, retrieve matching snapshots, and generate concise alarm reports after approving access to the local vpup.json session file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a local VisPatrol session token and surveillance snapshots.

Mitigation: Install only on a trusted Windows VisPatrol host, confirm vpup.json is expected, require explicit user approval for each query, and use the token only for read-only alarm and snapshot retrieval.

Risk: Network boundaries depend on the VisPatrol service endpoints declared in vpup.json.

Mitigation: Use only local or otherwise protected VisPatrol services and review the configured endpoints before installing or running the skill.

Risk: The security evidence notes weak enforcement and reliance on user or agent discipline for approval boundaries.

Mitigation: Keep the OpenClaw approval gate enabled and harden approval enforcement before use in environments with network attackers, untrusted service responses, or strict image-retention rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baymax1957/skills/vispatrol-alarm-query)
- [Publisher profile](https://clawhub.ai/user/baymax1957)
- [Security boundary](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown alarm report with JSON-derived snapshot attachment metadata and optional local snapshot image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured query parameters and should report only alarm and snapshot fields returned by the script.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
