## Description:

Scrape employee data from a logged-in SAP SuccessFactors browser session using browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[venkatalokesh-dot](https://clawhub.ai/user/venkatalokesh-dot)

### License/Terms of Use:


## Use Case:

Employees and authorized operators use this skill to retrieve visible employee profile details from a logged-in SAP SuccessFactors session when an employee ID is provided. It supports single-employee lookup and sequential batch lookup from the browser UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a live authenticated SuccessFactors browser session to collect sensitive employee HR data with limited safeguards.

Mitigation: Install and use it only when authorized to view the requested employee records; request only necessary fields, avoid broad batch use unless approved, and treat returned HR data as sensitive.

Risk: Browser scraping may return incomplete or stale fields when SuccessFactors pages, permissions, or tabs differ.

Mitigation: Review the returned fields before use and do not treat the skill as an auditable or least-privilege HR integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/venkatalokesh-dot/skills/sf-scrapper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text employee profile fields, with tables for batch results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes only fields found in the rendered SuccessFactors page; not all fields may be visible.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
