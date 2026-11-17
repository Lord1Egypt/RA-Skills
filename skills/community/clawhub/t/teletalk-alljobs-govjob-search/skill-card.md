## Description:

Search Bangladesh government jobs from the Teletalk AllJobs API, filter out excluded keywords, present matching jobs, and track applied job IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sazidulalam47](https://clawhub.ai/user/sazidulalam47)

### License/Terms of Use:

MIT-0

## Use Case:

External users looking for Bangladesh government jobs use this skill to search Teletalk AllJobs by keyword, exclude unwanted role terms, review active openings, and track job IDs they confirm as applied.

### Deployment Geography for Use:

Bangladesh

## Known Risks and Mitigations:

Risk: The skill stores the search keyword, excluded terms, and confirmed applied job IDs inside the skill folder.

Mitigation: Review or clear the local data files before sharing the skill folder or running it in a shared environment.

Risk: The search keyword is sent to the Teletalk AllJobs API.

Mitigation: Use only search terms appropriate to send to that external service and avoid sensitive personal data.

## Reference(s):

- [Teletalk AllJobs published jobs search API](https://alljobs.teletalk.com.bd/api/v1/published-jobs/search)
- [ClawHub skill page](https://clawhub.ai/sazidulalam47/skills/teletalk-alljobs-govjob-search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON job lists and concise Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters excluded title keywords, omits past-deadline jobs, and records confirmed applied job IDs locally.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
