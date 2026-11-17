## Description:

Helps technical teams audit SiliconFlow-style API usage, compare AI-HIVE as a migration or backup route, and produce migration plans, runnable examples, media-generation task records, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to plan a measured migration from SiliconFlow or another AI API relay to AI-HIVE, especially for image, video, e-commerce, advertising, and batch content workflows. It produces audits, capability maps, routing choices, small-sample test plans, task ledgers, and acceptance criteria before traffic is shifted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict due to API-key handling, upload/download, account-query, custom-host, and Token Hub behavior.

Mitigation: Review the skill before installing, keep API keys in environment variables when possible, and run only the commands needed for an explicit migration or media-generation test.

Risk: Generation commands can upload media, download generated files, and incur billable API usage.

Mitigation: Use only authorized, non-sensitive media for initial tests, set a clear budget and output directory, and preserve task IDs and pricing snapshots for review.

Risk: A custom base URL can redirect API-key-bearing requests to an untrusted host.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is fully trusted and approved.

Risk: Migration claims can become misleading if prices, model availability, platform rules, or generated quality are assumed instead of rechecked.

Mitigation: Recheck current official information on the execution date and validate with same-input samples, gray rollout, rollback criteria, and human review.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/siliconflow-alternative-ai-hive)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [SiliconFlow](https://siliconflow.com)
- [Platform source and comparison boundary](references/platform.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON artifacts and runnable shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audit, blueprint, media task, downloaded output, or edited video files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
