## Description:

工具软件教程自动生成器 accepts a tool or software name, searches Chinese-language tutorial sources, and produces a structured interactive HTML tutorial report covering overview, installation, basic usage, advanced tips, FAQ, learning roadmap, and resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a named tool, software product, programming language, or framework into a Chinese-language tutorial report with practical setup guidance, examples, FAQs, and curated learning links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad tutorial prompts may trigger external web searches for private tool names or sensitive internal topics.

Mitigation: Avoid using private or sensitive tool names unless sending those search queries externally is acceptable.

Risk: Generated tutorial reports can include incorrect, outdated, or low-quality guidance from search results.

Mitigation: Review sourced links and test installation commands or examples before relying on the report.

Risk: The skill creates a local HTML report in the workspace.

Mitigation: Inspect generated HTML before sharing or publishing it, especially when the source topic is sensitive.

## Reference(s):

- [Search Guide](artifact/references/search_guide.md)
- [HTML Tutorial Template](artifact/assets/tutorial_template.html)
- [ClawHub Skill Page](https://clawhub.ai/bettermen/skills/tool-tutorial-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Single-file HTML report with inline CSS and JavaScript, plus a concise Markdown handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a root-level HTML tutorial report named for the requested tool.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
