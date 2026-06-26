## Description: <br>
Integrate with Todoist task management using natural language for listing, creating, updating, completing, and deleting tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hail2skins](https://clawhub.ai/user/hail2skins) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Todoist tasks and projects through conversational requests or direct CLI commands. It supports task listing, natural-language task creation, task updates, completion, deletion, project lookup, filtering, priorities, due dates, and timezone-aware today filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Todoist API token to create, update, complete, and delete tasks in the user's Todoist account. <br>
Mitigation: Install only where that Todoist account access is intended, keep TODOIST_API_KEY private, and require confirmation before completing, updating, or deleting tasks from ambiguous natural-language requests. <br>
Risk: Date filters such as today can produce unexpected results if the runtime timezone does not match the user's intended timezone. <br>
Mitigation: Set the TZ environment variable when date-sensitive task filtering matters. <br>
Risk: Installation examples include sudo-based system paths that may grant broader file-system privileges than needed. <br>
Mitigation: Prefer the documented no-sudo user install path when possible. <br>


## Reference(s): <br>
- [Todoist API v1 Reference](references/api.md) <br>
- [Todoist REST API documentation](https://developer.todoist.com/api/v1/) <br>
- [Todoist developer token settings](https://todoist.com/app/settings/integrations/developer) <br>
- [Todoist Sync API documentation](https://developer.todoist.com/sync/v9/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from the Todoist CLI script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TODOIST_API_KEY for Todoist account access; TZ is optional for timezone-sensitive date filtering.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
