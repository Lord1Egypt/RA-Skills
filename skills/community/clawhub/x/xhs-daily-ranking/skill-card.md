## Description:

小红书每日爆款笔记 helps creators and operators query Xiaohongshu daily TOP50 breakout notes by keyword or category and turn ranking data into reusable topic, title, and content-pattern insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand operators, MCN scouts, and growth analysts use this skill to monitor daily Xiaohongshu breakout content, identify fast-rising topics, and generate ranking tables, trend analysis, and optional HTML reports for planning or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a RedFox API key and query metadata to redfox.hk.

Mitigation: Use a scoped or session-limited key where possible, store it in an environment variable or secret manager, and rotate or revoke it if exposed.

Risk: Environment-variable setup instructions can lead an agent to write or echo a plaintext API key in shell profiles or terminal output.

Mitigation: Prefer a secret manager or session-scoped environment variable, and avoid placing the key in logs, prompts, committed files, or shared shell history.

Risk: Generated HTML reports and JSON cache inputs can contain untrusted content and reports may load JavaScript from a CDN.

Mitigation: Open generated reports only in a trusted environment, review cache inputs before reuse, and apply normal browser and file-handling precautions.

Risk: Daily subscription pushes can continue sending trend data after setup.

Mitigation: Enable subscription only with clear user intent and keep a known cancellation path available.

## Reference(s):

- [Core workflow](artifact/references/core_workflow.md)
- [English README](artifact/README.en.md)
- [ClawHub skill page](https://clawhub.ai/if530770/skills/xhs-daily-ranking)
- [RedFoxHub](https://redfox.hk/)
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, shell commands, configuration, guidance, files]

**Output Format:** [Markdown tables and prose, with optional standalone HTML report files and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; optional HTML reports may load CDN JavaScript and can be generated from JSON cache input.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
