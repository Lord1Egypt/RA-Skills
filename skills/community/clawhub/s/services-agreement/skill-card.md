## Description:

Drafts and fills services agreement templates, including consulting contracts, contractor agreements, statements of work, professional services agreements, and freelancer contracts, producing signable DOCX files from Common Paper and Bonterms standard forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, business users, and agents use this skill to select a professional services, independent contractor, or statement-of-work template, collect required agreement terms, and generate a signable DOCX or markdown preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CLI use can expose agreement values to unsafe shell and temporary-file handling.

Mitigation: Use a per-run restricted temporary JSON file, validate filenames and template names, reject shell metacharacters and control characters, quote heredocs, and clean up the temporary file.

Risk: Remote MCP use sends agreement terms such as names, dates, pricing, and scope to the hosted Open Agreements service.

Mitigation: Confirm with the user that hosted processing is acceptable, and offer the local CLI path when confidentiality is a concern.

Risk: Inconsistent or unpinned CLI install guidance can introduce unexpected upstream changes.

Mitigation: Install the pinned CLI version documented by the skill, open-agreements@0.7.5, when using the local path.

Risk: Generated agreements may be incomplete, unsuitable, or mistaken for legal advice.

Mitigation: Require user review before signing and direct users to consult an attorney for legal advice.

## Reference(s):

- [Services Agreement ClawHub release](https://clawhub.ai/stevenobiajulu/skills/services-agreement)
- [Open Agreements](https://openagreements.org)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements)
- [Open Agreements Claude Code usage](https://github.com/open-agreements/open-agreements#use-with-claude-code)

## Skill Output:

**Output Type(s):** [files, markdown, shell commands, configuration, guidance]

**Output Format:** [DOCX files, download URLs, markdown previews, and markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP returns an expiring DOCX download URL; local CLI writes a DOCX file; preview-only mode emits a markdown preview.]

## Skill Version(s):

0.2.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
