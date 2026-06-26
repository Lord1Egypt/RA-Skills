## Description: <br>
StockScanner Pro is a social-media automation skill for generating, scheduling, publishing, and listing posts across Twitter/X, Weibo, and Xiaohongshu with optional comment auto-replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anson125chen](https://clawhub.ai/user/anson125chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketing operators, and developers use this skill to generate platform-specific social posts, schedule publication, run due tasks, and manage basic social-media automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or reply from public social-media accounts when configured with platform credentials. <br>
Mitigation: Use dry-run or manual review before enabling posting, scheduled execution, or auto-reply workflows; keep a quick disable path available. <br>
Risk: The skill relies on sensitive platform credentials, including API keys, access tokens, and browser cookies. <br>
Mitigation: Use least-privileged tokens where available, avoid browser cookies when possible, store credentials outside shared files, and rotate credentials after testing. <br>
Risk: Scheduled and automated replies can create unintended public activity at scale. <br>
Mitigation: Set explicit rate limits, review reply rules before activation, and monitor scheduled jobs after deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/anson125chen/stockscanner-pro) <br>
- [Publisher profile](https://clawhub.ai/user/anson125chen) <br>
- [Project website](https://asmartglobal.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local scheduled-task records and may propose cron-based execution when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
