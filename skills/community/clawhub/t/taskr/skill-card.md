## Description:

Persistent cloud task planning and execution for OpenClaw agents, with hierarchical plans, durable notes, cross-agent continuity, and user-visible status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echo-of-machines](https://clawhub.ai/user/echo-of-machines)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Taskr to plan substantial OpenClaw work in a persistent cloud task hierarchy, resume work across sessions or agents, and maintain auditable notes and status checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task plans and notes are stored in Taskr cloud and may contain sensitive work context.

Mitigation: Use separate projects for separate work contexts and avoid recording secrets or sensitive details beyond what the project requires.

Risk: MCP_USER_API_KEY can expose the configured Taskr project if it is leaked.

Mitigation: Treat the key as a secret; do not paste it into prompts, logs, screenshots, or commits, and rotate it if exposed.

Risk: Persistent shared task state can become stale or confusing if agents abandon incomplete tasks.

Mitigation: Review task status before resuming, keep one task in progress at a time, and close skipped work with an explanatory finding note.

## Reference(s):

- [Taskr homepage](https://taskr.one)
- [Taskr MCP endpoint](https://taskr.one/api/mcp)
- [ClawHub skill page](https://clawhub.ai/echo-of-machines/skills/taskr)
- [ClawHub publisher profile](https://clawhub.ai/user/echo-of-machines)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MCP_API_URL, MCP_PROJECT_ID, and MCP_USER_API_KEY configuration to use the Taskr service.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
