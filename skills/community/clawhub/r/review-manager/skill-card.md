## Description: <br>
고객사 리뷰 수집, 자동 답글, 알림, 리포트 통합 관리를 위해 네이버플레이스, 구글, 배민, 쿠팡 리뷰 모니터링과 감성 분석, 경쟁사 비교를 지원합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Business operators and support teams use this skill to collect customer reviews across configured commerce and local-business platforms, generate draft replies, detect negative reviews, and produce weekly or competitor comparison reports. Developers can configure the Node-based scripts for scheduled review monitoring and Discord notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord alerts and reports can expose private customer review content. <br>
Mitigation: Use a private Discord destination, minimize or redact review text before sending, and define retention rules for locally stored review and report data. <br>
Risk: Shell-built Discord send commands in alert and report scripts create a local command-execution risk. <br>
Mitigation: Replace execSync command-string construction with a safe API call or execFile/spawn argument arrays, and validate Discord channel IDs and message payloads. <br>
Risk: Review collection may require authenticated browser sessions for some platforms. <br>
Mitigation: Use only explicitly authorized accounts and keep account scope separate for each store or platform integration. <br>
Risk: Automatically generated replies may be inaccurate or inappropriate for a customer complaint. <br>
Mitigation: Review generated replies before applying them, especially for low-rating or keyword-triggered complaints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/review-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mupengi-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with Node shell commands, JSON configuration, generated reply JSON, alert state JSON, and review/report JSON outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and a local review-manager config.json; Discord delivery depends on an authorized OpenClaw message command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
