## Description: <br>
Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianjin-ren](https://clawhub.ai/user/tianjin-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to force an upfront check for applicable skills before ordinary responses, clarifying questions, or task work. It is intended as a global process-control skill for agents that support skill invocation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly controls agent behavior at the start of every conversation and can over-constrain normal interactions. <br>
Mitigation: Install only when a strict global skill-check workflow is intended, and review whether that workflow fits the target agent environment. <br>
Risk: The required skill checks may slow or distort everyday agent responses, including clarification flows. <br>
Mitigation: Test the skill in a non-critical workspace first and remove or disable it if it interferes with expected agent behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianjin-ren/using-superpowers-tianjin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown process guidance for agent behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, API calls, or data access are described by the artifact.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
