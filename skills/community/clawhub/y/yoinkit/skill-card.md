## Description: <br>
Search, analyze, and transcribe content across 13 social platforms -- trending topics, video transcripts, post metadata, and multi-platform research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seomikewaltman](https://clawhub.ai/user/seomikewaltman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search social platforms, retrieve post metadata, pull supported video transcripts, monitor creator feeds, and combine search plus trending data into research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Social media URLs, account handles, search terms, and research topics are sent to Yoinkit using the configured API token. <br>
Mitigation: Use the skill only for data you are comfortable sending to Yoinkit, and avoid private links, sensitive account identifiers, or confidential research topics unless Yoinkit's privacy and retention practices meet your needs. <br>
Risk: Optional cron examples can automate repeated monitoring or write research notes to local systems such as Obsidian. <br>
Mitigation: Review cron configuration, target paths, and automation frequency before enabling scheduled workflows. <br>


## Reference(s): <br>
- [YoinkIt ClawHub release](https://clawhub.ai/seomikewaltman/yoinkit) <br>
- [Yoinkit platform capabilities](references/platforms.md) <br>
- [Yoinkit](https://yoinkit.ai) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown summaries and JSON results from Yoinkit API-backed commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Yoinkit API token; optional cron examples can automate monitoring and research workflows.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
