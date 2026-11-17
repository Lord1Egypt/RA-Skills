## Description:

Search PDFs and local document libraries with vera-cli to retrieve citation-ready context for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dkylewillis](https://clawhub.ai/user/dkylewillis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search local PDF-derived .vera archives and document libraries, retrieve citation-ready passages or figure metadata, inspect and validate archives, and decide when conversion or indexing commands require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversion, indexing, overwrite, and export commands can create or replace local files.

Mitigation: Ask for explicit user authorization before write operations and disclose the expected .vera, .vera-index, or exported file output.

Risk: Sensitive PDF content may persist in generated .vera archives or .vera-index folders.

Mitigation: Treat archives and indexes as derived local data and avoid operating on sensitive document libraries unless the user intends that local persistence.

Risk: Search scores, ranks, captions, or weakly related text can be mistaken for direct evidence.

Mitigation: Read returned text, pages, headings, and figure metadata, then cite only claims directly supported by the retrieved evidence.

## Reference(s):

- [VERA CLI reference for agents](references/cli-reference.md)
- [VERA retrieval workflows](references/retrieval-workflows.md)
- [ClawHub Skill Page](https://clawhub.ai/dkylewillis/skills/vera)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local file access and vera-cli; read-only searches produce JSON, while conversion, indexing, overwrite, and export commands can write local files.]

## Skill Version(s):

0.1.1 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
