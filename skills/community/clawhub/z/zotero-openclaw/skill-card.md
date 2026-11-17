## Description:

Saves paper metadata, PDF links, tags, and AI-generated summaries to a user's Zotero library using Zotero API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-cat1](https://clawhub.ai/user/little-cat1)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to add paper metadata, optional abstracts, tags, AI-generated summaries, and arXiv PDF attachments to a Zotero library from command-line inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Zotero API credentials to create library entries and upload attachments.

Mitigation: Use a minimally scoped Zotero API key and install only when the workflow is trusted.

Risk: The skill may automatically download a PDF from a loosely checked arXiv URL and upload it to Zotero.

Mitigation: Review PDF attachment behavior before use, avoid untrusted URLs, and prefer stricter HTTPS arxiv.org validation with size and timeout limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/little-cat1/skills/zotero-openclaw)
- [Zotero](https://www.zotero.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with shell command examples and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, pyzotero, and ZOTERO_CREDENTIALS in userid:apiKey format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
