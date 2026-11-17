## Description:

Live sports alerts for Soccer, NFL, NBA, NHL, MLB, F1 and more. Real-time scoring with the free ESPN API. Track any team from any major league worldwide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure team tracking, fetch live and scheduled sports updates, and prepare OpenClaw automations for match-day reminders and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts ESPN plus Brave or Serper for sports results and search fallback behavior.

Mitigation: Install only when those external services are acceptable for the deployment, and review network behavior before use.

Risk: The skill can read a Serper API key from another installed skill's .env file.

Mitigation: Remove the web-search-plus .env fallback or require a sports-ticker-specific key before deployment.

Risk: Generated automations can execute the live monitor and require OpenClaw approval grants.

Mitigation: Review generated automations before applying them and approve only the intended exec grant.

Risk: The skill stores local score and configuration state.

Mitigation: Review the local config and score cache files for sensitive or stale information during operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/skills/sports-ticker)
- [OpenClaw](https://openclaw.com)
- [Public ESPN API Documentation](https://github.com/pseudo-r/Public-ESPN-API)
- [ESPN OpenAPI Spec](https://github.com/zuplo/espn-openapi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local config.json, score cache state, and OpenClaw automation definitions for review.]

## Skill Version(s):

3.3.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
