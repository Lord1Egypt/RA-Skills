## Description:

Deterministic SanMar API toolkit for product search, inventory and pricing checks, purchase-order validation and submission, order tracking, PO PDF parsing, and mainframe color-code resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and purchasing operations agents use this skill to query SanMar catalog, inventory, and pricing data, validate and submit purchase orders with confirmation, parse PO PDFs into drafts, and retrieve order status or tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live SanMar credentials and order data could be exposed through inline credential handling, logs, or raw SOAP payload and response output.

Mitigation: Use secure secret handling, avoid pasting passwords into chats or logs, and redact raw SOAP payloads and responses before display or retention.

Risk: Purchase-order submission can create external vendor orders.

Mitigation: Run validation before submission, preserve operator approval, and require confirm=true only after the user explicitly approves the live order.

Risk: SFTP color resolution needs review because host handling and credentials affect transport security.

Mitigation: Restrict SFTP to the official SanMar endpoint unless separately approved, verify the SFTP host key, and use separate SFTP credentials.

Risk: PDF purchase-order parsing is heuristic and may produce incomplete or incorrect draft orders.

Mitigation: Show parsed fields to the user and require approval before using the draft for purchase-order submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/sanmar)
- [SanMar homepage](https://www.sanmar.com)
- [Runtime docs index](references/README.md)
- [Agent examples](references/examples.md)
- [Authentication and integration patterns](references/auth_and_patterns.md)
- [SOAP web services reference](references/web_services.md)
- [Purchase order integration reference](references/purchase_orders.md)
- [FTP feeds and color resolution reference](references/ftp_feeds.md)
- [SanMar SOAP production endpoint](https://ws.sanmar.com:8080/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON objects from CLI actions, with Markdown guidance and inline shell commands in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Side-effecting purchase-order submission requires explicit confirm=true; PDF parsing and SFTP color lookup are optional feature paths.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
