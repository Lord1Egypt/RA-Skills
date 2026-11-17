## Description:

Fingerprint one project (or a whole folder of repos) for listable assets - MCP server, Agent Skill, plugin, OpenAPI, CLI, browser extension - and rank the marketplaces and directories it can be listed on now, plus which single asset to build next to unlock the most listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inventory a project’s listable assets, compare relevant platforms, and prioritize the next asset to build. It creates a visibility plan for a project or portfolio of repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance notes that the tool scope is undeclared.

Mitigation: Review the required commands and proposed actions before invoking the skill, and personally approve any external action.

Risk: The security guidance flags an unpinned install reference.

Mitigation: Inspect the referenced source and pin a reviewed revision before installing or executing it.

Risk: The security guidance notes an English-only documentation instruction.

Mitigation: Have a reviewer fluent in the documentation language check that the instructions are understood and followed.

Risk: The security guidance flags an auto-deploy reference.

Mitigation: Keep deployment behind explicit user review and approval.

Risk: The security review was partial because some referenced paths were missing.

Mitigation: Review the complete release contents and relevant paths before relying on the scan verdict.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/orensegal/skills/visibility-plan)
- [Project homepage](https://github.com/OrenSegal/visibility)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, CSV]

**Output Format:** [Markdown reports and a CSV ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project visibility plan files under .visibility/; it does not publish listings.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
