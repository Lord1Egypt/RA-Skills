## Description: <br>
Slack API integration with managed OAuth for sending messages, managing channels, searching conversations, and interacting with Slack workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and agent users use this skill to operate Slack workflows through Maton OAuth, including messages, channels, users, files, reactions, search, and connection management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton and Slack credentials that can access Slack workspace data. <br>
Mitigation: Install only if Maton is trusted for Slack data handling, protect MATON_API_KEY, and use the least-privileged Slack connection available. <br>
Risk: Requests can make real Slack workspace changes, including posting, deleting, archiving, inviting, kicking, uploading, or removing content. <br>
Mitigation: Require explicit user confirmation that names the target resource and intended effect before any write operation. <br>
Risk: Multiple Slack connections can cause actions to run against the wrong workspace or account. <br>
Mitigation: Specify the intended Maton connection whenever more than one Slack workspace is connected. <br>
Risk: Slack or Maton rate limits can interrupt automated workflows. <br>
Mitigation: Handle 429 responses with backoff or retry logic and keep request volume within documented limits. <br>


## Reference(s): <br>
- [ClawHub Slack skill page](https://clawhub.ai/byungkyu/slack-api) <br>
- [Maton homepage](https://maton.ai) <br>
- [Slack API Methods](https://api.slack.com/methods) <br>
- [Slack Web API Reference](https://api.slack.com/web) <br>
- [Slack Block Kit Reference](https://api.slack.com/reference/block-kit) <br>
- [Slack Message Formatting](https://api.slack.com/reference/surfaces/formatting) <br>
- [Slack Rate Limits](https://api.slack.com/docs/rate-limits) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with CLI commands, HTTP API examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and an active Slack OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
