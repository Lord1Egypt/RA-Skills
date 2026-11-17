## Description:

Manage Userorbit resources via the public API. Create and manage feedback, announcements, roadmap topics, help center articles, boards, tags, subscribers, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[middlerange](https://clawhub.ai/user/middlerange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a Userorbit workspace through authenticated API calls for feedback, announcements, roadmaps, help center content, subscribers, and related resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API access can affect customer-facing content, project settings, and subscriber data.

Mitigation: Use a least-privilege Userorbit API key if available and require explicit confirmation before deletes, publishes, subscriber changes, or project-level actions.

Risk: The required API key and team ID are supplied through environment variables.

Mitigation: Keep USERORBIT_API_KEY and USERORBIT_TEAM_ID private, avoid logging them, and rotate credentials if exposure is suspected.

## Reference(s):

- [Userorbit API Reference](references/api.md)
- [Userorbit API Base URL](https://api.userorbit.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/middlerange/skills/userorbit)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with inline curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires USERORBIT_API_KEY and USERORBIT_TEAM_ID environment variables.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
