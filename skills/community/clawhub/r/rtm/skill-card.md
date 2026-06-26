## Description: <br>
Manage Remember The Milk tasks: list, add, complete, delete, search, prioritize, tag, move, and annotate tasks with notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxdraki](https://clawhub.ai/user/maxdraki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage tasks in a linked Remember The Milk account, including reading task lists and performing task updates when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Remember The Milk API credentials and stores an auth token at ~/.rtm_token, which can grant account access if exposed. <br>
Mitigation: Keep RTM_API_KEY and RTM_SHARED_SECRET in skill configuration, restrict token file permissions, and remove ~/.rtm_token when persistent access is no longer needed. <br>
Risk: The skill requests delete-level Remember The Milk permission so it can delete tasks or notes. <br>
Mitigation: Review delete and note-deletion actions before execution, and use a dedicated API key or account scope where practical. <br>


## Reference(s): <br>
- [Remember The Milk API Keys](https://www.rememberthemilk.com/services/api/keys.rtm) <br>
- [Remember The Milk Advanced Search](https://www.rememberthemilk.com/help/answers/search/advanced.rtm) <br>
- [Remember The Milk REST API](https://api.rememberthemilk.com/services/rest/) <br>
- [Remember The Milk Auth](https://www.rememberthemilk.com/services/auth/) <br>
- [ClawHub Skill Page](https://clawhub.ai/maxdraki/rtm) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/maxdraki) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and plain text task output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task output includes list, series, task, and note identifiers needed for follow-up write operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
