## Description:

Extracts paper information from direct citations, paper links, or social media posts and helps save the resulting metadata, notes, and supported PDFs to a user's Zotero library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auto-dog](https://clawhub.ai/user/auto-dog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and research-oriented agents use this skill to turn citations, paper URLs, or social media posts that mention papers into Zotero library entries with metadata, optional summaries, tags, and supported PDF attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored Zotero API credentials to create items, notes, and attachments in a user's Zotero library.

Mitigation: Use the skill only for explicit save-to-Zotero requests, keep credentials scoped to the intended Zotero library, and review created records after execution.

Risk: Weakly validated arXiv-style URLs may cause non-paper content to be downloaded and uploaded as an attachment.

Mitigation: Avoid untrusted or shortened paper URLs and review any PDF attachment before relying on or sharing the Zotero entry.

## Reference(s):

- [Zotero](https://www.zotero.org)
- [ClawHub skill page](https://clawhub.ai/auto-dog/skills/social-media-scholar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with inline shell commands and Zotero item, note, and attachment writes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Zotero credentials from macOS Keychain or ZOTERO_CREDENTIALS; can create library items, notes, tags, and supported PDF attachments.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
