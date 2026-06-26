## Description: <br>
Guides agents through authenticated Sequenzy email-marketing operations, including subscriber, list, segment, campaign, sequence, template, webhook, inbox, team, analytics, and transactional-email workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose and run the correct Sequenzy CLI or MCP workflow for email-marketing account management, campaign operations, audience management, content generation, delivery stats, and dashboard handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through broad account-changing Sequenzy actions such as campaign sends, subscriber imports or removals, webhook changes, API-key creation, and campaign cancellation. <br>
Mitigation: Install only when the publisher is trusted, verify authentication context first, and require explicit confirmation of the account, audience, campaign, and exact action before mutation. <br>
Risk: Campaign cancellation guidance notes a no-confirmation path, which could stop scheduled, paused, waiting-approval, or sending campaigns immediately. <br>
Mitigation: Require a human confirmation step before cancellation and review the campaign ID, status, audience, and business impact before running the command. <br>
Risk: The skill requires sensitive Sequenzy credentials and may expose or create account-level access. <br>
Mitigation: Use scoped API keys where available, avoid sharing secrets in prompts or logs, and rotate or revoke keys after elevated workflows. <br>


## Reference(s): <br>
- [Sequenzy Email Marketing Skill](https://clawhub.ai/polnikale/sequenzy-email-marketing) <br>
- [Command Reference](references/command-reference.md) <br>
- [Use Cases](references/use-cases.md) <br>
- [Sequenzy Dashboard](https://sequenzy.com) <br>
- [Sequenzy API](https://api.sequenzy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dashboard URLs, API caveats, confirmation prompts, and review steps for account-changing actions.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
