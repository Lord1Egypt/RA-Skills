## Description:

Generates article illustrations as embedded SVG, static SVG, or optional PNG exports for Markdown publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

External authors and content teams use this skill to analyze Markdown articles, plan illustration placement, and generate concise SVG visuals or PNG-compatible outputs for publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default illustration workflow edits article files in place and archives generated SVGs.

Mitigation: Run the skill on files under version control and review generated SVG and Markdown changes before publishing.

Risk: Optional PNG export renders SVG through a local browser path that the security summary identifies as under-hardened.

Mitigation: Only convert trusted SVG files, avoid credentialed or sensitive environments, and prefer a pinned Puppeteer install with browser sandboxing, JavaScript disabled, and outbound requests blocked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/svg-article-illustrator)
- [Publisher profile](https://clawhub.ai/user/cat-xierluo)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [Core design principles](references/core-principles.md)
- [Dynamic SVG mode](references/dynamic-svg.md)
- [Static SVG mode](references/static-svg.md)
- [PNG export mode](references/png-export.md)
- [Multi-agent generation guide](references/multi-agent-generation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown containing embedded SVG code, optional SVG and PNG files, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default modes edit the source Markdown in place by embedding SVG; PNG export requires Node.js and Puppeteer.]

## Skill Version(s):

1.0.5 (source: release evidence and changelog, released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
