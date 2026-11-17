## Description:

Exports a Xiaohongshu creator's accessible public notes from a logged-in browser into local Markdown files with text, media links, and engagement counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and researchers use this skill to archive and analyze a Xiaohongshu creator's accessible public notes as local Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported notes contain scraped content and links bearing xsec_token values from a logged-in browser session.

Mitigation: Review before installing, keep exports in a private directory, and remove xsec_token parameters before committing or sharing Markdown or JSON files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fatmind/skills/xhs-note-batch-export)
- [Webclaw3 browser automation setup](https://webclaw3.com)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Local per-note and aggregate Markdown files, plus JSON summary and status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media is saved as links, not downloaded; missing content or engagement counts may be marked partial.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
