## Description: <br>
Manage vacation rental properties, guest reservations, and cleaning checklists with the TIDY platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mchusma](https://clawhub.ai/user/mchusma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Short-term rental hosts, vacation property managers, and Airbnb or VRBO operators use this skill to manage TIDY properties, guest reservations, and cleaning checklists from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TIDY_API_TOKEN is a long-lived bearer token for the connected TIDY account. <br>
Mitigation: Protect the token as a secret, prefer a limited or test account when possible, and rotate the token if it may have been exposed. <br>
Risk: Delete or natural-language requests can modify properties or reservations. <br>
Mitigation: Require explicit confirmation before running delete commands or natural-language requests that change account data. <br>


## Reference(s): <br>
- [TIDY homepage](https://tidy.com) <br>
- [ClawHub skill page](https://clawhub.ai/mchusma/vacation-property-management) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TIDY_API_TOKEN as a bearer token; examples cover property, reservation, cleaning checklist, and natural-language TIDY API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
