## Description: <br>
Qclaw Task Submitter helps an agent route complex QClaw requests to WorkBuddy by submitting task descriptions to a local WorkBuddy queue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QClaw users and operators use this skill to identify complex document generation, analysis, file-processing, and automation requests that should be handed to WorkBuddy. The skill guides the agent to submit those requests through the WorkBuddy queue and report task status back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can hand broad local file, document, analysis, and automation tasks to an immediate executor without clear confirmation, scope limits, or cancellation guidance. <br>
Mitigation: Confirm the exact task, files, folders, and schedule before submission; avoid secrets or sensitive documents unless intended; and ensure the user knows how to cancel or undo WorkBuddy actions. <br>
Risk: The skill depends on a local WorkBuddy bridge helper to execute queued tasks. <br>
Mitigation: Install only when the local WorkBuddy bridge is trusted and its qclaw_queue.py helper has been inspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuboacean/qclaw-task-submitter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise user-facing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WorkBuddy task identifiers, status checks, and result retrieval commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
