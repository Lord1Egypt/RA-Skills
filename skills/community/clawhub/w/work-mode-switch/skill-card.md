## Description: <br>
Guides an OpenClaw agent through 12 work modes for flexible collaboration, including planning, research, writing, coding, review, self-check, and self-learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jijinbao-code](https://clawhub.ai/user/jijinbao-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to select collaboration modes that shape an agent's response style, confirmation points, and expected deliverables for different task types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic activation can cause the agent to infer a mode from vague language and change behavior unexpectedly. <br>
Mitigation: Prefer explicit mode-switch commands and ask for confirmation when the requested mode or next action is ambiguous. <br>
Risk: Execution, self-check, or self-learning flows may be treated as permission to continue without enough user confirmation. <br>
Mitigation: Review the skill before installation and require explicit user approval before file changes, system changes, or autonomous follow-up work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jijinbao-code/work-mode-switch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with mode-specific checklists, trigger phrases, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure documentation skill; no executable code is included.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter and package.json show 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
