## Description: <br>
Monitors YouTube videos for configured keywords, retrieves transcripts, creates Chinese summaries, and sends update reports to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huxiaoqiao](https://clawhub.ai/user/huxiaoqiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to monitor YouTube search terms, summarize newly found videos in Chinese, and receive scheduled Telegram updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript-derived reports may include private, sensitive, or copyrighted material and are saved locally before being sent through Telegram. <br>
Mitigation: Monitor only approved content, control the Telegram recipient, and set a retention policy for files in youtube-summaries. <br>
Risk: Incorrect Telegram or transcript API configuration can misroute reports or expose credentials. <br>
Mitigation: Store credentials in environment variables or a secrets manager, restrict local access, and verify the Telegram user ID before scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huxiaoqiao/youtube-openclaw-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/huxiaoqiao) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reports, Telegram-ready text, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create dated transcript summary files and a latest-report.md file under youtube-summaries when run with configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
