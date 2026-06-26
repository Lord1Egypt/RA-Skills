## Description: <br>
Learns your tool preferences while staying capable of using anything. Adapts to your stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent remember preferred tools, default to known stack choices, and suggest alternatives only when they are meaningfully better. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to rely on outdated, inaccurate, or overly broad saved tool preferences. <br>
Mitigation: Periodically review saved preferences and remove entries that no longer reflect the user's current stack or decision criteria. <br>
Risk: Tool preference notes could accidentally capture sensitive details or lead to use of unfamiliar high-impact tools. <br>
Mitigation: Do not store secrets in preferences, and require confirmation before using unfamiliar or high-impact tools. <br>


## Reference(s): <br>
- [Tool Preference Criteria](criteria.md) <br>
- [Tool Dimensions to Detect](dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown guidance and preference entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; saved preferences should be reviewed before they guide tool choices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
