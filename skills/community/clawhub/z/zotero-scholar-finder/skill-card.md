## Description:

Saves paper metadata, links, tags, abstracts, optional AI summaries, and arXiv PDF attachments to a user's Zotero library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justin18chan](https://clawhub.ai/user/justin18chan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent users use this skill to add paper records to Zotero from command-line paper metadata. It is useful when an agent has identified a paper and needs to persist the title, authors, URL, abstract, summary, tags, and available arXiv PDF in a Zotero library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Zotero credentials to create items, notes, and attachments in a user's library.

Mitigation: Use a least-privilege Zotero API key, keep ZOTERO_CREDENTIALS secret, and review paper metadata before running the command.

Risk: The security evidence reports that the PDF download path is under-scoped and can fetch non-arXiv or local/internal resources before uploading them to Zotero.

Mitigation: Run it only on trusted paper URLs until arXiv URL validation, download limits, and dependency pinning are tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justin18chan/skills/zotero-scholar-finder)
- [Zotero](https://www.zotero.org)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS in userid:apiKey format; creates Zotero items and may attach arXiv PDFs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
