## Description:

Manage Remember The Milk tasks: list, add, complete, delete, search, prioritize, tag, move, and annotate tasks with notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxdraki](https://clawhub.ai/user/maxdraki)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage Remember The Milk tasks and notes from a command-line workflow, including read operations and account-modifying actions such as completion, deletion, tagging, moving, and note updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The saved RTM token at ~/.rtm_token grants persistent access to the linked Remember The Milk account.

Mitigation: Restrict the token file to owner-only permissions after authentication and remove it when persistent access is no longer needed.

Risk: The skill requests delete permission so it can delete tasks and notes.

Mitigation: Install it only when account management, including deletion, is intended; use a dedicated RTM API key where practical.

Risk: Runtime API credentials are required through RTM_API_KEY and RTM_SHARED_SECRET.

Mitigation: Provide credentials through the skill environment configuration instead of hardcoding them in prompts, scripts, or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxdraki/skills/rtm)
- [Remember The Milk API keys](https://www.rememberthemilk.com/services/api/keys.rtm)
- [Remember The Milk advanced search syntax](https://www.rememberthemilk.com/help/answers/search/advanced.rtm)
- [Remember The Milk REST API endpoint](https://api.rememberthemilk.com/services/rest/)
- [Remember The Milk authorization endpoint](https://www.rememberthemilk.com/services/auth/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task listings include Remember The Milk list, series, task, and note IDs needed for follow-up write operations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
