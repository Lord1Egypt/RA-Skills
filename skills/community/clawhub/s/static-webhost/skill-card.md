## Description:

Deploy static web pages and apps through auto-detected Caddy or Nginx while requiring explicit approval for privileged local web-server changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serein-213](https://clawhub.ai/user/serein-213)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy static HTML, CSS, and JavaScript assets through an existing Caddy or Nginx service and obtain a reachable HTTP URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through root-level Caddy or Nginx changes using under-specified deployment path templates.

Mitigation: Require explicit approval for every privileged command, validate project names and source paths, back up existing configuration, and run server config tests before reload.

Risk: System-level static hosting may be unnecessary for local previews and can expose files over HTTP.

Mitigation: Prefer a non-root local static server when system deployment is not necessary and confirm the intended exposure before copying files into the web root.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/serein-213/skills/static-webhost)
- [ClawHub publisher profile](https://clawhub.ai/user/serein-213)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and web-server configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged command proposals that require explicit user approval, backups, configuration tests, and service reloads before deployment.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
