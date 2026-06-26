## Description: <br>
Routes simple Claude requests to Haiku and escalates complex requests to Sonnet to reduce model costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterokase42](https://clawhub.ai/user/peterokase42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to classify request complexity and route Claude work between a lower-cost default model and a stronger model for complex tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complex or uncertain requests may be forwarded to a spawned Sonnet session with the full task content. <br>
Mitigation: Use only where automatic model handoff is intended, and avoid sensitive prompts unless forwarding the full task content is acceptable. <br>
Risk: Escalation can increase model costs without a separate confirmation step. <br>
Mitigation: Monitor usage and costs, and disable or adjust the skill where automatic escalation is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peterokase42/save-money) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text] <br>
**Output Format:** [Markdown guidance with model-routing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a spawned Sonnet session for complex or uncertain tasks.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
