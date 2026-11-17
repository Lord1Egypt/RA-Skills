## Description:

Saves paper metadata, PDF links, and AI-generated summaries to a user's Zotero library using Zotero credentials supplied through ZOTERO_CREDENTIALS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloamingblue](https://clawhub.ai/user/gloamingblue)

### License/Terms of Use:


## Use Case:

Researchers, students, and developers use this skill to add paper records, optional abstracts, summaries, tags, and arXiv PDF attachments to a Zotero library from command-line inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Zotero API credentials and can create Zotero items and upload attachments.

Mitigation: Use a least-privilege Zotero API key and review the target library before running the skill.

Risk: The skill can derive and download a PDF URL from user-provided arXiv links before uploading the file to Zotero.

Mitigation: Process only trusted paper URLs unless the PDF logic is constrained to canonical HTTPS arxiv.org URLs with size and content validation.

## Reference(s):

- [Zotero](https://www.zotero.org)
- [ClawHub skill page](https://clawhub.ai/gloamingblue/skills/zotero-paper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS in userid:apiKey format.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
