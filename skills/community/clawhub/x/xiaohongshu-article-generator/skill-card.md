## Description:

Generates Xiaohongshu-style content packages from hot topics, including copywriting, HTML pages, and image outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiker1996](https://clawhub.ai/user/shiker1996)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and agent users can use this skill to turn a topic into a Xiaohongshu-style note package with short-form copy, mobile HTML layouts, and publishable page images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe topic or output path handling may write files outside the intended output folder.

Mitigation: Use trusted topic values, choose an isolated output directory, slug or sanitize topic-derived filenames, and enforce path containment before writing files.

Risk: Unescaped topic or content values may inject active HTML into browser-rendered output.

Mitigation: Escape user-controlled text before HTML generation and review rendered HTML before converting it to images.

Risk: Browser rendering and dependency behavior may expand the execution surface during image conversion.

Mitigation: Pin dependencies, run conversion in a restricted browser context, and avoid workspaces with sensitive writable files until rendering restrictions are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shiker1996/skills/xiaohongshu-article-generator)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [README.md](README.md)
- [EXAMPLES.md](EXAMPLES.md)
- [LAYOUT_GUIDE.md](LAYOUT_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown guidance plus generated copywriting, HTML, and PNG page files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces topic-scoped output directories with 375x667 Xiaohongshu-style pages rendered as images.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
