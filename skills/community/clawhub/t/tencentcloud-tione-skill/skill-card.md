## Description:

Tencent Cloud TI-ONE query toolkit for training tasks, online services, notebooks, resource groups, model repositories, datasets, logs, and events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alger-z](https://clawhub.ai/user/alger-z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to inspect Tencent Cloud TI-ONE resources through predefined read-only query scripts and to generate console links for supported resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Cloud credentials are required and could expose cloud account access if reused broadly or shown in responses.

Mitigation: Use dedicated Tencent Cloud credentials limited to read-only TI-ONE Describe permissions, and never display secret values.

Risk: The dependency instructions install tccli without a pinned version.

Mitigation: Install tccli in an isolated environment and pin or verify the package version before exposing cloud credentials.

Risk: Unsupported actions or direct API calls could exceed the skill's intended read-only query scope.

Mitigation: Use only the predefined scripts under artifact/scripts and refuse create, modify, delete, or direct tccli/API workflows.

## Reference(s):

- [Tencent Cloud TIONE ClawHub Release](https://clawhub.ai/alger-z/skills/tencentcloud-tione-skill)
- [TI-ONE Tool Parameter Reference](artifact/references/cmd-reference.md)
- [TI-ONE Console Reference](artifact/references/tione-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Configuration guidance]

**Output Format:** [Markdown guidance with bash script invocations and JSON-formatted cloud query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials, tccli, jq, and an optional default TI-ONE region.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
