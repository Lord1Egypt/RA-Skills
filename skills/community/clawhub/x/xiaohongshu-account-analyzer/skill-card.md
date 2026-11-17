## Description:

深度拆解小红书账号，输出七维度量化评分诊断报告与可导出HTML；当用户提供小红书号进行账号诊断、rednote分析、账号健康度评估、商业价值评估、多账号对比或制定优化策略时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, MCN operators, brand marketers, and competitive analysts use this skill to evaluate Xiaohongshu accounts, compare multiple accounts, assess commercial value, and generate optimization recommendations from RedFox account data plus web context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an API key and Xiaohongshu account data through RedFox.

Mitigation: Install only when RedFox is an acceptable account-data provider, configure REDFOX_API_KEY through environment variables, and avoid sensitive or private account data unless the deployment environment is trusted.

Risk: Generated HTML reports may be unsafe when populated from untrusted account data.

Mitigation: Treat generated HTML as untrusted unless the input data and viewing environment are controlled, and review generated reports before sharing or opening them broadly.

Risk: The security review states the skill needs review before use because TLS verification and HTML escaping should be fixed.

Mitigation: Review transport security and HTML escaping before deployment, and do not rely on generated reports for sensitive workflows until those issues are resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/xiaohongshu-account-analyzer)
- [API guide](references/api_guide.md)
- [Workflow guide](references/workflow_guide.md)
- [Report template guide](references/report_template.md)
- [Benchmark data](references/benchmark_data.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox service](https://redfox.hk?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic reports, generated HTML report files, JSON report data, and shell commands for local report generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may process Xiaohongshu account IDs and account analytics data.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
