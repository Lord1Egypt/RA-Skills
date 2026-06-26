## Description: <br>
Send transactional and marketing emails via UniOne Email API, manage templates, validate addresses, check delivery statistics, manage suppression lists, configure webhooks, and handle domain settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unione-repo](https://clawhub.ai/user/unione-repo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and marketing teams use this skill to let an agent work with UniOne email workflows, including sending transactional or marketing email, validating addresses, managing templates, configuring webhooks, reviewing delivery data, and maintaining domain and suppression settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send emails and change UniOne account resources such as templates, webhooks, suppressions, projects, domains, analytics exports, and subscription settings. <br>
Mitigation: Review recipients, message content, attachments, webhook URLs, domain changes, suppressions, project changes, analytics exports, and subscription actions before allowing API calls. <br>
Risk: A broadly scoped or production UniOne API key could permit unintended account changes or email sends. <br>
Mitigation: Use a least-privilege or test API key scoped to the actions needed for the task. <br>
Risk: Retrying an email send without idempotency can create duplicate messages. <br>
Mitigation: Use a unique idempotency key for each logical send operation and reuse it only when retrying that same operation. <br>
Risk: Email delivery can fail if the sender domain is not verified or DNS records are misconfigured. <br>
Mitigation: Verify the sending domain and DKIM/SPF records in UniOne before sending production email. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unione-repo/unione-api-skill) <br>
- [UniOne website](https://unione.io/en/) <br>
- [Declared source metadata](https://github.com/unione-repo/unione-api-skill) <br>
- [UniOne API documentation](https://docs.unione.io/en/web-api-ref) <br>
- [UniOne getting started guide](https://docs.unione.io/en/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON request bodies, curl commands, and language-specific code examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIONE_API_KEY and a verified UniOne sending domain for email delivery.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
