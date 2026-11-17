## Description:

Deploy a self-hosted funnel builder, take a funnel from empty install to published - landing page, checkout, one-click upsell, thank-you - and drive it from an agent over MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autonnel](https://clawhub.ai/user/autonnel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and operate a self-hosted sales funnel system on Cloudflare Workers, Docker, or a Node checkout, then configure checkout, tracking, and MCP-driven funnel edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npm or npx package execution can run newer code than the user reviewed.

Mitigation: Pin npm and npx package versions where possible and review commands before executing them.

Risk: Admin passwords or deployment secrets can be exposed when placed directly on the command line or in generated configuration.

Mitigation: Use secret managers or interactive secret commands, avoid putting real passwords in shell history, and keep credentials out of generated config files.

Risk: MCP write keys can modify production funnel content and checkout flows.

Mitigation: Issue one key per trusted agent, prefer read-only keys for reporting, and revoke keys instead of sharing them.

## Reference(s):

- [Autonnel repository](https://github.com/autonnel/autonnel)
- [Autonnel documentation](https://autonnel.com/docs)
- [ClawHub skill page](https://clawhub.ai/autonnel/skills/self-hosted-funnel-launch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides deployment steps, configuration values, MCP client snippets, launch checks, and operational cautions.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
