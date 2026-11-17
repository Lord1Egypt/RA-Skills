## Description:

Publish content to any Sanity CMS instance by creating Sanity drafts, pushing documents, uploading image assets, or converting content into Sanity-formatted documents for any document type and schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squidpunch](https://clawhub.ai/user/squidpunch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare Sanity-compatible document JSON, resolve schema and reference details, optionally upload image assets, and create Sanity CMS drafts or published documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live Sanity CMS data when used with a write-enabled token.

Mitigation: Use a least-privilege Sanity token, prefer a staging dataset, keep draft mode enabled, and review generated document JSON before pushing changes.

Risk: The security evidence reports a serious script-safety flaw involving untrusted filenames or environment overrides.

Mitigation: Avoid untrusted filenames and environment overrides until the publish script passes values as data instead of interpolating them into Python source.

## Reference(s):

- [Sanity Content API Reference](references/api.md)
- [Portable Text Reference](references/portable-text.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON document examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Sanity document JSON, API request guidance, draft IDs, and manual follow-up notes for Sanity Studio.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
