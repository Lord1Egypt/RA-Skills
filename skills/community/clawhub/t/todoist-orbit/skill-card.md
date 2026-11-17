## Description:

Operate Todoist through a deterministic Python CLI backed by the Todoist REST API for listing, creating, updating, moving, completing, deleting, resolving, and commenting on Todoist tasks and related objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myx0m0p](https://clawhub.ai/user/myx0m0p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need deterministic Todoist automation through explicit CLI commands instead of natural-language task parsing. It supports Todoist tasks, projects, sections, labels, comments, uploads, and concurrent lookup resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, move, close, reopen, archive, delete, and comment on Todoist data using the supplied API token.

Mitigation: Review destructive commands before execution and prefer explicit Todoist IDs for write operations.

Risk: Uploads and stdin/file comments may store local file content or generated text in Todoist.

Mitigation: Upload only files and comment bodies that are intended to be stored in the Todoist account.

Risk: The skill depends on TODOIST_API_KEY and acts with the permissions of that token.

Mitigation: Install only when the agent should operate on the target Todoist account, and keep the API token in environment configuration rather than command text.

Risk: Some Todoist features, especially uploads and comments, may vary by account or workspace plan.

Mitigation: Handle API errors as capability or plan limits and confirm important changes in Todoist when needed.

## Reference(s):

- [Todoist Orbit API notes](references/api-notes.md)
- [Todoist REST API base](https://api.todoist.com/api/v1)
- [Todoist developer token settings](https://todoist.com/app/settings/integrations/developer)
- [ClawHub release page](https://clawhub.ai/myx0m0p/skills/todoist-orbit)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TODOIST_API_KEY; --pretty enables indented JSON output.]

## Skill Version(s):

0.1.6 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
