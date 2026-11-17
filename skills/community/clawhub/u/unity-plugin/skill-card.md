## Description:

Control Unity Editor via OpenClaw Unity Plugin for Unity game development tasks including scene management, GameObject and Component manipulation, debugging, input simulation, and Play mode control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlichao456](https://clawhub.ai/user/mlichao456)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to control and inspect Unity Editor projects through OpenClaw workflows. It supports scene operations, object and component changes, asset and package management, testing, screenshots, and local or gateway-based Unity sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad project-changing updates in Unity projects.

Mitigation: Use it on test or version-controlled projects and review proposed Unity actions before execution.

Risk: The supplied security evidence reports an unauthenticated bridge with weak safeguards.

Mitigation: Keep the gateway reachable only from trusted local or private contexts and review the bridge authentication gap before using valuable projects.

Risk: Package installation and reflection-based script execution can introduce or run unintended code.

Mitigation: Avoid arbitrary Git package installs and reflection script execution unless explicitly intended and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mlichao456/skills/unity-plugin)
- [Skill Homepage](https://github.com/TomLeeLive/openclaw-unity-skill)
- [Unity Plugin Repository](https://github.com/TomLeeLive/openclaw-unity-plugin)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Unity Plugin Tools Reference](references/tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May queue Unity Editor commands and return JSON-formatted tool results through OpenClaw.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter states 1.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
