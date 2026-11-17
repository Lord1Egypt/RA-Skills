## Description: <br>
RSS AI 摘要 LITE helps an agent fetch RSS or Atom feeds, generate Chinese summaries with an LLM, de-duplicate items in SQLite, and post new summaries to a Feishu webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to monitor technical blogs and personal feed subscriptions, summarize new items in Chinese, and send updates to a Feishu group. It is intended for one-shot runs and can be paired with external scheduling when recurring delivery is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feed content and generated summaries may be sent to the configured LLM service and Feishu group. <br>
Mitigation: Use the skill only with feeds whose content may be shared with those services, and review organization privacy requirements before enabling delivery. <br>
Risk: LLM and Feishu credentials are required for normal use. <br>
Mitigation: Store API keys and webhook URLs in secure environment variables, rotate exposed credentials, and avoid committing populated configuration files. <br>
Risk: The skill relies on Python project files and dependencies referenced by the user workflow. <br>
Mitigation: Review the referenced Python project and requirements before running commands, and execute in an environment with appropriate filesystem and network permissions. <br>
Risk: The callback_url input is documented but the security guidance treats it as unsupported. <br>
Mitigation: Do not rely on callback_url behavior unless the publisher documents exactly how it is used. <br>
Risk: Summaries depend on the configured LLM and may be incomplete or factually inaccurate. <br>
Mitigation: Review generated summaries before using them for business decisions or broad distribution, and follow source links for full context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-ai-reader-free) <br>
- [Hacker News RSS example feed](https://hnrss.org/frontpage) <br>
- [阮一峰周刊 Atom example feed](https://www.ruanyifeng.com/blog/atom.xml) <br>
- [V2EX RSS example feed](https://www.v2ex.com/index.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with YAML configuration examples, shell command examples, and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include Chinese feed summaries, Feishu message content, execution logs, and SQLite-backed de-duplication status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
