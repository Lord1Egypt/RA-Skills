## Description: <br>
A personalized writing style memory skill that loads a user's style rules, applies them to writing tasks, and learns updated preferences from user edits and feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanjiaming](https://clawhub.ai/user/shanjiaming) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Writers, editors, translators, and agents use this skill to adapt generated or revised text to a user's evolving writing preferences. It is intended for writing, rewriting, polishing, tone adjustment, and translation tasks where style consistency matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save local copies and git history of writing drafts and style preferences, which can retain sensitive content. <br>
Mitigation: Avoid sensitive, client, legal, medical, or workplace documents unless explicit approval is required before each snapshot or style-memory update; periodically review or delete ~/.writing-style-iterator/. <br>
Risk: The workflow encourages the agent to update user files and style memory with limited prior confirmation. <br>
Mitigation: Require confirmation before file writes and style-memory changes in higher-risk contexts, and review diffs or git history before relying on updated drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shanjiaming/writing-style-iterator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local writing drafts and style memory files when the workflow is followed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
