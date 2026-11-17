## Description: <br>
Social Media Toolkit helps agents prepare and run social-media operations with batch actions, multi-agent coordination, analytics, relationship-graph management, webhook handling, and API-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, developers, and operators use this skill to coordinate social-platform API workflows, batch messages or relationship updates, analyze engagement data, and manage multi-agent social operations. Users should review and approve external actions manually before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk social actions such as messages, likes, swipes, profile updates, and relationship changes can affect external accounts or people at scale. <br>
Mitigation: Require human approval for every external action, enforce conservative rate limits, and verify consent plus platform policy compliance before execution. <br>
Risk: API tokens, webhook secrets, archived analytics, and relationship data may expose sensitive account or social-graph information. <br>
Mitigation: Use environment variables, least-privilege credentials, HTTPS, webhook signature validation, secret rotation, and log redaction for all sensitive data. <br>
Risk: Generated curl commands and exec-enabled workflows can trigger real network operations against social-platform APIs. <br>
Mitigation: Run commands in a controlled environment, restrict allowed endpoints and actions, and review dry-run output before live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/social-media-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown with inline shell, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce external API request plans, curl commands, configuration snippets, analytics summaries, and structured JSON responses for human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
