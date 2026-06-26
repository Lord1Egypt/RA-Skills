## Description: <br>
Manage YouTube subscriptions by listing subscriptions or subscribers, subscribing to channels, and unsubscribing through the yutu CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenWaygate](https://clawhub.ai/user/OpenWaygate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage YouTube channel subscriptions from an agent workflow, including listing subscriptions, adding subscriptions, and deleting subscriptions through yutu commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth credentials and cached tokens that can grant access to a YouTube account. <br>
Mitigation: Keep client_secret.json and youtube.token.json out of shared folders and version control, restrict file permissions, and install only when comfortable granting yutu YouTube account access. <br>
Risk: Subscription deletion can remove YouTube subscriptions without enough built-in guardrails for agent use. <br>
Mitigation: Require the agent to list subscriptions first and confirm exact subscription IDs before running any delete command. <br>


## Reference(s): <br>
- [Yutu Homepage](https://github.com/eat-pray-ai/yutu) <br>
- [Setup Guide](references/setup.md) <br>
- [Subscription Delete](references/subscription-delete.md) <br>
- [Subscription Insert](references/subscription-insert.md) <br>
- [Subscription List](references/subscription-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes yutu CLI commands and setup notes that may require OAuth credential and token files.] <br>

## Skill Version(s): <br>
0.10.7-dev (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
