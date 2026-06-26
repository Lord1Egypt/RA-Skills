## Description: <br>
Your agent learns to think like you. Captures your direction system, makes decisions as you would, guides all processes toward your goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to help an agent progressively learn their values, goals, decision criteria, boundaries, and resource preferences so it can make better-aligned decisions over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a persistent local profile of the user's values, goals, boundaries, preferences, and decision patterns. <br>
Mitigation: Review ~/self-direction/ regularly, avoid recording secrets or sensitive health, financial, legal, or personal details, and define retention and deletion rules before routine use. <br>
Risk: The skill can reuse inferred preferences or pass them to sub-agents, which may create misalignment if confidence is low or consent is unclear. <br>
Mitigation: Require explicit approval before using inferred preferences for important actions or sharing direction frames with sub-agents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/self-direction) <br>
- [Skill Homepage](https://clawic.com/skills/self-direction) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Memory Template](artifact/memory-template.md) <br>
- [Evidence Logging Guide](artifact/evidence.md) <br>
- [Direction Transmission Guide](artifact/transmission.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance and local profile templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local direction, evidence, confidence, conflict, and transmission notes under ~/self-direction/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
