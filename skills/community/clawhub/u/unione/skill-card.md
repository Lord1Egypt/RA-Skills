## Description: <br>
Send transactional and marketing emails via UniOne Email API, manage templates, validate email addresses, check delivery statistics, manage suppression lists, configure webhooks, and handle domain settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[selzy-openclaw](https://clawhub.ai/user/selzy-openclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent draft UniOne Email API calls for sending email, validating addresses, managing templates, configuring webhooks, handling suppression lists, checking domains, exporting events, and managing projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill may operate a UniOne account, including sending emails or changing templates, webhooks, suppression lists, projects, and exports. <br>
Mitigation: Require manual review before sends, webhook changes, deletions, suppression changes, project creation, and event exports. <br>
Risk: The UniOne API key grants access to account operations. <br>
Mitigation: Use a least-privileged API key when available and never paste or log the full key. <br>
Risk: Tracking, webhook, and event-dump data can expose sensitive recipient activity data. <br>
Mitigation: Treat delivery, tracking, webhook, and event-export data as sensitive and limit access to users who need it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/selzy-openclaw/unione) <br>
- [UniOne website](https://unione.io/en/) <br>
- [UniOne API documentation](https://docs.unione.io/en/web-api-ref) <br>
- [UniOne getting started guide](https://docs.unione.io/en/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API request examples, JSON payloads, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIONE_API_KEY for API calls; the skill itself is documentation-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
