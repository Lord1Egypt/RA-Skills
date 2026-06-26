## Description: <br>
Design and build OpenClaw skills. Use when asked to "make/build/craft a skill", extract ad-hoc functionality into a skill, or package scripts/instructions for reuse. Covers OpenClaw-specific integration (tool calling, memory, message routing, cron, canvas, nodes) and ClawHub publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmz1](https://clawhub.ai/user/jmz1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Skillcraft to design, package, and publish OpenClaw skills from new requirements or existing reusable workflows. It guides skill architecture, frontmatter, OpenClaw integration choices, state handling, and implementation review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skills authored with this guide may introduce scheduled jobs, local command execution, browser sessions, API tokens, downloads, or persistent memory. <br>
Mitigation: Review generated skills before deployment, require clear user approval for powerful capabilities, and scope permissions and credentials to least privilege. <br>


## Reference(s): <br>
- [Skillcraft on ClawHub](https://clawhub.ai/jmz1/skillcraft) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [OpenClaw Creating Skills documentation](https://docs.openclaw.ai/tools/creating-skills) <br>
- [AgentSkills specification](https://agentskills.io) <br>
- [API Wrapper Pattern](patterns/api-wrapper.md) <br>
- [CLI Wrapper Pattern](patterns/cli-wrapper.md) <br>
- [Composable Pattern Examples](patterns/composable-examples.md) <br>
- [Monitor Pattern](patterns/monitor.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with structured skill specifications, file plans, and implementation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose skill files, frontmatter, scripts, integration patterns, state locations, and publishing guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
