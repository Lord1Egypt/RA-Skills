## Description: <br>
Decision forecasting engine based on Menos architecture and swarm intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shewingong](https://clawhub.ai/user/shewingong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and decision-support users can use this skill to simulate multi-agent debate around a decision or query and receive probabilistic scenario guidance before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use stored memory or ledger context during forecasting without clearly documented boundaries. <br>
Mitigation: Review what L1 Physical Ledger and L2 Long-term Memory context is available before running forecasts, and avoid using sensitive personal, financial, or business information unless context access is documented and acceptable. <br>
Risk: The skill claims subagent execution for Skeptic, Optimist, and Strategist agents without documenting what each subagent can access. <br>
Mitigation: Run only in environments where subagent permissions can be reviewed or constrained, and require approval before sharing sensitive context with spawned agents. <br>
Risk: Forecast output may influence financial or business decisions even though the evidence describes it as probabilistic guidance. <br>
Mitigation: Treat forecasts as decision-support material, not authoritative advice, and require independent review before acting on high-impact recommendations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JSON tool result and human-facing forecast report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The tool accepts a query plus an optional mode of light, standard, or sovereign.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
