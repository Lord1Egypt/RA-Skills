## Description: <br>
Event-driven webhook workflows with HMAC verification, retry logic, and multi-provider patterns for receiving, validating, routing, and retrying webhook events from providers such as GitHub, Stripe, and Slack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build webhook endpoints that parse JSON payloads, verify HMAC signatures, route provider events to handlers, and retry failed deliveries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample webhook server can accept unauthenticated webhook requests if no secret is configured or if requests omit signatures. <br>
Mitigation: Require a configured secret, reject missing signatures, implement provider-specific verification for GitHub, Slack, and Stripe, and run the endpoint behind HTTPS on the intended interface. <br>
Risk: Webhook payloads can contain sensitive event data. <br>
Mitigation: Avoid logging or storing raw payloads unless access controls and retention rules are defined. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/webhook-automation) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes sample webhook server and handler patterns that require local configuration before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
