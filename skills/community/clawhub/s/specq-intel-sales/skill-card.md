## Description:

SpecQ helps electronic-chemicals sales and field engineering teams turn customer, product, visit-history, loss-review, and competitor context into an eight-part sales intelligence brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daizehua-wq](https://clawhub.ai/user/daizehua-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Sales engineers, field application engineers, and sales-support teams use this skill before customer meetings to recall local sales history, gather public market context, and generate a structured attack-plan brief for semiconductor electronic chemicals. It can also record visit notes, closed-loop feedback, and concise sales insights for later reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory can retain customer history, visit notes, feedback, and generated intelligence.

Mitigation: Use a dedicated workspace or profile, set storage to an approved data directory, and review retention and deletion expectations before entering real customer data.

Risk: Configured API keys can cause customer text, search terms, embeddings, or recordings to be sent to external providers.

Mitigation: Run without optional external API keys for sensitive work, or approve providers and data classes before enabling embedding, search, or transcription integrations.

Risk: Database paths and API URLs supplied to insight extraction can expose sensitive or unintended business data.

Mitigation: Restrict database paths and endpoints to approved sources, avoid arbitrary inputs, and review tenant isolation before shared or production use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daizehua-wq/skills/specq-intel-sales)
- [Publisher profile](https://clawhub.ai/user/daizehua-wq)
- [Skill README](artifact/README.md)
- [Skill workflow](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown briefs by default, with JSON for memory/search/insight tools and short text formats for email or chat summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated briefs follow an eight-module sales-intelligence structure and may include locally recalled history, public search snippets, confidence/source labels, and feedback reminders.]

## Skill Version(s):

2.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
