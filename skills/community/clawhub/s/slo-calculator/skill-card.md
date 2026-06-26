## Description: <br>
Calculates SLO/SLA error budgets, allowed downtime, burn rates, uptime metrics, target comparisons, and reference tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SREs, platform engineers, and developers use this skill to select and run local SLO calculator commands for error-budget, burn-rate, uptime, and availability-target analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent toward running a local Python command-line calculator. <br>
Mitigation: Review proposed commands before execution and run them in a least-privileged workspace. <br>
Risk: SLO and SLA results depend on user-provided inputs and the calculator's fixed period assumptions. <br>
Mitigation: Confirm period definitions, downtime inputs, and contractual SLA terms before using results for operational or customer-facing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/slo-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands; calculator output can be text, JSON, or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure Python stdlib CLI; accepts SLO targets, period/window selections, durations, and output format flags.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact script reports VERSION = 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
