## Description:

Builds websites and web applications from scratch using a structured planning workflow for static sites, SPAs, full-stack apps, and separated frontend/backend projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to plan, implement, validate, and launch web projects. It guides requirement gathering, architecture selection, UI planning, coding, build verification, and local preview delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create project files, update .web-builder/plan.md, install dependencies, run npm, pip, or build commands, and start a local Vite preview server.

Mitigation: Use it in a disposable or trusted workspace, review generated package files before install, and stop the server after use.

Risk: The skill starts Vite with network host exposure by default during preview delivery.

Mitigation: Bind previews to localhost unless LAN sharing is intentional.

Risk: Generated dependency files may introduce unpinned or unexpected packages.

Mitigation: Review generated package files and pin dependencies before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/skills/wps-web-builder)
- [Publisher profile](https://clawhub.ai/user/xixihaha123123123123)
- [Frontend design guidance](artifact/frontend-design.md)
- [Web builder plan template](artifact/plan-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell commands, configuration files, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files, plan documentation, package configuration, README content, and local preview commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
