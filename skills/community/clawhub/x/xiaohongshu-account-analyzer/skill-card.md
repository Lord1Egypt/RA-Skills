## Description: <br>
我是一名深耕小红书账号分析的诊断师，擅长用数据说话，帮你发现账号的真实问题。从定位模糊到变现困难，从选题迷茫到更新瓶颈，我都能给你一份基于数据的诊断报告和可落地的行动建议。当你需要分析自己的账号数据、诊断账号健康度、评估商业价值、对比竞品账号或制定优化策略时，找我准没错。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Xiaohongshu creators, MCN operators, brands, and competitor analysts use this skill to query account data, score account health across seven dimensions, compare one or more accounts, and generate actionable markdown and HTML diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFoxHub API key and sends Xiaohongshu account identifiers to RedFoxHub. <br>
Mitigation: Install only after confirming the API key source, scope, validity, and revocation path; avoid hard-coding or exposing the key in prompts, logs, or generated files. <br>
Risk: The security summary reports API-key-protected account data transfer with TLS verification disabled. <br>
Mitigation: Avoid use on sensitive accounts or hostile networks unless TLS verification is fixed and reviewed. <br>
Risk: The skill writes local raw data and generated report files that may contain account analysis details. <br>
Mitigation: Review, protect, or delete output/raw_data.json and generated HTML reports after use. <br>
Risk: The skill includes delayed push/backfill and cross-platform search behavior. <br>
Mitigation: Treat those actions as optional, explicitly confirmed, and cancellable before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/xiaohongshu-account-analyzer) <br>
- [API guide](references/api_guide.md) <br>
- [Workflow guide](references/workflow_guide.md) <br>
- [Report template](references/report_template.md) <br>
- [Benchmark data](references/benchmark_data.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with JSON data files, HTML reports, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may write raw_data.json plus generated single-account or multi-account report files under output/.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
