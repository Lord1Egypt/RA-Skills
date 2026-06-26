## Description: <br>
Checks a local QClaw and WorkBuddy queue for task status, completed task results, and result details when a user asks about WorkBuddy outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to answer user questions about whether a WorkBuddy task has completed and to retrieve the latest completed result or a specific task result from the local queue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad result-related prompts may reveal prior WorkBuddy task descriptions, full results, or local attachment paths from the queue. <br>
Mitigation: Use the skill only in trusted local contexts and review retrieved WorkBuddy queue output before sharing it further. <br>
Risk: The skill depends on a separate local qclaw-workbuddy-bridge helper that is outside this artifact. <br>
Mitigation: Install and use the skill only if the local helper is already present and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuboacean/qclaw-result-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with shell command examples and formatted task status or result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task identifiers, task descriptions, result summaries, full result output, error details, or local attachment paths when present in the WorkBuddy queue.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
