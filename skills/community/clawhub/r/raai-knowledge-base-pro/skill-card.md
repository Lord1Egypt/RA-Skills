## Description:

Knowledge Base Pro helps Russian-speaking teams build and maintain a business knowledge base with search, FAQ, role-based onboarding, SOP templates, audit, analytics, and export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, HR operators, operations leaders, and business teams use this skill to structure internal knowledge, answer repeated questions, onboard employees by role, create SOPs, audit knowledge gaps, and export knowledge-base content for bots or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Networked document processing may be used when indexing from Notion, Google Docs, Confluence, YouTube, embeddings, vector databases, or Telegram reports.

Mitigation: Treat these workflows as requiring network access, review each integration before enabling it, and explicitly configure external-provider destinations and credentials.

Risk: Sensitive HR, salary, contract, finance, or NDA material may appear in searches, query logs, exports, or external indexing destinations.

Mitigation: Do not use confidential material until access control, redaction, query-log retention, export approval, and data-destination rules are configured.

Risk: Archive, delete, export, and indexing commands can materially change what the knowledge base contains or exposes.

Mitigation: Require explicit commands, confirmations, and review for archive, delete, export, and indexing workflows.

Risk: The knowledge base can become inaccurate if the company lacks content owners, real source material, or revision discipline.

Mitigation: Assign owners for critical sections, start with verified FAQ and SOP content, and run regular stale-record and gap-analysis reviews.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/raaipro/skills/raai-knowledge-base-pro)
- [README](artifact/README.md)
- [Configuration Reference](artifact/config.yaml)
- [Implementation Guide](artifact/docs/onboarding.md)
- [Limitations and Anti-Fail Guide](artifact/docs/anti-fail.md)
- [ROI Guide](artifact/docs/roi.md)
- [Quick Start Example](artifact/examples/quick-start.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown responses with tables, checklists, templates, and optional JSON or YAML exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Russian-language operational knowledge-base outputs; optional indexing, analytics, bot, and external-document workflows depend on configured integrations.]

## Skill Version(s):

3.5.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
