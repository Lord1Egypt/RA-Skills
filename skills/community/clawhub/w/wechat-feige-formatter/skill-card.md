## Description:

Wechat Feige Formatter helps agents optimize article drafts into formatter-ready Markdown and convert them into WeChat-compatible styled HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tracevan](https://clawhub.ai/user/tracevan)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and publishing teams use this skill to turn drafts, plain text, or Markdown articles into WeChat public-account HTML with consistent formatting. Agents use the bundled rules to add layout markers, run the formatter script, and explain how to preview and copy the resulting HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may carry unsafe script content from untrusted Markdown.

Mitigation: Format only trusted article sources and review or sanitize generated HTML before copying it into a publisher workflow.

Risk: Local image embedding can inline files referenced by Markdown image paths.

Mitigation: Restrict image paths to intended article assets and disable or limit local image embedding when processing user-supplied Markdown.

Risk: The workflow accepts local file paths, which may expose private content if used without boundaries.

Mitigation: Do not allow arbitrary local paths; process files from a controlled workspace with non-public files excluded.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tracevan/skills/wechat-feige-formatter)
- [README](README.md)
- [Formatting rules](references/排版优化规则.md)
- [Example article](examples/example.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with formatter commands and generated HTML output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use a custom brand color; local image embedding is enabled by default in one bundled formatter.]

## Skill Version(s):

2.3.6 (source: server release evidence and clawhub.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
