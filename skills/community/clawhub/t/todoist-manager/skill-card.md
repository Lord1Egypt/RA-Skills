## Description:

Manage Todoist tasks, projects, labels, and comments via the todoist CLI wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreisuslov](https://clawhub.ai/user/andreisuslov)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to have an agent manage Todoist tasks, projects, sections, labels, and comments through the Todoist CLI using their Todoist API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Todoist CLI uses a Todoist API token that can access the user's account.

Mitigation: Install only when the user is comfortable granting CLI access to that token, and keep the token in an environment variable rather than writing it into prompts or shared files.

Risk: Account-changing commands can create, update, complete, reopen, or delete Todoist tasks, projects, sections, labels, and comments.

Mitigation: Before destructive or account-changing actions, show the exact Todoist target and operation and ask for explicit confirmation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Todoist CLI commands require TODOIST_API_TOKEN, curl, and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
