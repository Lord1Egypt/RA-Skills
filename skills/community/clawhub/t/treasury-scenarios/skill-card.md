## Description: <br>
Provides lookup guidance for treasury-system business scenarios, returning process steps, interface combinations, and ASCII flow diagrams for 10 treasury workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbj-bnu](https://clawhub.ai/user/lbj-bnu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Treasury-system developers and analysts use this skill to map business questions about account monitoring, payroll, supplier payments, internal transfers, budget planning, SSO, receipts, balances, and monthly operations to documented scenario flows and interface sequences. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Treasury workflow descriptions include sensitive banking operations and could be mistaken for approval to perform live financial actions. <br>
Mitigation: Use the skill as a reference aid only; require separate authorization, confirmations, and normal business controls before any real banking operation. <br>
Risk: Scenario and interface guidance may be incomplete or stale for a specific treasury deployment. <br>
Mitigation: Confirm process steps, interface codes, and required fields against the current authoritative treasury-system documentation before implementation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lbj-bnu/treasury-scenarios) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Scenario data](artifact/scenarios.json) <br>
- [Interface data](artifact/interfaces.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with numbered process steps, interface sequences, and ASCII flow diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference-only output; it does not access accounts, credentials, files, or networks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
