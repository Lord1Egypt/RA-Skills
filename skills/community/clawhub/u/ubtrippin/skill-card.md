## Description: <br>
Manages travel through UBTRIPPIN, including trips, itinerary items, loyalty programs, family sharing, city guides, events, notifications, webhooks, and billing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fistfulayen](https://clawhub.ai/user/fistfulayen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to read and manage UBTRIPPIN travel records, add bookings, retrieve loyalty details, and coordinate family or trip-sharing workflows through the UBTRIPPIN API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive travel records, loyalty numbers, booking emails, ticket PDFs, family/collaborator information, and related account data. <br>
Mitigation: Install only when the user trusts UBTRIPPIN with this data, and store API keys only in protected secrets or configuration. <br>
Risk: The skill can trigger consequential actions such as forwarding booking emails, exporting loyalty data, deleting or merging records, sharing trips or family access, creating webhooks or calendar links, and starting billing or checkout flows. <br>
Mitigation: Require explicit user confirmation before performing these actions. <br>


## Reference(s): <br>
- [UBTRIPPIN API documentation](https://www.ubtrippin.xyz/api/v1/docs) <br>
- [UBTRIPPIN website](https://www.ubtrippin.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/fistfulayen/ubtrippin) <br>
- [Publisher profile](https://clawhub.ai/user/fistfulayen) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a UBTRIPPIN API key and registered sender email for authenticated account actions.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
