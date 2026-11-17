## Description:

War Room helps agents run structured multi-agent sessions that use specialist roles, dependency-ordered waves, adversarial review, and consolidation to produce plans, specs, blueprints, and next-step deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxkle1nz](https://clawhub.ai/user/maxkle1nz)

### License/Terms of Use:

MIT

## Use Case:

Developers, product leads, and other external users use War Room to structure complex planning sessions for software, hardware, content, business strategy, and architecture review. It is most useful when a team needs multiple specialist perspectives, explicit decision logs, adversarial challenge, and a consolidated blueprint before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a high-autonomy multi-agent workflow that can move from planning into execution or build phases.

Mitigation: Require operator confirmation before execution or build phases and review the consolidated blueprint before acting on it.

Risk: The workflow may schedule follow-up checks through OpenClaw cron when agents are running asynchronously.

Mitigation: Require confirmation before cron scheduling and monitor or cancel scheduled OpenClaw jobs after the session.

Risk: The workflow writes a broad workspace structure for each war room session.

Mitigation: Restrict project names to simple kebab-case and review the target workspace before initialization.

Risk: The workflow may open generated local artifacts for review through the operating system's default file viewer.

Mitigation: Require confirmation before opening local files and keep artifact paths scoped to the war room workspace.

## Reference(s):

- [War Room README](README.md)
- [Agent Roles Reference](references/agent-roles.md)
- [Agent DNA v3](references/dna-template.md)
- [Wave Protocol Reference](references/wave-protocol.md)
- [ClawHub Skill Page](https://clawhub.ai/maxkle1nz/skills/war-room)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents, shell commands, project files, and structured planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a war-rooms/<project>/ workspace with briefs, decisions, agent outputs, artifacts, communication logs, blockers, status, summaries, and post-mortems.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
