## Description: <br>
Provides WhatsApp customer service agents with customer history, sentiment analysis, priority scoring, order context, VIP detection, and suggested responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Customer service teams and support agents use this skill to process WhatsApp conversations with local customer context, recent message history, order details, sentiment, priority, warnings, and response suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores customer chat, profile, and order data in a local SQLite database. <br>
Mitigation: Treat the database as private customer data; place it in an approved storage location with appropriate access controls, backups, and deletion procedures. <br>
Risk: Context exports can include sensitive customer messages, profile attributes, order details, warnings, and response suggestions. <br>
Mitigation: Redact or minimize exported context before sending it to logs, analytics, APIs, or model training workflows. <br>
Risk: The release evidence does not provide enough built-in privacy, retention, or access-control guardrails. <br>
Mitigation: Define retention periods, authorized users, and operational review requirements before deploying the skill in a customer support workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cerbug45/whatsapp-context-manager) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON-compatible context exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local customer context summaries, including sentiment, priority, categories, warnings, insights, orders, and suggested responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
