## Description:

Guides agents in parsing, extracting, splitting, and editing documents with Reducto through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can guide an agent to process documents, extract structured data, and make approved changes to PDFs and DOCX files using their Reducto connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents and extracted data are sent to Reducto and may persist there.

Mitigation: Confirm the documents and extraction instructions before sending them, and avoid sharing unnecessary sensitive content.

Risk: Edits, hosted functions, and triggers can change documents or run later without direct supervision.

Mitigation: Confirm each edit, function, trigger, and destination before execution; use read-only requests by default.

Risk: Direct use of a Maton API key may expose credentials.

Mitigation: Prefer CLI login and use the raw API-key path only when the CLI is unavailable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/reducto)
- [Maton homepage](https://maton.ai)
- [Reducto documentation](https://docs.reducto.ai)
- [Reducto API reference](https://docs.reducto.ai/api-reference)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document-processing results depend on the connected account and approved requests.]

## Skill Version(s):

1.2.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
