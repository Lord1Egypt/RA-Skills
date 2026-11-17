## Description:

Export WeChat public account articles as mobile long screenshots (PNG), PDFs, or high-quality Markdown with YAML frontmatter and code block support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzking](https://clawhub.ai/user/benzking)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content operations teams use this skill to export WeChat public-account article URLs into portable PNG, PDF, or Markdown files for archiving, review, or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes remote WeChat article content and can fetch associated images.

Mitigation: Run it in a sandboxed or containerized environment with restricted network egress, and use --no-images unless local image copies are needed.

Risk: The security summary flags disabled browser sandboxing.

Mitigation: Avoid privileged host execution and isolate the browser process with container, VM, or dedicated user boundaries.

Risk: The security summary flags weak dependency controls.

Mitigation: Pin and review Python dependencies before production or shared-environment use.

Risk: Exported files may contain untrusted or sensitive article content.

Mitigation: Review generated PNG, PDF, and Markdown outputs before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benzking/skills/wechat-article-export)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code]

**Output Format:** [PNG screenshots, PDF documents, Markdown files, and a JSON-like result object with output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown output may include YAML frontmatter and optional local image copies; screenshot and PDF outputs are written under an article-specific output directory.]

## Skill Version(s):

1.1.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
