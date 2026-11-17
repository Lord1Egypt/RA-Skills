## Description:

Team Projects helps OpenClaw agents plan, assign, dispatch, track, and discuss multi-agent project work with task boards, work breakdown structures, @-mention routing, and optional Control UI views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-agent projects in OpenClaw, create phases and tasks, assign work to specialist agents, route inter-agent messages, and track progress through CLI tools and optional UI components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad wildcard agent and tool permissions can give spawned agents more authority than a project requires.

Mitigation: Replace wildcard allowlists with explicit agent and tool allowlists before enabling the skill.

Risk: The optional local API behavior can expose project and chat operations without sufficient access controls if enabled casually.

Mitigation: Keep TEAM_PROJECTS_PORT disabled unless the API is protected with authentication and strict origin restrictions.

Risk: Project tasks and team chat may carry sensitive project details between agents.

Mitigation: Avoid placing secrets or sensitive business data in tasks, comments, chat messages, or generated project artifacts.

Risk: Spawned-agent tasks may request file writes or powerful tool use as part of project execution.

Mitigation: Review each dispatch plan and task prompt before allowing agents to write files or use privileged tools.

## Reference(s):

- [ClawHub Team Projects release page](https://clawhub.ai/maverick-software/skills/team-projects)
- [Team Projects walkthrough](artifact/references/walkthrough.md)
- [Example OpenClaw configuration](artifact/references/example-config.json)
- [Gateway plugin build registration](artifact/gateway-plugin/BUILD_REGISTRATION.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, JavaScript/TypeScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local JSON project state and chat logs under the configured Team Projects data directory when commands are executed.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
