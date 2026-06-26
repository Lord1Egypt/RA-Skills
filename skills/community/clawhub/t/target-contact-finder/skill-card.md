## Description: <br>
Finds CRM leads for hospitality and B2B travel segments, converts user requests into structured search criteria, and imports confirmed contacts into CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tourmind](https://clawhub.ai/user/tourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business development teams use this skill to search for potential hotel, travel, OTA, distribution, corporate travel, and DMC contacts, review results, and import approved contacts into CRM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends credentials and contact data to an unencrypted raw-IP service. <br>
Mitigation: Install only if the publisher and service are trusted; use a limited, revocable key and avoid processing contact data without a lawful basis. <br>
Risk: The skill can add records to a CRM. <br>
Mitigation: Confirm the target CRM account and review every batch before approving import. <br>
Risk: A compromised or stale user_key could allow unauthorized use. <br>
Mitigation: Use a revocable key, remove it after unauthorized responses, and rotate it when access changes. <br>


## Reference(s): <br>
- [Target Contact Finder on ClawHub](https://clawhub.ai/tourmind/target-contact-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown text with JSON API request and response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user_key and human confirmation before CRM import.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
