## Description:

Converts Markdown into WeChat-compatible inline HTML with theme styles for preview, copy-paste, or downstream draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhylq](https://clawhub.ai/user/zhylq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to convert Markdown files into styled HTML that can be previewed, copied into the WeChat official account editor, or passed to downstream draft publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs npm packages at conversion time.

Mitigation: Install only after review; prefer a version that pins dependencies with a lockfile and installs dependencies during setup or with install scripts disabled.

Risk: The conversion script writes output files and creates then deletes a working-directory temporary folder.

Mitigation: Run it in a controlled workspace and review input, theme, and output paths before execution.

Risk: Generated publishing HTML may need review before use in WeChat workflows.

Mitigation: Review or sanitize generated HTML before publishing, especially when converting Markdown from untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhylq/skills/zhy-markdown2wechat)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [HTML file plus concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a WeChat-compatible HTML file with inline CSS; default output name is output.html when not specified.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
