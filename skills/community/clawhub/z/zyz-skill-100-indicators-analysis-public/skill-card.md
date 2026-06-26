## Description: <br>
基于100个热门TradingView Pine Script指标转换的Python技术分析工具集，提供专业的技术指标计算、分析和可视化功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[super-max21](https://clawhub.ai/user/super-max21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users and developers can invoke a Prana-hosted TradingView indicator analysis skill to request technical indicator calculation, analysis, or visualization through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and task data are sent to the configured Prana base URL for remote execution. <br>
Mitigation: Use the skill only with data approved for the configured Prana service, and set NEXT_PUBLIC_URL to a trusted endpoint. <br>
Risk: First-run setup may fetch and store a Prana API key under config/api_key.txt. <br>
Mitigation: Use PRANA_SKILL_NO_AUTO_API_KEY=1 to disable automatic key provisioning or PRANA_SKILL_SKIP_WRITE_API_KEY=1 to avoid local key storage; prefer environment-provided credentials for managed deployments. <br>
Risk: The artifact is a Prana wrapper and does not include the underlying indicator implementation. <br>
Mitigation: Treat outputs as remote service results and review technical or financial analysis before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/super-max21/zyz-skill-100-indicators-analysis-public) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Skill manifest](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON response containing Prana agent-run result content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include thread_id and recovery metadata for multi-turn or long-running Prana calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
