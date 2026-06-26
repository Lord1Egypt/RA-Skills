## Description: <br>
Fetches recent AI, product, and technology YouTube channel updates, summarizes available transcripts in Chinese, and sends the digest as Feishu cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jadeyang7458-byte](https://clawhub.ai/user/jadeyang7458-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor selected AI, product, and technology YouTube channels, produce Chinese summaries of new videos, and deliver them to Feishu on demand or by cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports packaged real-looking credentials and reliance on local OpenClaw secrets. <br>
Mitigation: Remove or replace scripts/config.json before installation and confirm the skill uses only the user's own OpenClaw and Feishu configuration. <br>
Risk: Cron usage can repeatedly fetch YouTube data, send transcript excerpts to a model gateway, and deliver summaries to Feishu without further prompts. <br>
Mitigation: Treat scheduled execution as opt-in unattended processing, review the configured channels and recipient, and run with user-approved OpenClaw and Feishu credentials. <br>


## Reference(s): <br>
- [Complete Setup Guide and Troubleshooting Notes](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jadeyang7458-byte/youtube-daily-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style Feishu card content with setup and cron shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese digest text from YouTube transcript content and local OpenClaw Gateway responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
