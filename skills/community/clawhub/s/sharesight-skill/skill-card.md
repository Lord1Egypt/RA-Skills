## Description: <br>
Manage Sharesight portfolios, holdings, and custom investments via the API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lextoumbourou](https://clawhub.ai/user/lextoumbourou) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect Sharesight portfolio data, run performance and holdings queries, and manage custom investments through authenticated CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Sharesight account data and cache an access token after authentication. <br>
Mitigation: Install it only when Sharesight account access is intended, protect the required credentials, and clear the cached token when the integration is no longer needed. <br>
Risk: Create, update, and delete commands can change Sharesight records when write access is enabled. <br>
Mitigation: Keep SHARESIGHT_ALLOW_WRITES unset for read-only use, enable it only for sessions that need changes, and review each write action carefully. <br>


## Reference(s): <br>
- [Sharesight API Getting Started](https://portfolio.sharesight.com/api/) <br>
- [OpenClaw Environment Configuration](https://docs.openclaw.ai/environment) <br>
- [Sharesight Skill on ClawHub](https://clawhub.ai/lextoumbourou/sharesight-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, shell commands, configuration, JSON data, guidance] <br>
**Output Format:** [JSON responses from CLI commands, with setup guidance and command examples in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations are disabled unless SHARESIGHT_ALLOW_WRITES is set to true.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, pyproject.toml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
