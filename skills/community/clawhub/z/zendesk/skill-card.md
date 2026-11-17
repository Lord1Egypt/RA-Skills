## Description:

Manage Zendesk tickets, users, and support workflows with API integration and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Support teams, developers, and authorized operations staff use this skill to create and update Zendesk tickets, search support history, retrieve user details, and automate support workflows through Zendesk API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable Zendesk API token may be saved in a local Markdown memory file.

Mitigation: Use a dedicated least-privilege Zendesk API identity and prefer a secure secret manager or tightly controlled environment variables over storing the token in ~/zendesk/memory.md.

Risk: State-changing Zendesk actions can update tickets, public comments, users, macros, or bulk records.

Mitigation: Confirm every state-changing action with the user and summarize the affected records before execution.

Risk: Ticket content, user data, and search queries are sent to the Zendesk API.

Mitigation: Use the skill only with authorized Zendesk API access and avoid sending unrelated customer data in searches, comments, or exports.

## Reference(s):

- [ClawHub Zendesk skill listing](https://clawhub.ai/ivangdavila/skills/zendesk)
- [Skill homepage](https://clawic.com/skills/zendesk)
- [Zendesk API endpoint pattern](https://{subdomain}.zendesk.com/api/v2/*)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Markdown]

**Output Format:** [Markdown guidance with shell command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized Zendesk subdomain, email, and API token; may create or modify Zendesk tickets, users, macros, and related support records through the Zendesk API.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
