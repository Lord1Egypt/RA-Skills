## Description: <br>
Quickly assesses whether a task exceeds LLM limits, then advises what the LLM can do versus what needs expert or tool input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianzhiceng297-boop](https://clawhub.ai/user/tianzhiceng297-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to classify high-risk or out-of-scope requests before execution and route unsafe or restricted subtasks to humans or specialized tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an agent more conservative and add boundary-audit language before answering. <br>
Mitigation: Use it for high-stakes verification, prediction, physical design, legal, medical, financial, or mixed safe and unsafe tasks; skip it for routine text generation, translation, summarization, and simple Q&A. <br>
Risk: Boundary classifications are guidance and do not replace formal verification, professional review, or domain-specific tools. <br>
Mitigation: Route prohibited and restricted subtasks to the responsible human, expert system, formal tool, simulator, or professional reviewer identified by the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianzhiceng297-boop/task-boundary-auditor) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit blocks, routing tables, and concise recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces boundary classifications, task decomposition, risk points, disclaimers, and recommended human/tool handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
