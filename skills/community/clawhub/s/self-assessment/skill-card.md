## Description: <br>
Guides an agent to assess its capabilities, available skills, memory, and task fit before accepting, caveating, or redirecting a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvianEvans](https://clawhub.ai/user/EvianEvans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent developers and multi-agent operators use this skill to make agents perform a structured self-assessment before accepting a TASK_OFFER. It helps the agent compare task requirements against its identity, skills, and past experience, then return an acceptance, caveat, reassignment suggestion, or skill-gap response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install missing skills and update persistent identity information, which can change future agent behavior without a clear approval step. <br>
Mitigation: Require explicit user approval before installing skills or modifying IDENTITY.md, and review the proposed changes before they are applied. <br>
Risk: Self-assessment output can overstate task fit or produce misleading reassignment guidance. <br>
Mitigation: Review the assessment before acting on ACCEPT, ACCEPT_WITH_CAVEAT, SUGGEST_REASSIGN, or SKILL_GAP decisions in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EvianEvans/self-assessment) <br>
- [Publisher profile](https://clawhub.ai/user/EvianEvans) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON-like decision responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ACCEPT, ACCEPT_WITH_CAVEAT, SUGGEST_REASSIGN, and SKILL_GAP response patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
