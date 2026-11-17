## Description:

Captures public webpages as viewport or full-page screenshots and exports rendered pages to image or PDF files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaonvmo-maker](https://clawhub.ai/user/jiaonvmo-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and content reviewers use this skill to capture public webpage screenshots, create visual comparison artifacts, archive rendered pages, or export pages as PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open arbitrary URLs in a headless browser, which may expose internal or sensitive pages if misused.

Mitigation: Use it for public webpages, avoid internal or sensitive URLs, and restrict URL destinations in managed deployments.

Risk: The skill can write screenshots or PDFs to user-selected file paths.

Mitigation: Keep outputs under a dedicated temporary or artifact directory and review output paths before execution.

Risk: The browser runtime is broad enough to warrant review before installation.

Mitigation: Prefer a version that pins Playwright, uses browser sandboxing or external containment, and prevents overwrites outside its artifact directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiaonvmo-maker/skills/web-screenshot)
- [ClawHub publisher profile](https://clawhub.ai/user/jiaonvmo-maker)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PNG, JPG, or PDF files with concise terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports viewport screenshots, full-page screenshots, and A4 PDF export for rendered public webpages.]

## Skill Version(s):

1.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
