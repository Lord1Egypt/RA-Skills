## Description:

Each week, Ora audits your site and up to three competitors for AI agent readiness, opens one pull request with eligible source fixes, and posts a Slack digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing or go-to-market engineering teams use this agent to monitor how well AI agents can discover and use their website, compare it with competitors, and prepare limited source fixes for human review while sharing a weekly digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial and runtime permissions were not fully assessed; the skill uses MCP and shell capabilities.

Mitigation: Review the needed MCP and shell capabilities and the project's GitHub, Slack, and Anthropic permissions before enabling scheduled runs.

Risk: Automated website source changes may be unsuitable or incorrect for the site's conventions.

Mitigation: Review and validate the pull request before merging; the agent does not merge changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/website-auditing)
- [Project homepage](https://github.com/getcargohq/gtm-skills)
- [Weekly digest format](references/digest.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Markdown]

**Output Format:** [Weekly website audit findings, source changes proposed in a pull request, and a Slack digest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most one pull request per week, with up to three source-level fixes; changes require human review and merge.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
