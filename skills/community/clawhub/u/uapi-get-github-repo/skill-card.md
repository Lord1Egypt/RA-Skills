## Description:

Uses UAPI's GET /github/repo endpoint to help an agent look up GitHub repository information and explain required parameters, call behavior, and response codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when a user asks for GitHub repository details through UAPI. It guides the agent to confirm the required repo parameter, call GET /github/repo, and explain successful or failed responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording such as 'repo' can invoke the skill when the user did not clearly ask for a GitHub repository lookup.

Mitigation: Confirm the user wants GitHub repository information before calling GET /github/repo.

Risk: Returned collaborator, maintainer, and email fields may expose public personal data.

Mitigation: Use those fields only for the user's stated repository lookup and avoid bulk harvesting or unsolicited outreach.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [GET /github/repo Operation](references/operations/get-github-repo.md)
- [Social Category Interfaces](references/resources/Social.md)
- [UAPI Base URL](https://uapis.cn/api/v1)
- [UAPI](https://uapis.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown guidance with endpoint, parameter, response-code, and result-summary details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public repository metadata returned by UAPI, including collaborator, maintainer, and email fields when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
