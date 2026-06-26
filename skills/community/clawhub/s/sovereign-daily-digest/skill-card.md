## Description: <br>
Compile configured weather, calendar, task, email, RSS, quote, and related sources into a structured daily personal briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agent users use this skill to generate a daily digest they can scan quickly, combining local personal context and configured online sources into Markdown, HTML, or plain-text briefing output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local personal sources such as tasks, calendars, and GitHub issue context. <br>
Mitigation: Review the config before first use, keep unwanted sections disabled, and only add local paths or repositories that should appear in the digest. <br>
Risk: The skill contacts third-party services for weather, quotes, and feeds. <br>
Mitigation: Disable network-backed sources you do not want summarized or contacted, and review feed URLs before enabling them. <br>
Risk: The skill writes digest archives under ~/.openclaw and may guide recurring execution through cron or other schedulers. <br>
Mitigation: Inspect the output directory and retention settings, and only enable scheduled execution after confirming the exact command and how to remove it. <br>
Risk: Email handling can expose sensitive message metadata or content if enabled. <br>
Mitigation: Keep email disabled unless credentials, recipients, and summarized content are explicitly reviewed; use environment variables for passwords. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-daily-digest) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, or plain text digest content with optional saved files and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create a default local config, write digest archives under ~/.openclaw/daily-digest, print results to stdout, and optionally guide scheduling.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
