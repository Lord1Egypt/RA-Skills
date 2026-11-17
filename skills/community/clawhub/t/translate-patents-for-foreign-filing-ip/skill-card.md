## Description:

Translate Chinese patent applications, priority texts, claims, descriptions, abstracts, drawing text, sequence-listing references, or invention disclosures into filing-support drafts for Europe, the United States, Japan, or Korea while preserving source support, claim scope, terminology, and destination-specific patent style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, patent professionals, and translation reviewers use this skill to convert Chinese patent source material into EP, US, JP, or KR filing-support drafts while preserving claim scope, terminology, source locators, and destination-specific patent style. The skill also helps produce terminology, ambiguity, change, QA, and review notes for counsel and translator confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or unpublished patent material could be exposed if optional external connectors are used without matter-specific approval.

Mitigation: Use only materials the user is authorized to process, and avoid optional external connectors for confidential inventions unless those services are approved for the matter.

Risk: A filing-support translation may contain wording that changes claim scope, support, priority, added-matter analysis, or filing-route compliance.

Mitigation: Require review by qualified destination patent counsel and a competent patent translator before using any draft for filing.

Risk: Incomplete, conflicting, or unreadable source material can produce missing dependencies, unresolved ambiguity, or unsupported translation choices.

Mitigation: Freeze the authoritative source, identify missing or conflicting sections, keep source locators, and record unresolved ambiguity instead of guessing.

## Reference(s):

- [European Patent Translation Reference](references/europe.md)
- [United States Patent Translation Reference](references/united-states.md)
- [Japan Patent Translation Reference](references/japan.md)
- [Korea Patent Translation Reference](references/korea.md)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown or structured text with destination-specific translation sections, terminology registers, ambiguity and change registers, QA notes, and review items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create destination-specific project folders when file output is requested; all filing-support drafts require qualified patent counsel and translator review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
