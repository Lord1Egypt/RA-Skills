## Description:

Saves academic paper metadata, tags, PDF links, and optional AI-generated summaries to a Zotero library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozisword](https://clawhub.ai/user/mozisword)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to have an agent create Zotero entries for academic papers, add metadata, tags, and optional summaries, and attach arXiv PDFs when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a credential-shaped value in the shipped script.

Mitigation: Review the script before installation, remove any embedded credential-shaped value, and rotate any matching Zotero API key if it is real.

Risk: The security summary reports that credential handling does not match the documented ZOTERO_CREDENTIALS configuration.

Mitigation: Confirm the script reads ZOTERO_CREDENTIALS as documented before use, and use a narrowly scoped Zotero API key.

Risk: The security guidance warns that automatic PDF download and upload behavior is poorly validated.

Mitigation: Avoid untrusted URLs until arXiv host validation, download limits, and opt-in attachment behavior are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mozisword/skills/zotero-myscholar)
- [Zotero](https://www.zotero.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and argument guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS; writes entries and optional notes or attachments through the Zotero API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
