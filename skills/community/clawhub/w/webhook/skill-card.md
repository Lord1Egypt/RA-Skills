## Description: <br>
Implement secure webhook receivers and senders with proper verification and reliability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as guidance for building webhook receivers and senders with signature verification, replay prevention, idempotency, retries, delivery tracking, and operational safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook payloads, delivery logs, or troubleshooting records may expose secrets or sensitive fields. <br>
Mitigation: Avoid logging secrets or full sensitive payloads unnecessarily, redact private fields, restrict log access, and set retention periods appropriate to the data. <br>
Risk: Unsigned or replayed webhook requests can forge events or repeat critical actions. <br>
Mitigation: Verify HMAC signatures over raw body bytes, enforce timestamp freshness, and deduplicate processed event IDs. <br>
Risk: Duplicate deliveries or slow processing can create repeated side effects. <br>
Mitigation: Acknowledge quickly after minimal validation, process work asynchronously, and make handlers idempotent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/webhook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only; no executable code or system access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
