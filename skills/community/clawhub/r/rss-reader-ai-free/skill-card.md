## Description: <br>
Automatically fetches RSS and Atom feeds, uses an AI model to generate concise Chinese summaries, deduplicates previously delivered items, and sends updates through one selected notification channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal users and information workers use this skill to monitor RSS or Atom feeds, summarize new items in Chinese, avoid duplicate notifications, and receive updates through Feishu, Telegram, or email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected feed content, generated summaries, API keys, webhook URLs, bot tokens, and email credentials may be exposed to configured LLM or notification providers if handled carelessly. <br>
Mitigation: Keep credentials in environment variables or a secret manager, review provider destinations before use, and send only feed content appropriate for those services. <br>
Risk: Scheduled execution can repeatedly deliver incorrect, duplicate, or unwanted summaries if configuration, feeds, or provider access are wrong. <br>
Mitigation: Test with one-time execution before enabling a schedule, review missing implementation files before running them, and monitor initial deliveries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-reader-ai-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces feed summaries and setup guidance for a single notification channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
