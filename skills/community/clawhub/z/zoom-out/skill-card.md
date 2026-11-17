## Description:

Tell the agent to zoom out and give broader context or a higher-level perspective on a section of code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get a concise architecture-level map of an unfamiliar code area before making changes or diving into implementation details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce an incomplete or misleading architecture map if relevant files, callers, or dependencies are missed.

Mitigation: Ask the agent to identify the files and call relationships it inspected, and verify the map before relying on it for code changes.

Risk: The skill is intended to inspect project files for architecture context.

Mitigation: Use it only in workspaces where the agent is allowed to inspect the relevant project code and avoid including unrelated secrets or sensitive files in the review scope.

## Reference(s):

- [Zoom Out ClawHub Skill Page](https://clawhub.ai/genortg/skills/zoom-out)
- [Publisher Profile](https://clawhub.ai/user/genortg)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown architecture overview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically includes module role, public API, dependencies, callers, and architectural context.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
