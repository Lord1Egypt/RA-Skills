## Description:

Direct Todoist API integration via curl/jq. Lightweight, reliable, and uses working v1/v2 endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitsujy](https://clawhub.ai/user/nitsujy)

### License/Terms of Use:


## Use Case:

Developers and productivity users use this skill to generate Todoist API requests for listing, creating, completing, and reviewing tasks, projects, and sections when the Todoist CLI is unavailable or failing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands use TODOIST_API_TOKEN and can access the user's Todoist account.

Mitigation: Keep the token secret, use the minimum account access needed, and review each generated curl command before running it.

Risk: Create and close task operations can change the wrong Todoist item if task or project IDs are incorrect.

Mitigation: Verify task, project, and section IDs before executing account-changing requests.

## Reference(s):

- [Todoist Developer Documentation](https://developer.todoist.com)
- [ClawHub skill page](https://clawhub.ai/nitsujy/skills/todoist-api-rest)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TODOIST_API_TOKEN for generated commands.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
