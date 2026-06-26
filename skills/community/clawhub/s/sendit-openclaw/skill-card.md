## Description: <br>
Execute SendIt social publishing workflows in OpenClaw using the official @senditapp/openclaw plugin tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shree-git](https://clawhub.ai/user/Shree-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social operations teams use this skill to connect SendIt accounts, validate posts, publish or schedule content, manage inbox and listening workflows, review analytics, and run related campaign, CRM, advertising, and automation tasks from OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad live social publishing, deletion, advertising, CRM, workflow, and connector actions. <br>
Mitigation: Install only when the publisher and SendIt environment are trusted, connect only required accounts, and require explicit user approval before publishing, deleting, replying, importing in bulk, creating ad campaigns, or triggering workflows. <br>
Risk: Connected social accounts may expose OAuth scopes beyond a single posting task. <br>
Mitigation: Review requested OAuth scopes before account connection and avoid optional agents or connectors unless they are needed for the user's workflow. <br>
Risk: Drafts or scheduled posts can be wrong, mistargeted, or misrendered across platforms. <br>
Mitigation: Use the skill's validation and preview workflows before publishing, and prefer approval workflows for high-impact posts. <br>


## Reference(s): <br>
- [SendIt OpenClaw on ClawHub](https://clawhub.ai/Shree-git/sendit-openclaw) <br>
- [Shree-git publisher profile](https://clawhub.ai/user/Shree-git) <br>
- [SendIt OpenClaw Tool Reference](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with tool names, workflow steps, configuration keys, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the @senditapp/openclaw plugin and plugins.entries.sendit.enabled configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
