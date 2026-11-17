## Description:

Scrapes employee data from a logged-in SAP SuccessFactors browser session using browser automation when a user provides an employee ID and asks for SuccessFactors profile details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[venkatalokesh-dot](https://clawhub.ai/user/venkatalokesh-dot)

### License/Terms of Use:


## Use Case:

Authorized HR or business users use this skill to look up SAP SuccessFactors employee profile details by employee ID from an already-authenticated browser session. It is intended for scoped employee data retrieval from the UI, not API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect broad sensitive employee data from a user's logged-in SuccessFactors session without strong scope controls.

Mitigation: Use only by authorized HR or business users, and limit collection to the specific employee fields explicitly requested.

Risk: Employee profile areas may include compensation, documents, performance, leave, home contact details, or screenshots that require stronger authorization.

Mitigation: Do not access or return those categories unless clear authorization and a business need are established.

Risk: Browser automation may expose restricted or hidden fields if the user navigates beyond the requested scope.

Mitigation: Respect UI restrictions, report restricted fields as restricted, and avoid navigating beyond SuccessFactors or beyond the requested profile details.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text grouped by employee profile section, with tables for batch lookups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only fields found in the visible authorized UI should be returned; restricted or hidden values should be reported as restricted.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
