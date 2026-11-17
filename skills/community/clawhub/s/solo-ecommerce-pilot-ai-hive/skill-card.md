## Description:

Helps solo ecommerce operators turn product facts, budgets, channels, available media, and weekly goals into prioritized execution plans, content prompts, runnable AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as individual merchants, small ecommerce teams, independent-store sellers, and side-business founders use this skill to plan low-cost product listing and acquisition content. It can produce business breakdowns, daily content plans, image or video task prompts, AI-HIVE command examples, task records, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be sent to a configurable endpoint if AI_HIVE_BASE_URL or --base-url is changed.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is trusted, review ~/.ai-hive/config.json before execution, and prefer a limited API key.

Risk: Selected product media can be uploaded to AI-HIVE or object-storage services.

Mitigation: Upload only media the user is authorized to share and confirm privacy, trademark, copyright, and platform-rule constraints before submitting generation tasks.

Risk: Generated image or video tasks may incur costs and download files without strong destination or size limits.

Mitigation: Confirm final prompts, routing mode, and model parameters before paid execution; start with small samples and monitor task costs and downloaded file sizes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/solo-ecommerce-pilot-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference AI-HIVE task IDs, pricing snapshots, downloaded file paths, and acceptance checklist status when generation tasks are used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
