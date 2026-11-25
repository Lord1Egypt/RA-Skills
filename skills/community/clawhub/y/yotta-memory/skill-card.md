## Description:

Yotta-memory gives AI agents persistent, file-based memory for restoring context across sessions, recording important information, and archiving older memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use it to restore task context between sessions and save facts, preferences, boundaries, and commitments in a local or shared memory store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports serious memory-security and data-handling weaknesses, and the scan covered only part of the artifact.

Mitigation: Consider avoiding installation until the reported issues are addressed; if evaluating it, use a reviewed, version-pinned package and do not send credentials over ordinary HTTP.

## Reference(s):

- [Project documentation](https://github.com/YottaMeta/yotta-memory)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-memory)
- [Memory format and CLI protocol](references/protocol.md)
- [Extension provider protocol](references/provider-protocol.md)
- [FAQ and usage guidance](references/faq.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, JSON, Shell commands]

**Output Format:** [Markdown memory files, recalled context, and text or JSON operation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent user- or project-level memory; FACT entries are shared and PREF, BOUND, and COMMIT entries are owner-isolated.]

## Skill Version(s):

0.24.5 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
