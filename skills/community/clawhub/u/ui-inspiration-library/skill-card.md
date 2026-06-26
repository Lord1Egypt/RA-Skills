## Description: <br>
Archive UI screenshots into a searchable inspiration library and retrieve matching references by style, page type, use case, or visual goal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KhalilHsu](https://clawhub.ai/user/KhalilHsu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and product teams use this skill to archive UI screenshots with retrieval-friendly metadata and later find matching visual references by style, page type, use case, or visual goal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store screenshots and metadata in a long-term Notion-backed library. <br>
Mitigation: Confirm the exact target database or parent page before archiving and avoid storing confidential customer, internal, or personal screenshots unless the workspace is appropriate for that data. <br>
Risk: Notion access requires a configured API credential. <br>
Mitigation: Use a dedicated least-privilege Notion integration and keep backend identifiers and credentials configurable outside the public skill. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/KhalilHsu/ui-inspiration-library) <br>
- [Publisher profile](https://clawhub.ai/user/KhalilHsu) <br>
- [Analysis schema](references/analysis-schema.md) <br>
- [Channel flow](references/channel-flow.md) <br>
- [Notion database schema](references/notion-database-schema.md) <br>
- [Notion file upload flow](references/notion-file-upload.md) <br>
- [Notion mapping specification](references/notion-mapping-spec.md) <br>
- [Query flow](references/query-flow.md) <br>
- [Tag vocabulary v1](references/tag-vocabulary-v1.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured metadata summaries, archive status, retrieved image references, rationale, and item links when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archive mode returns titles, tags, storage status, and item links; retrieval mode returns 1-5 ranked visual matches with concise rationale and image previews when supported.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
