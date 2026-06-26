## Description: <br>
Guides an agent to clarify vague development requests, confirm design direction in small steps, and plan implementation before coding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipoon](https://clawhub.ai/user/sipoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a feature, module, or project request is under-specified. It helps turn a vague request into clarified requirements, a concise design draft, and a phased implementation plan before work begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly auto-triggers on unclear development requests, which can slow direct execution when the user expects an immediate change. <br>
Mitigation: Use it when requirements are ambiguous, and skip or override the planning gate for simple fixes, pure reading, pure search, or already well-defined tasks. <br>
Risk: The skill can hand work to downstream skills after planning, which may change the agent workflow. <br>
Mitigation: Review the proposed handoff before allowing the agent to continue into implementation or multi-skill coordination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sipoon/sipoon-brainstorming) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with questions, design drafts, and implementation plan tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to ask a few clarifying questions at a time and wait for user confirmation before proceeding.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
