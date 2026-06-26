## Description: <br>
Operate TradingBoat/TBOT (TBOT runtime stack) via a controlled automation interface (DB-first queries; lifecycle control on explicit request). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PlusGenie](https://clawhub.ai/user/PlusGenie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use TBOT Controller to inspect TBOT SQLite data, retrieve runtime status and logs, and start, stop, or restart a TradingBoat/TBOT stack when explicitly confirmed. It can also generate and send schema-validated TradingView-style webhook JSON to a configured TBOT endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook mode can send authenticated trading signals using local secrets without the promised confirmation guard. <br>
Mitigation: Treat json mode as a real trade-signal send, use paper trading first, confirm live-vs-paper configuration, and provide webhook settings deliberately. <br>
Risk: Runtime discovery or auto-discovered secrets may target a different TBOT directory than the user intended. <br>
Mitigation: Set the intended runtime path and webhook variables explicitly, confirm the resolved runtime before live use, and keep webhook secrets out of transcripts and logs. <br>
Risk: Service control actions can affect a running TBOT stack. <br>
Mitigation: Require explicit user intent and confirmation before start, stop, or restart actions, and prefer read-only status and database inspection for routine checks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PlusGenie/tbot-controller) <br>
- [TBOT Controller Operations Reference](references/ops.md) <br>
- [Alert Webhook JSON Schema](scripts/schema/alert_webhook_schema.json) <br>
- [Reference TBOT Runtime Implementation](https://github.com/PlusGenie/openclaw-on-tradingboat) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, json] <br>
**Output Format:** [Plain text or Markdown with shell commands and schema-validated JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform read-only local TBOT inspection, run docker compose or systemd control commands with explicit confirmation, and send authenticated webhook payloads when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
