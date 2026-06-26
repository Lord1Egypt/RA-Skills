## Description: <br>
Generates structured, engineering-grade prompts for technical software, infrastructure, architecture, DevOps, AI systems, testing, refactoring, automation, and integration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZoriyAI](https://clawhub.ai/user/ZoriyAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a technical request into a concise, structured prompt with role, goal, constraints, phases, deliverables, and validation criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts can carry ClaudeKit Engineer and Context7 defaults into another agent even when those defaults are not desired. <br>
Mitigation: Review the generated prompt before reuse and remove those defaults when they do not fit the target workflow. <br>
Risk: Prompt output may be less appropriate for non-technical requests. <br>
Mitigation: Use this skill for technical prompt generation and review outputs for fit before passing them to another agent. <br>


## Reference(s): <br>
- [Prompt examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/ZoriyAI/zoriy-prompt-engineer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill selects QUICK, FULL, or MASTER prompt structure based on task scope and defaults to FULL when scope is not clearly small or large.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
