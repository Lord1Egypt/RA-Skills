## Description: <br>
Integrates OKX API workflows for spot and contract trading, asset management, risk control, and real-time market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danihe001](https://clawhub.ai/user/danihe001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide OKX spot and contract trading workflows, including balance checks, order placement, risk checks, and market-data retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes live-looking OKX account and API details. <br>
Mitigation: Treat any displayed credential as exposed, rotate real credentials, and store secrets only in environment variables or a secret manager. <br>
Risk: The skill supports real crypto trading and fund movement workflows. <br>
Mitigation: Prefer read-only or sandbox mode by default, disable transfers unless required, and require explicit confirmation for every trade or fund movement. <br>
Risk: The security review found insufficient user-confirmation safeguards for trading actions. <br>
Mitigation: Review the skill carefully before installing and require operator approval before any order, transfer, or risk-control change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danihe001/temp-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline function calls and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe OKX trading operations that require explicit user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
