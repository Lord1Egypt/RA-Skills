## Description:

Automatically discover and route relevant installed skills for the current task, plus run a daily skill audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chchchadzilla](https://clawhub.ai/user/chchchadzilla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to rank installed skills before non-trivial tasks and to audit skill descriptions for duplicates, overlaps, and weak trigger language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local router reads installed skill metadata from configured skill directories.

Mitigation: Install only in workspaces where reading installed skill names, descriptions, and paths is acceptable.

Risk: Automatic routing hooks in AGENTS.md or HEARTBEAT.md can influence which skills an agent considers before work.

Mitigation: Manually review hook changes and load only the top 1-3 matching skills as the artifact operating rules recommend.

## Reference(s):

- [Setup Checklist for Auto Skill Routing](references/setup-checklist.md)
- [Skill Auto-Router ClawHub Release](https://clawhub.ai/chchchadzilla/skills/skill-auto-router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from the router script and Markdown guidance with inline shell commands for setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The router reports ranked skill candidates, match reasons, audit findings, and integration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
