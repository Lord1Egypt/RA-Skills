## Description: <br>
Task Delegator routes tool-using requests such as search, file work, code execution, API calls, and data handling to temporary subagents while keeping the main conversation focused on results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EKKOLearnAI](https://clawhub.ai/user/EKKOLearnAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep long, tool-heavy conversations concise by routing searches, file operations, code execution, API calls, and data transformations through temporary workers. It is intended for workflows where concise result reporting matters more than retaining detailed intermediate tool traces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic delegation can reduce visibility into tool-based work and make sensitive actions less explicit. <br>
Mitigation: Require explicit confirmation before file changes, code execution, API mutations, memory writes, or soul.md writes, especially in sensitive projects. <br>
Risk: The skill can persist user or project information without clear consent. <br>
Mitigation: Avoid using it around secrets or sensitive account and project data, and review or tighten memory behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EKKOLearnAI/task-delegator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text, with code blocks or commands when the delegated task calls for them] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes results for the user and may omit intermediate tool details by design.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
