## Description: <br>
小红书每日爆款笔记推荐 helps agents query Xiaohongshu daily breakout content by keyword or category, summarize trend patterns, and optionally prepare HTML reports for review or sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, MCN teams, and growth analysts use this skill to monitor Xiaohongshu daily breakout notes, identify reusable topic and title patterns, and plan follow-up content or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends query metadata to redfox.hk. <br>
Mitigation: Use a scoped or revocable API key, store it in a temporary environment variable or secret manager, and avoid exposing it in prompts, logs, generated files, or source control. <br>
Risk: The skill guidance includes persistent shell or user environment configuration for REDFOX_API_KEY. <br>
Mitigation: Review any proposed environment edits before applying them and prefer session-scoped configuration when testing or running in shared environments. <br>
Risk: Generated HTML can be network-active because it loads CDN scripts for image and PDF export. <br>
Mitigation: Open generated HTML only in an environment where loading external CDN scripts is acceptable, or disable network access before viewing if export features are not needed. <br>
Risk: Daily subscription pushes may continue producing Xiaohongshu trend outputs after setup. <br>
Mitigation: Enable subscription only with explicit user consent and keep a clear cancellation path available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-daily-breaking) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFoxHub](https://redfox.hk) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Configuration, HTML files, Guidance] <br>
**Output Format:** [Markdown rankings and analysis, optional HTML report files, and shell commands for local script execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for RedFox API access; HTML export loads CDN scripts for image and PDF generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
