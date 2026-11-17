## Description:

A ThumbGate-hardened WhatsApp ordering agent for QSRs, featuring smart upsells and inventory awareness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant operators and QSR teams use this skill to run a WhatsApp ordering agent that captures orders, suggests upsells, checks inventory, handles allergen notes, confirms pricing, and logs orders to Google Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order logs may contain customer identifiers, order details, allergen notes, and other sensitive operational data in Google Sheets.

Mitigation: Configure the Google Sheet with least-privilege access, avoid logging payment details or unnecessary customer notes, disclose order recordkeeping where required, and set a retention policy.

Risk: Incorrect menu, inventory, pricing, tax, or allergen configuration could lead to bad order confirmations or customer safety issues.

Mitigation: Review the menu sheet and ThumbGate rules before deployment, test representative orders, and require manual review for blocked, high-value, allergen-related, duplicate, or out-of-hours orders.

Risk: WhatsApp API tokens and spreadsheet identifiers can expose the ordering channel or order records if mishandled.

Mitigation: Store credentials outside public skill text, restrict service account permissions, rotate tokens when access changes, and avoid sharing environment files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/igorganapolsky/skills/subway-whatsapp-ordering)
- [Setup Guide](artifact/setup-guide.md)
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with conversational ordering guidance, setup steps, environment configuration, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces order-handling guidance and setup instructions; no executable code is bundled.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
