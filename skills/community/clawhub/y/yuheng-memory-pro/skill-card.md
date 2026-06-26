## Description: <br>
Memory Pro proactively distills important knowledge from conversations and notes into structured long-term memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to identify durable preferences, decisions, lessons, project knowledge, and cross-domain insights, then save them as structured long-term memory notes for future sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can proactively store private conversation details in long-term memory. <br>
Mitigation: Require the agent to show the exact note content and destination before saving, and exclude secrets or sensitive personal details. <br>
Risk: The skill may commit saved notes to Git without clear user approval. <br>
Mitigation: Approve each file write and Git commit explicitly before execution. <br>
Risk: Sensitive or outdated memories may persist after they are no longer appropriate. <br>
Mitigation: Periodically review, edit, or remove saved notes and related Git history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horizoncove/yuheng-memory-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown notes with optional shell command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update long-term memory files and propose Git archival commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
