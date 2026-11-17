## Description:

Routes user requests across finance, e-commerce, media, and office agent teams for analysis, content generation, media processing, and office workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx6315909](https://clawhub.ai/user/mx6315909)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route natural-language requests to specialized teams for stock and portfolio analysis, e-commerce product and listing work, media processing, and office productivity tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local, web, memory, session, and scheduling powers without enough scoping.

Mitigation: Review prompts and commands before installation and limit granted tool permissions to the minimum needed for the intended workflow.

Risk: Generated HTML mind maps may expose confidential content through unsafe HTML handling or CDN-loaded rendering code.

Mitigation: Avoid confidential content in generated HTML mind maps until the CDN dependency and HTML escaping issues are fixed.

Risk: The documented remote shell installation pattern can execute unreviewed code.

Mitigation: Do not run curl-piped shell commands without independent verification of the downloaded script and source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mx6315909/skills/xiaodi-multi-team-switcher)
- [Artifact README](artifact/README.md)
- [Artifact requirements](artifact/REQUIREMENTS.md)
- [ClawHub manifest](artifact/clawhub.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, code snippets, shell commands, JSON/configuration snippets, and task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files for media and office workflows and may call public web sources or optional API-backed video/image providers when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact frontmatter, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
