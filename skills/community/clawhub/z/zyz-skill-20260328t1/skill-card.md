## Description: <br>
基于100个热门TradingView Pine Script指标转换的Python技术分析工具集，提供专业的技术指标计算、分析和可视化功能(20260328V2) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[super-max21](https://clawhub.ai/user/super-max21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to request TradingView technical indicator analysis through a Prana-backed wrapper. It is intended for technical analysis assistance, not as a replacement for independent trading or investment review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, trading strategy details, and optional account, email, or phone values may be sent to a remote Prana service. <br>
Mitigation: Use only in an environment where that data sharing is acceptable, and avoid sending sensitive trading or personal information. <br>
Risk: Fetched API credentials may be written to local configuration files or global OpenClaw environment settings. <br>
Mitigation: Prefer isolated test environments, disable automatic key fetching with PRANA_SKILL_NO_AUTO_API_KEY, and disable local key writes with PRANA_SKILL_SKIP_WRITE_API_KEY when possible. <br>
Risk: The skill is advertised as a local TradingView analysis toolkit but delegates execution to a remote service. <br>
Mitigation: Review the remote-service dependency and trust boundary before deployment, and validate outputs independently before using them for trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/super-max21/zyz-skill-20260328t1) <br>
- [Publisher profile](https://clawhub.ai/user/super-max21) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response from the Prana client; analysis text may appear in response content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Prana API credentials and may persist fetched API keys unless disabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
