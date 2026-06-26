## Description: <br>
Submits user-provided stories, confessions, thoughts, or selected chat conversations anonymously to a community Feishu form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit a story or confession to the community tree-hole form. It can also prepare a selected chat conversation for submission after anonymization and explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send freeform personal content or chat history to a Feishu form. <br>
Mitigation: Show the exact text to be submitted, anonymize personal identifiers, and require explicit user confirmation before submission. <br>
Risk: Users may not understand that selected content leaves the current chat environment. <br>
Mitigation: Use the skill only when the user intentionally wants content submitted to the Feishu form and disclose the destination before running browser actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/tree-hole) <br>
- [Community Feishu submission form](https://ainewmedia.feishu.cn/share/base/form/shrcn1AeCLxzQdV15UaxAzu2L0e) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and submission guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses agent-browser commands to open, fill, submit, and optionally screenshot the Feishu form.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
