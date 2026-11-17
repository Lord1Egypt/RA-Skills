## Description:

This employee-facing skill retrieves company intelligence reports from a company API for B2B sales workflows when a user enters a company name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, especially B2B sales users, use this skill to query a company by name and receive a company intelligence report with business context, opportunity signals, and optional opportunity insight returned by the company API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Employee identity, bearer tokens, and company queries may be sent to a non-HTTPS or untrusted API endpoint.

Mitigation: Configure and verify an organization-controlled HTTPS COMPANY_INFO_API_URL before installation or use.

Risk: Access tokens and employee identity may be cached locally in plaintext.

Mitigation: Use only protected machines, restrict access to the token cache, or move token storage to an approved credential store.

Risk: Refresh or re-search requests may trigger backend collection even when the user expects a read-only lookup.

Mitigation: Confirm the organization's data-handling policy and use refresh behavior only when new collection is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-company-info-personal)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown company intelligence report with status messages, opportunity signals, and optional opportunity insight sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and python3; may call a configured company API and cache access tokens locally.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
