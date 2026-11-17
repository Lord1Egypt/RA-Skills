## Description:

Scanblitz helps agents create dynamic, trackable QR codes, update QR destinations, and inspect scan analytics through the ScanBlitz API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whotookmylogin](https://clawhub.ai/user/whotookmylogin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill when an agent needs to create, update, deactivate, delete, or analyze dynamic QR codes for campaigns, events, packaging, or landing pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ScanBlitz API credentials may authorize QR creation, update, analytics, or deletion actions beyond the current task.

Mitigation: Use keys scoped to the needed account actions, keep them in trusted environment storage, and avoid printing or committing SCANBLITZ_API_KEY.

Risk: An untrusted SCANBLITZ_API_BASE value could route credentials or QR data to an unintended endpoint.

Mitigation: Use the documented default endpoint or another trusted endpoint, and do not accept base URL overrides from prompt or project context.

Risk: The optional MCP setup uses unpinned npx package execution.

Mitigation: Skip the MCP path unless the package has been verified and pinned to a trusted version.

Risk: The optional qrserver.com rendering path sends campaign links to an additional third-party service.

Mitigation: Avoid that rendering path for sensitive or unreleased campaign links; use a trusted QR renderer instead.

## Reference(s):

- [ScanBlitz homepage](https://scanblitz.com)
- [ScanBlitz API docs](https://scanblitz.com/api-docs)
- [ScanBlitz agent reference](https://scanblitz.com/llms-full.txt)
- [ClawHub skill page](https://clawhub.ai/whotookmylogin/skills/scanblitz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash, JSON, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes expected API response shapes and operational notes for ScanBlitz QR code workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
