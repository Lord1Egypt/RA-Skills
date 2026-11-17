## Description:

Archive UI screenshots into a searchable inspiration library and retrieve matching references by style, page type, use case, or visual goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khalilhsu](https://clawhub.ai/user/khalilhsu)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and product teams use this skill to archive UI screenshots with searchable metadata and retrieve image-first design references by style, page type, use case, or visual goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad Notion integration or sensitive screenshots could expose customer data, internal dashboards, secrets, or other private content in the archive.

Mitigation: Use a Notion integration scoped to the intended inspiration database or parent page, and avoid archiving sensitive screenshots unless explicitly intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/khalilhsu/skills/ui-inspiration-library)
- [Analysis schema for UI inspiration ingestion](references/analysis-schema.md)
- [Channel flow: chat channels to a visual inspiration library](references/channel-flow.md)
- [Notion database schema for a UI inspiration library](references/notion-database-schema.md)
- [Notion file upload flow for image-backed archive items](references/notion-file-upload.md)
- [Notion database creation spec and field mapping](references/notion-mapping-spec.md)
- [Query flow for UI inspiration retrieval](references/query-flow.md)
- [Tag vocabulary v1 for UI inspiration library](references/tag-vocabulary-v1.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, API calls]

**Output Format:** [Markdown responses with structured metadata, image previews or item links when available, and concise status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archive mode returns titles, tags, write/upload status, and links; retrieval mode returns ranked image-first matches with short rationale.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
