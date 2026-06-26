## Description: <br>
Repliz social media management API integration for managing connected social media accounts, schedules, and comments with Repliz credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staryone](https://clawhub.ai/user/staryone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Repliz-connected social media accounts, scheduled posts, and comment queues from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable live posting, replies, scheduling changes, and irreversible deletion on connected social media accounts. <br>
Mitigation: Use revocable, least-privilege Repliz API credentials and require the agent to show the account, post or comment, schedule ID, and intended action before making live changes. <br>
Risk: Repliz credentials grant access to manage social media content. <br>
Mitigation: Store REPLIZ_ACCESS_KEY and REPLIZ_SECRET_KEY securely, rotate them when no longer needed, and avoid exposing them in prompts, logs, or generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/staryone/repliz) <br>
- [Repliz homepage](https://repliz.com) <br>
- [Repliz API base URL](https://api.repliz.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API request examples] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and REPLIZ_ACCESS_KEY and REPLIZ_SECRET_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
