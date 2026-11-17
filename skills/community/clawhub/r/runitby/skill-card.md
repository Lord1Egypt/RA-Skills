## Description:

Collect answers from people outside the chat by link. Make an open form, survey, poll or sign-up sheet anyone can fill (like a Tally or Google Form), ask specific people for details (a shipping address, client intake, availability, an RSVP), or get approval or sign-off from named people (human in the loop), then read the answers back as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aldrinsalazar](https://clawhub.ai/user/aldrinsalazar)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can collect information from people outside the chat through forms, surveys, sign-ups, and named approval requests, then use the validated responses in their workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forms and approval requests may collect personal or sensitive information, and links or answers may be emailed to participants.

Mitigation: Request only necessary information, review Run it by's privacy and retention terms, and share each link only with its intended recipients.

Risk: A compromised API key could allow unauthorized use of the service.

Mitigation: Protect RUNITBY_API_KEY and avoid exposing it in prompts, logs, or shared content.

Risk: An approval response could be used to trigger a consequential action without adequate identity checks.

Mitigation: Use authorized named approvers with email verification for consequential decisions, and proceed only when the verdict is approved.

## Reference(s):

- [Run it by](https://runitby.app)
- [Run it by API reference](https://runitby.app/llms.txt)
- [Run it by OpenAPI specification](https://runitby.app/openapi.json)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [API request payloads and validated response JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the RUNITBY_API_KEY credential; responses may contain information submitted by external participants.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
