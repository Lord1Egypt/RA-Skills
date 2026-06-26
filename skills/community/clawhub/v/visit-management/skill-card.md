## Description: <br>
Visit Management generates visit plans and reminders from a local Excel customer ledger using service history, tenant level, renewal warnings, fee risk, repair records, and manual or scheduled triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property and customer-service operations employees use this skill to plan tenant visits, generate daily reminders, track visit closure, and prioritize follow-up based on customer records, payment status, repair history, and renewal timing. <br>

### Deployment Geography for Use: <br>
Global, subject to local data-access and workplace messaging compliance. <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local customer Excel ledger and writes generated plan, reminder, report, history, and backup files that may contain sensitive customer and tenant context. <br>
Mitigation: Install and run it only on machines authorized to access the workbook, and restrict filesystem permissions for the source workbook and generated JSON or Excel outputs. <br>
Risk: Reminder content may be delivered to WeCom or similar workplace chat channels, exposing customer context to unintended recipients if webhook or chat permissions are misconfigured. <br>
Mitigation: Confirm recipient groups before enabling delivery, protect and rotate webhook keys, and review generated reminder content before automated sends. <br>
Risk: Evidence guidance identifies a unit-number versus tenant-name matching bug that could send or use the wrong customer context. <br>
Mitigation: Fix and test customer matching before relying on automated planning, reminders, or outbound messages. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/perrykono-debug/visit-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese text, Markdown reminders, JSON plan/reminder/report files, and Python command-line output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and may update a local Excel workbook; writes local JSON outputs under the visit-management skill directory; formats reminders for manual review or configured workplace-chat delivery.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
