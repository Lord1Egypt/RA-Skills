## Description: <br>
Fetches recent Double Color Ball lottery history, applies a Contextual Quantum-like Bayesian Network simulation, and prepares Top 10 recommended combinations with optional Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rix-zhang](https://clawhub.ai/user/rix-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a concise SSQ lottery prediction report from recent public draw history and optionally deliver it to a configured Feishu group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lottery recommendations could be mistaken for reliable investment or gambling advice. <br>
Mitigation: Treat predictions as speculative entertainment or mathematical research, and keep the report's cautionary language visible. <br>
Risk: A configured Feishu group ID can route the generated report to a group chat. <br>
Mitigation: Confirm FEISHU_SSQ_GROUP_ID points to the intended group before enabling automatic delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rix-zhang/ssq-prediction) <br>
- [SSQ historical data source](https://datachart.500.com/ssq/history/newinc/history.php?start=24001&end=24200) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with optional Feishu delivery command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Top 10 recommended lottery combinations; sends to Feishu only when FEISHU_SSQ_GROUP_ID is configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
