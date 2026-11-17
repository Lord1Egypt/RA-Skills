## Description:

AI-powered WhatsApp support context manager that gives agents customer history, sentiment, priority, order details, VIP status, and suggested responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cerbug45](https://clawhub.ai/user/cerbug45)

### License/Terms of Use:

MIT

## Use Case:

Customer service teams and agent developers use this skill to add local WhatsApp support context, prioritization, order tracking, customer profiling, and response suggestion workflows for support agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and exposes sensitive customer conversations and related customer records.

Mitigation: Use only after privacy review, restrict database access, define retention and deletion policies, and avoid exporting full context objects unless needed.

Risk: Security evidence reports weak privacy safeguards and overstated security claims.

Mitigation: Redact identifiers in logs and outputs, review the implementation before real customer-support use, and pin and verify the exact source version before running scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cerbug45/skills/whatsapp-context-manager)
- [Publisher profile](https://clawhub.ai/user/cerbug45)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with Python code snippets, shell commands, and JSON-compatible context summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite-backed customer context including insights, warnings, priorities, sentiment, recent messages, active orders, and suggested responses.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
