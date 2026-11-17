## Description:

Routes a user's task into one of six scenarios, applies a prioritized sequence of thinking frameworks, and checks whether the resulting conclusion is clear, example-backed, and logically sound.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wukaifeng704-cell](https://clawhub.ai/user/wukaifeng704-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to classify planning, learning, writing, prioritization, crisis, or ideation tasks and select an appropriate thinking framework sequence. It is most useful when a user wants structured reasoning guidance rather than a domain-specific tool integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references memory and publishing/layout pipelines that are not defined in the artifact.

Mitigation: Require explicit user consent before any persistent memory write, publishing action, or layout pipeline invocation.

Risk: The crisis-mode guidance says to skip normal approval.

Mitigation: Keep host approval gates in force and review proposed external commands or state-changing actions before execution.

Risk: Installer behavior can change across ClawHub versions.

Mitigation: Use a pinned ClawHub installer version when deploying the skill.

## Reference(s):

- [Scenario First Thinking on ClawHub](https://clawhub.ai/wukaifeng704-cell/skills/scenario-first-thinking)
- [SCQA Template](references/scqa-template.md)
- [Six Scenario Routing](references/six-scenario-routing.md)
- [Tool Handbook](references/tool-handbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured plain text with task classification, selected frameworks, reasoning steps, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external APIs or MCP tools are identified in the artifact evidence.]

## Skill Version(s):

2.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
