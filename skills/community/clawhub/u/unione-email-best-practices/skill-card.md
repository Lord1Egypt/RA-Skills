## Description:

Use when building email features on UniOne or fixing delivery: emails going to spam, bounces and complaints, SPF/DKIM/DMARC for spf.unione.io, domain warm-up, bulk sender rules, tracking domain and dedicated IP, consent and unsubscribes (GDPR, CAN-SPAM, CASL), double opt-in, list hygiene, which transactional emails an app needs and how to keep them out of unsubscribes, retries and idempotency, accessible emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unione](https://clawhub.ai/user/unione)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to plan and operate UniOne email features, including sender authentication, consent and list management, transactional messages, and reliable delivery. It provides practical guidance for diagnosing spam placement, bounces, and complaints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports the package benign, but its overall analysis is partial because one reference in SKILL.md could not be resolved.

Mitigation: Check the unresolved reference before relying on guidance that depends on it, and verify current API details against UniOne's documentation.

Risk: Email consent and unsubscribe rules vary by jurisdiction, and the compliance reference is not legal advice.

Mitigation: Have counsel review the flows for the markets where email will be sent.

## Reference(s):

- [UniOne Web API documentation](https://docs.unione.io/en/web-api-ref)
- [Deliverability](references/deliverability.md)
- [Compliance](references/compliance.md)
- [List management](references/list-management.md)
- [Sending reliability](references/sending-reliability.md)
- [Transactional emails](references/transactional-emails.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown with tables, diagrams, and inline API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
