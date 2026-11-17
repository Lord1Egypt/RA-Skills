## Description:

Manage Sharesight portfolios, holdings, and custom investments via the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lextoumbourou](https://clawhub.ai/user/lextoumbourou)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to inspect Sharesight portfolios, holdings, performance data, trades, custom investments, prices, coupon rates, and reference data. It can also create, update, and delete financial records when write access is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, or delete financial records when write mode is enabled.

Mitigation: Keep SHARESIGHT_ALLOW_WRITES unset unless write actions are intentional, and review delete or trade-changing commands before execution.

Risk: The skill uses Sharesight API credentials and caches access tokens locally.

Mitigation: Protect SHARESIGHT_CLIENT_ID, SHARESIGHT_CLIENT_SECRET, and the local token cache; install only in trusted environments.

Risk: The security verdict places this release in Review rather than automatic approval.

Mitigation: Use a locked or reviewed dependency installation and review the package before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lextoumbourou/skills/sharesight-skill)
- [Sharesight API getting started](https://portfolio.sharesight.com/api/)
- [OpenClaw environment configuration](https://docs.openclaw.ai/environment)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Sharesight API credentials; write operations require SHARESIGHT_ALLOW_WRITES=true.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, pyproject.toml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
