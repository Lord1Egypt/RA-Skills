## Description:

元公 creates reproducible school-document skeletons from versioned rules and structured facts, then checks drafts for missing fields, date and attachment issues, student personal information, placeholders, overclaims, sensitive wording, and incomplete meeting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

School staff use it to draft structured notices, parent letters, reports, meeting minutes, plans, and other school documents from supplied facts, and to check existing drafts for deterministic gaps. Developers can add checks to batch workflows or CI; final documents still require school review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may overwrite custom skill files or affect multiple agents when installed globally.

Mitigation: Use a reviewed, version-pinned release or reviewed local installer, select one destination, preview with --dry-run, and back up custom edits before reinstalling.

Risk: Generated reports can quote student information.

Mitigation: Keep reports private and review or redact them before sharing.

## Reference(s):

- [Privacy and usage boundaries](artifact/references/privacy.md)
- [Document type and facts format](artifact/references/types-format.md)
- [Report format](artifact/references/report-format.md)
- [ClawHub release page](https://clawhub.ai/yottameta/skills/yotta-school-doc)
- [Project homepage](https://github.com/YottaMeta/yotta-school-doc)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-school-doc)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown or JSON document skeletons and validation reports; JSON rule packs and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic findings include evidence lines and suggestions; missing facts remain explicit placeholders, and a configurable findings threshold can gate CI.]

## Skill Version(s):

0.1.5 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
