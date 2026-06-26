## Description: <br>
Automatically evaluates agent outputs for clarity, conciseness, actionability, and structure using a lightweight rule-based quality gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leic8959-sudo](https://clawhub.ai/user/leic8959-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill as a pre-delivery quality gate to check whether an agent response is clear, structured, concise, and actionable before sending it to a user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rule-based quality gate can reject acceptable responses or approve weak responses because it relies on lightweight heuristics rather than semantic review. <br>
Mitigation: Keep the gate advisory or set explicit thresholds and manual review paths for safety-critical, factual, legal, medical, financial, or multilingual output. <br>


## Reference(s): <br>
- [Self Review ClawHub page](https://clawhub.ai/leic8959-sudo/self-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with pass/fail status and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exit code 0 when approved and 1 when the output needs improvement.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
