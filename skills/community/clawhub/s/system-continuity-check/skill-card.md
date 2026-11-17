## Description:

System Continuity Check helps agents review system and workflow designs for continuity, automation, restart recovery, and error isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minijoy-b](https://clawhub.ai/user/minijoy-b)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly evaluate whether a proposed system or automation workflow has complete handoffs, restart behavior, error handling, and low manual intervention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend autostart, service, monitoring, or restart changes during system design discussions.

Mitigation: Review those recommendations as design prompts and require explicit approval before implementing operational changes.

Risk: Broad activation wording may make the checklist appear in general engineering or automation discussions.

Mitigation: Use the skill when Chinese-language continuity review is desired and disregard it when the discussion is not about system, workflow, or automation design.

## Reference(s):

- [System Continuity Check on ClawHub](https://clawhub.ai/minijoy-b/skills/system-continuity-check)
- [Publisher profile: minijoy-b](https://clawhub.ai/user/minijoy-b)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown checklist results with pass, warning, or fail status and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language review guidance; no code execution or automatic system changes.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and artifact version notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
