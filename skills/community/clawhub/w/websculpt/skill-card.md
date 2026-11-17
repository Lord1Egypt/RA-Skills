## Description:

WebSculpt bootstraps a CLI-backed browser automation workflow for acquiring external information, scraping pages, calling APIs, and maintaining reusable web operation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bqw1013](https://clawhub.ai/user/bqw1013)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, content teams, ecommerce operators, and analysts use WebSculpt to install and route browser automation workflows that access web information behind login or content walls and convert repeated web operations into reusable CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or updates the global WebSculpt package and persistent agent skills.

Mitigation: Install only if the WebSculpt package is trusted, prefer a project-local install where practical, pin and review the exact WebSculpt version, and inspect generated lifecycle skill files before allowing automatic use.

Risk: Browser automation may run on machines with logged-in browser sessions or sensitive data.

Mitigation: Use a constrained browser profile or isolated environment, review commands before execution, and avoid granting access to accounts or data beyond the intended task.

## Reference(s):

- [WebSculpt Skill on ClawHub](https://clawhub.ai/bqw1013/skills/websculpt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to install or update WebSculpt, Playwright CLI, and lifecycle skills before routing the user's web automation task.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
