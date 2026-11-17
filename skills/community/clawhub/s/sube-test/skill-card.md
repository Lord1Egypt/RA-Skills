## Description:

Converts PDF, Word, PowerPoint, and image files into LLM-ready Markdown with paragraphs, tables, formulas, charts, and ordered headings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sube-py](https://clawhub.ai/user/sube-py)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse local documents through PDRouter into Markdown before extracting fields, tables, document text, or content for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local documents are uploaded to PaodingAI/PDRouter for parsing, which may be inappropriate for confidential or restricted data.

Mitigation: Run the skill only on documents approved for external SaaS parsing and confirm PD_ROUTER_API_KEY use before processing sensitive material.

Risk: Using an unpinned or untrusted release could change the upload workflow or handling of parsed output.

Mitigation: Install from a pinned or trusted ClawHub release and review release evidence before automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sube-py/skills/sube-test)
- [PDRouter platform](https://platform.paodingai.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown printed to stdout and optionally written to a local file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and PD_ROUTER_API_KEY; uploads the source document to PDRouter and can include image data when PDFLUX_INCLUDE_IMAGES=true.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
