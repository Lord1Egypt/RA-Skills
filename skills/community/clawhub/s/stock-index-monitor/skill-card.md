## Description: <br>
A stock and index monitoring skill that defines configurable alert rules for cost thresholds, price moves, volume changes, moving-average crosses, RSI, gaps, and trailing stops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quant520](https://clawhub.ai/user/quant520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure market-monitoring alerts for stocks, ETFs, and gold instruments, then review generated alert messages and analysis prompts as decision-support material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release references a background control.sh script that is not included in the artifact, so runtime behavior, data access, logging, and stop behavior cannot be reviewed from the package. <br>
Mitigation: Inspect the actual script locally before running it, including data sources contacted, logs written, holdings or cost-basis storage, and whether the stop command reliably terminates the process. <br>
Risk: The skill generates trading alerts and analysis suggestions that may be delayed, incorrect, or unsuitable for a user's financial situation. <br>
Mitigation: Treat alerts and suggestions as research prompts only, verify them against trusted market data, and do not use them as standalone investment advice or automated trading instructions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python configuration examples, shell commands, and alert message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes financial monitoring examples and should be treated as research support, not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
