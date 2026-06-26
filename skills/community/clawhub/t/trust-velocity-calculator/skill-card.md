## Description: <br>
Helps calculate the rate at which trust in a skill or agent is decaying by combining time elapsed since last verification with the rate of change in behavior, permissions, or dependencies, producing a trust velocity score that predicts when a trusted credential will become unreliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to estimate when a skill or agent should be re-reviewed based on elapsed verification time, change velocity, and verification coverage lag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trust velocity scores are model-based guidance and can be mistaken for evidence of compromise. <br>
Mitigation: Use the report as an advisory signal, calibrate decay parameters to the environment, and verify input data independently before acting. <br>
Risk: curl or python3 use could inspect unintended sources if the agent is given broad targets. <br>
Mitigation: Allow tool use only for user-specified skills or sources that are intended for analysis, and review external targets before fetching them. <br>
Risk: Frequent version changes can inflate trust decay even when the changed surface is low impact. <br>
Mitigation: Review the change velocity breakdown and distinguish meaningful behavior, permission, endpoint, or dependency changes from cosmetic releases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/trust-velocity-calculator) <br>
- [Publisher profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown trust velocity report with text-based scores, projections, change analysis, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference curl and python3 when the user asks the agent to analyze user-specified skills or sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
