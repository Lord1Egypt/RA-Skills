## Description:

Multi-platform article publisher and content distribution tool for syncing and cross-posting Markdown or HTML articles to Chinese content platforms, tech communities, blogging sites, and self-hosted blogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lljxx1](https://clawhub.ai/user/lljxx1)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, developers, and publishing teams use this skill to have an agent prepare WechatSync CLI workflows for checking platform login status, extracting browser articles, and syncing Markdown or HTML drafts across supported publishing platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned npm CLI or browser extension can introduce supply-chain exposure.

Mitigation: Install only from the intended npm registry and Chrome Web Store or source repository, avoid elevated installs, and consider pinning or reviewing the @wechatsync/cli version before use.

Risk: The browser extension can act through platform sessions where the user is already logged in.

Mitigation: Confirm the target platforms and login state before syncing, use dry-run or draft workflows when available, and review drafts before publishing.

Risk: The WechatSync token grants local CLI-to-extension access for the user's browser environment.

Mitigation: Keep WECHATSYNC_TOKEN local, avoid sharing it in prompts or logs, and rotate it if it may have been exposed.

## Reference(s):

- [WechatSync Homepage](https://github.com/wechatsync/Wechatsync)
- [WechatSync CLI Source](https://github.com/wechatsync/Wechatsync/tree/v2/packages/cli)
- [WechatSync Extension Source](https://github.com/wechatsync/Wechatsync/tree/v2/packages/extension)
- [Chrome Web Store Listing](https://chrome.google.com/webstore/detail/hchobocdmclopcbnibdnoafilagadion)
- [WechatSync Install Page](https://www.wechatsync.com/#install)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include login-status summaries, draft URLs, or next-step publishing guidance based on WechatSync CLI results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
