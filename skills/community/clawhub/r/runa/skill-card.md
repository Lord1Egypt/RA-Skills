## Description:

Save, search, list, update, and delete bookmarks and text notes in Runa, and upload PDF or image files to a Runa library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imprakharshukla](https://clawhub.ai/user/imprakharshukla)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Runa libraries: save URLs or text notes, search and list saved items, update status or metadata, delete bookmarks after confirmation, preview URL enrichment, and upload PDFs or images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected URLs, notes, and uploaded PDFs or images are sent to Runa and may be stored or AI-processed in the user's Runa account.

Mitigation: Use the skill only for data approved for Runa, and avoid saving secrets or confidential documents unless Runa is approved for that data.

Risk: Bookmark deletion is permanent.

Mitigation: Confirm the target bookmark and user intent before issuing delete requests.

## Reference(s):

- [Runa API Reference](references/api.md)
- [Runa Skill Page](https://clawhub.ai/imprakharshukla/skills/runa)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RUNA_API_KEY authentication and reports saved, listed, or searched bookmark details back to the user.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
