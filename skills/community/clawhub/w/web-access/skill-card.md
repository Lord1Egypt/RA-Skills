## Description:

Helps agents search and read websites and navigate interactive or login-required pages through a Chromium browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eze-is](https://clawhub.ai/user/eze-is)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to research websites, retrieve page content, and complete browser interactions that need a logged-in session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser control can read private pages and perform actions in logged-in accounts.

Mitigation: Use a separate browser profile with limited accounts and authorize sensitive actions before execution.

Risk: The skill can inspect local browser history and bookmarks and attach local files to upload controls.

Mitigation: Limit access to the browser profile and files needed for the task; review requested searches and uploads.

Risk: The local browser-control service can remain active after a task finishes.

Mitigation: Stop the proxy when it is no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/eze-is/skills/web-access)
- [Project homepage listed in skill metadata](https://github.com/eze-is/web-access)
- [Browser API reference](references/cdp-api.md)
- [Version 2.6 migration guide](references/migration-2.6.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Natural-language responses with extracted web content and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may reflect content from authenticated browser sessions.]

## Skill Version(s):

2.6.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
