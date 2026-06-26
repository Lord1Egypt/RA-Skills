## Description: <br>
Multi-platform article publisher and content distribution tool for syncing and cross-posting Markdown or HTML articles to Chinese content platforms, tech communities, blogging sites, and self-hosted blogs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lljxx1](https://clawhub.ai/user/lljxx1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, developers, and operators use this skill to check WechatSync prerequisites and authentication state, extract browser articles, and prepare CLI commands for syncing article drafts to selected publishing platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected articles and images may be uploaded to third-party publishing platforms through logged-in browser sessions. <br>
Mitigation: Confirm the exact article file and target platforms before syncing, use dry-run or draft review where possible, and review resulting drafts before publishing. <br>
Risk: The workflow depends on the external WechatSync npm package and Chrome extension. <br>
Mitigation: Install only after confirming trust in those components and verifying the required CLI, extension, token, and platform logins. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lljxx1/wechatsync) <br>
- [WechatSync homepage](https://github.com/wechatsync/Wechatsync) <br>
- [WechatSync CLI source](https://github.com/wechatsync/Wechatsync/tree/v2/packages/cli) <br>
- [WechatSync extension source](https://github.com/wechatsync/Wechatsync/tree/v2/packages/extension) <br>
- [Chrome Web Store extension](https://chrome.google.com/webstore/detail/hchobocdmclopcbnibdnoafilagadion) <br>
- [WechatSync extension install page](https://www.wechatsync.com/#install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prerequisite checks, platform login guidance, sync or extraction commands, and draft URLs reported by the CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
