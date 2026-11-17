## Description:

Deep Research Agent specializes in complex, multi-step research tasks that require planning, decomposition, and long-context reasoning across tools and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to plan complex research, decompose broad questions into sub-tasks, analyze large context across tools and files, and synthesize findings into actionable reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests use of an external Crafted service and a CRAFTED_API_KEY, which may expose research context outside the local agent session.

Mitigation: Install only when the user is comfortable with the external service, and avoid providing sensitive files, secrets, or confidential research unless the publisher documents storage, transmission, opt-out, and deletion controls.

Risk: The skill describes retained cross-conversation memory without clear limits or user controls.

Mitigation: Use separate research contexts for sensitive work and review publisher documentation for retention, deletion, and memory-management controls before deployment.

Risk: The skill asks for broad local and external research access, which can increase exposure if the workspace contains private files.

Mitigation: Review the installed skill and workspace scope before use, limit accessible files to the intended research corpus, and scan proposed actions before execution.

## Reference(s):

- [Deep Research on ClawHub](https://clawhub.ai/asterisk622/skills/xiaoding-deep-research)
- [Crafted Deep Research](https://we-crafted.com/agents/deep-research)
- [Crafted](https://we-crafted.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research plans, synthesized analysis, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on external Crafted service access, local research context, and retained cross-conversation memory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
