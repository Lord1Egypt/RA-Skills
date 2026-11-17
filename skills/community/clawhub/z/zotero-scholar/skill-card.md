## Description:

Save academic papers with metadata, PDF links, and AI-generated summaries to a Zotero library using credentials from ZOTERO_CREDENTIALS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gottenzzp](https://clawhub.ai/user/gottenzzp)

### License/Terms of Use:


## Use Case:

Researchers, students, and developers use this skill to create Zotero library entries from paper metadata, add optional AI summaries as notes, and attach arXiv PDFs when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Zotero API key through ZOTERO_CREDENTIALS.

Mitigation: Use a narrowly scoped Zotero API key and avoid exposing ZOTERO_CREDENTIALS in prompts, logs, or shared command output.

Risk: The skill can fetch and upload content from insufficiently validated URLs.

Mitigation: Pass only trusted HTTPS Zotero or arXiv URLs and require strict arXiv URL validation before routine use.

Risk: The Python dependency is declared with a lower-bound version rather than an exact pin.

Mitigation: Require exact dependency pinning before routine use.

## Reference(s):

- [ClawHub zotero-scholar skill page](https://clawhub.ai/gottenzzp/skills/zotero-scholar)
- [Zotero](https://www.zotero.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Zotero item creation guidance and status text; requires uv and ZOTERO_CREDENTIALS.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
