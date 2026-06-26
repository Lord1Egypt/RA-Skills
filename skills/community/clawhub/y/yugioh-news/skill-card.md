## Description: <br>
Summarizes the previous day's Japanese Yu-Gi-Oh news in Chinese and can be scheduled as a daily Beijing-time OpenClaw cron task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangrongyong](https://clawhub.ai/user/jiangrongyong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Yu-Gi-Oh players, collectors, content creators, and community maintainers can use this skill to receive a daily Chinese summary of Japanese Yu-Gi-Oh card, rules, event, and product news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled task can post recurring Yu-Gi-Oh news summaries into the current conversation. <br>
Mitigation: Install it only when that daily 10:00 Beijing-time behavior is desired, and keep the OpenClaw cron job easy to list, change, or remove. <br>
Risk: The provided cron prompt contains hardcoded 2026 date wording that can become stale after 2026. <br>
Mitigation: Update the prompt's year wording before using the skill in later years. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangrongyong/yugioh-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted Chinese news summary with optional shell command guidance for cron setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for a daily 10:00 Asia/Shanghai schedule; summaries depend on web search results available at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
