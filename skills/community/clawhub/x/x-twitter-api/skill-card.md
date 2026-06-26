## Description: <br>
X (Twitter) API client for searching tweets, retrieving article content, and fetching trending topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zaaachary](https://clawhub.ai/user/Zaaachary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query X API v2 for recent posts, tweet or article details, and trending topics from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an X/Twitter bearer token and sends search queries, tweet IDs, and trend requests to X. <br>
Mitigation: Use a limited or read-only token where possible, avoid sharing sensitive queries, and rotate the token if it may have been exposed. <br>
Risk: Saved API responses may include content or metadata that the user did not intend to persist. <br>
Mitigation: Use --save only with explicit, intended output paths and review saved files before sharing or syncing them. <br>


## Reference(s): <br>
- [X Developer Portal](https://developer.x.com) <br>
- [X API Documentation](https://docs.x.com) <br>
- [WOEID Lookup](https://woeid.rosselliot.co.nz/) <br>
- [ClawHub Skill Page](https://clawhub.ai/Zaaachary/x-twitter-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Pretty text, JSON, Markdown, and optional saved files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the X_BEARER_TOKEN environment variable and may write user-selected output files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
