## Description: <br>
Manage communities, schedule posts, automate workflows, and run DM sequences across Skool, Circle, Mighty Networks, Discord, and Slack via the stickyhive CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexblr](https://clawhub.ai/user/alexblr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and agent-assisted community teams use StickyHive to list communities and spaces, create or schedule posts, manage automation workflows, run DM sequences, and configure webhooks across supported community platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent publish, delete, reschedule, or bulk schedule posts in live communities. <br>
Mitigation: Require explicit user approval and review target space IDs, post IDs, content, and schedule times before running write actions. <br>
Risk: The skill requires a sensitive StickyHive API key. <br>
Mitigation: Use a test or least-privilege key where possible and avoid exposing the key in prompts, logs, screenshots, or shared terminal output. <br>
Risk: Workflow and DM sequence commands can automate messages, enroll members, and toggle or run automations. <br>
Mitigation: Review workflow configs, sequence steps, member IDs, daily limits, and dry-run results before enabling, running, or changing enrollments. <br>
Risk: Webhook commands can create or remove integrations that send event data to external URLs. <br>
Mitigation: Verify webhook destinations and event scopes before creation or deletion. <br>


## Reference(s): <br>
- [ClawHub StickyHive release](https://clawhub.ai/alexblr/stickyhive) <br>
- [StickyHive website](https://stickyhive.com) <br>
- [StickyHive dashboard](https://app.stickyhive.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STICKYHIVE_API_KEY and optional STICKYHIVE_API_URL environment variables.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
