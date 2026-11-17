## Description:

OpenClaw Video Publisher helps agents install, configure, and operate a Node.js tool for publishing videos across Douyin, Kuaishou, WeChat Channels, Bilibili, YouTube, and TikTok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and agents use this skill to configure credentials, publish single or batched videos, schedule releases, retry failures, and review publication history across multiple social video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unaudited mutable code can expose the agent environment and publishing credentials.

Mitigation: Pin the package to a reviewed version or full Git commit, avoid global installation where possible, and review the package before running npm install.

Risk: Platform API credentials can authorize public content publication if they are leaked or over-scoped.

Mitigation: Use narrowly scoped, revocable credentials, store them in local environment files or environment variables, and redact credentials from logs.

Risk: Automated or scheduled publishing can post unintended files to unintended platforms or accounts.

Mitigation: Require explicit allowlists for files, platforms, accounts, and publication times before enabling batch or scheduled publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/video-publisher)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zhenstaff)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, credential configuration, publishing, retry, scheduling, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
