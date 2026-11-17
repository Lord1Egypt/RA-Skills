## Description:

Generates Chen-style entity-relationship diagrams from SQL schemas or natural-language data model requests, with optional Mermaid, Word, and GoJS outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyanye](https://clawhub.ai/user/zhouyanye)

### License/Terms of Use:

MIT

## Use Case:

Developers and database designers use this skill to turn SQL DDL or proposed table designs into ER diagrams and, when requested, documentation or diagram source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL schemas are sent to yanleaf.com for parsing by default.

Mitigation: For private or production schemas, use --no-api to parse locally.

Risk: Optional installation commands change the global pip mirror or use sudo.

Mitigation: Avoid these optional commands unless needed, and review their system-wide effects first.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhouyanye/skills/sql-to-er)
- [Server-resolved source repository](https://github.com/zhouyanye/sql-to-er)
- [SQL to ER online tool](https://yanleaf.com/tools/sql-to-er)

## Skill Output:

**Output Type(s):** [Files, Code]

**Output Format:** [Chen PNG diagrams, Mermaid text, Word documents, or GoJS JSON, as requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces only requested formats; PNG is the default diagram format.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
