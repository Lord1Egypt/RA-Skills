## Description:

yunxiao-devops helps agents interact with Alibaba Cloud Yunxiao DevOps across project tracking, Codeup repositories and merge requests, Flow pipelines, AppStack delivery, artifacts, testing, insights, and knowledge-base workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codingadai](https://clawhub.ai/user/codingadai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps teams use this skill to query and automate Yunxiao work items, code review, repository initialization, pipeline runs, release workflows, test cases, and Feishu notification cards from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact repository, merge request, pipeline, and deployment actions.

Mitigation: Use least-privilege test credentials first, require human review for proposed code and deployment changes, and keep automated merge or deploy flows disabled until reviewed.

Risk: Credential and SSH-key handling can expose or persist sensitive access material.

Mitigation: Rotate or revoke any exposed or generated tokens and SSH keys, avoid storing production secrets in local configuration files, and scope credentials to the minimum Yunxiao and Feishu permissions needed.

Risk: Shell command construction and unrestricted agent execution modes can make automation unsafe on trusted systems.

Mitigation: Avoid running the skill as root, review command inputs before execution, and do not enable automated bug-fix flows until shell command construction and bypass-permission behavior are remediated.

Risk: Shared temporary state can mix workflow data across executions or users.

Mitigation: Run the skill in an isolated workspace, clear temporary state between workflows, and avoid concurrent multi-user execution with shared credentials.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/codingadai/skills/yunxiao-devops)
- [Skill instructions](artifact/SKILL.md)
- [Projex workflow guide](artifact/references/projex-guide.md)
- [Pipeline YAML guide](artifact/references/pipeline-yaml-guide.md)
- [Pipeline YAML syntax](artifact/references/pipeline-yaml-syntax.md)
- [Workflow transition cache](artifact/references/workflow-transitions.json)
- [Yunxiao OpenAPI index](artifact/references/api-docs/INDEX.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and script invocation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local scripts and external DevOps APIs when the agent executes the generated commands.]

## Skill Version(s):

2.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
