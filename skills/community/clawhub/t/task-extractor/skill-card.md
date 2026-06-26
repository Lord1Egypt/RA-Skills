## Description: <br>
Extract, track, and verify completion of multiple tasks from a single user message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to keep compound user requests organized by extracting multi-item prompts into a numbered queue, tracking execution, and reporting completion status per task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate broadly and push the agent toward execution without clear approval boundaries. <br>
Mitigation: Review extracted tasks before execution and require explicit confirmation for sends, deployments, configuration changes, and sub-agent delegation. <br>
Risk: Task details may be written to a persistent TASK_QUEUE.md file in the workspace. <br>
Mitigation: Avoid using the skill with secrets, personal data, or confidential project details, and delete the queue file when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dodge1218/task-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown task queue and status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update TASK_QUEUE.md in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
