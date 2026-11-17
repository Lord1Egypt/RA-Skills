## Description:

Establishes a workflow for checking and invoking applicable agent skills before responding or taking action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make agents check for applicable skills at the start of conversations and before task actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad mandatory skill-invocation rules can reduce agent discretion and cause unrelated secondary skills to influence normal work.

Mitigation: Install only where skill-first routing is desired, keep higher-priority policies authoritative, and review proposed secondary skill use before acting.

Risk: The skill attempts to impose process rules across nearly any action.

Mitigation: Scope deployment to agents or workspaces that explicitly require this behavior and remove it if it conflicts with local operating policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown instructions for agent behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, API calls, or generated files are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
