## Description: <br>
Guides an agent through persistent Japanese-language debugging with escalation prompts, structured hypothesis checks, source reading, search, and verification steps after repeated failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanweai](https://clawhub.ai/user/tanweai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators can use this skill to push an assistant toward structured troubleshooting after repeated failures, including listing attempts, testing alternate hypotheses, reading source context, searching references, and reporting verified findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can pressure an agent to continue acting across broad task types when it may need to pause, clarify, refuse, or escalate. <br>
Mitigation: Use it with explicit task boundaries that preserve the agent's ability to stop, ask clarifying questions, refuse unsafe work, and recommend human handling in high-stakes situations. <br>
Risk: Its strong persistence style may encourage excessive action after repeated failures. <br>
Mitigation: Require the agent to state verified facts, ruled-out possibilities, remaining uncertainty, and a bounded next step before continuing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tanweai/pua-debugging-ja) <br>
- [Homepage](https://openpua.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with checklists, investigation steps, commands when useful, and verification notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No fixed output schema; responses are task-dependent troubleshooting plans, findings, and handoff notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
