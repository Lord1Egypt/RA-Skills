## Description:

Use when a request needs a real Ubuntu Server browser session with durable site login reuse, bounded manual login recovery, or host-side page inspection for protected sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linsuisheng034](https://clawhub.ai/user/linsuisheng034)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to open, inspect, and continue work in a real Ubuntu Server browser while reusing durable site logins. It supports bounded manual login recovery for protected sites when local recovery cannot clear a login wall or challenge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An authenticated browser profile can be exposed over unauthenticated LAN noVNC.

Mitigation: Bind noVNC to 127.0.0.1 or require SSH tunneling, avoid LAN exposure without authentication, and stop assisted sessions after login recovery.

Risk: Durable browser state can retain access to logged-in sites across agent tasks.

Mitigation: Use trusted session-key values, avoid guessing between identities, and review persistent profile reuse before installing the skill.

## Reference(s):

- [Ubuntu Browser Session ClawHub page](https://clawhub.ai/linsuisheng034/skills/ubuntu-browser-session)
- [Use Cases](references/use-cases.md)
- [Assisted Session Flow](references/assisted-session-flow.md)
- [Session Storage](references/session-manifest.md)
- [Manual Fallback](references/manual-fallback.md)
- [Forum/Search Result Enhancements](references/forum-enhancements.md)
- [Testing Matrix](references/testing-matrix.md)
- [Validation Findings](references/validation-findings.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Markdown, Text]

**Output Format:** [Markdown guidance with bash commands and JSON or text browser inspection output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return noVNC access URLs and Chrome DevTools Protocol inspection results for the active host browser session.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
