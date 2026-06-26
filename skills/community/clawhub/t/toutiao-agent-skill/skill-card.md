## Description: <br>
Provides Toutiao account automation guidance and assets for scheduled local-livelihood content publishing, vegetable-price tracking, revenue optimization, and operational knowledge management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhhjwei](https://clawhub.ai/user/jhhjwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators with Toutiao accounts use this skill to prepare and publish scheduled local-livelihood posts, track vegetable-price and account-performance data, and apply revenue-focused operating playbooks. It is intended for users who can review posts and manage a logged-in Toutiao browser session. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content to a live Toutiao account through an existing browser session. <br>
Mitigation: Use manual or draft-only posting unless unattended scheduled publishing is explicitly desired, and review generated content before publication. <br>
Risk: A logged-in browser session may expose a primary Toutiao account to unintended posting or account changes. <br>
Mitigation: Prefer a non-primary account, keep browser sessions protected, and confirm the account state before enabling automation. <br>
Risk: The restore script copies knowledge, memory, and template files into an OpenClaw workspace and may affect existing workspace content. <br>
Mitigation: Inspect restore.sh and back up existing workspace knowledge, memory, and temp files before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jhhjwei/toutiao-agent-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jhhjwei) <br>
- [Toutiao creator platform](https://mp.toutiao.com) <br>
- [Toutiao publishing guide](artifact/knowledge/toutiao-publishing-guide.md) <br>
- [Toutiao growth knowledge base](artifact/knowledge/toutiao-growth.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell-command examples, content templates, operational checklists, and browser-action snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scheduled posting workflows, example memory/template files, and restore instructions for an OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
