## Description:

Raindrop.io bookmark and collection manager for a local OpenClaw workspace. Use when the user wants to validate Raindrop auth, inspect their account, list or search bookmark collections, create/update/delete collections, save or edit bookmarks, bulk import/export bookmark links, or run local Raindrop.io OAuth flows without exposing secrets inside the published skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Raindrop.io collections and bookmarks from an agent-driven local OpenClaw workspace. It supports authentication checks, collection and bookmark inspection, OAuth token flows, import, export, and account-changing create/update/delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Raindrop.io OAuth tokens and may save credentials to a local env file.

Mitigation: Prefer environment variables or a short-lived test token, avoid passing secrets on the command line, and check permissions on any ~/.openclaw/raindrop.env file.

Risk: Delete, update, and import commands can change or remove Raindrop.io account data without an extra confirmation step.

Mitigation: Validate authentication with whoami, inspect target collections and bookmarks first, confirm IDs before account-changing commands, and export data before bulk changes.

## Reference(s):

- [API notes](references/api-notes.md)
- [Optional local env file example](references/env-example.md)
- [Raindrop.io REST API base](https://api.raindrop.io/rest/v1)
- [Raindrop.io OAuth authorize endpoint](https://raindrop.io/oauth/authorize)
- [Raindrop.io OAuth token endpoint](https://raindrop.io/oauth/access_token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files, API calls]

**Output Format:** [Markdown guidance with shell commands; CLI commands emit JSON or CSV and can write JSON, TXT, or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided Raindrop.io credentials and can perform account-changing create, update, delete, import, and export workflows.]

## Skill Version(s):

0.2.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
