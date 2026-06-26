## Description: <br>
基于每小时收录的抖音、微博、B站、快手、知乎、头条、百度等7大平台热点数据，聚合全网最热TOP10热点。支持回溯近7天热点。不支持具体热点的查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, content operations teams, brand PR teams, and data analysts use this skill to retrieve and summarize the top cross-platform trending topics from seven Chinese social and search platforms, compare discussion focus across platforms, and generate a shareable HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key. <br>
Mitigation: Provide the key only through environment configuration, confirm its scope and revocation path, and avoid exposing it in prompts, logs, generated files, or source code. <br>
Risk: The skill contacts redfox.hk and creates local report files. <br>
Mitigation: Install and run it only in environments where outbound RedFox API access and local report generation are acceptable. <br>
Risk: Subscription or keyword-tracking flows may be under-scoped. <br>
Mitigation: Use those flows only after explicit user confirmation and only when the host clearly shows how to cancel or modify the subscription. <br>
Risk: Generated HTML reports include external trend data without strong sanitization. <br>
Mitigation: Treat generated reports as untrusted content, review them before sharing, and avoid opening them in privileged browser contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/trending-hub-top10) <br>
- [instruction-list.md](references/instruction-list.md) <br>
- [output-templates.md](references/output-templates.md) <br>
- [prediction-logic.md](references/prediction-logic.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, structured JSON, shell commands, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may create local report files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
