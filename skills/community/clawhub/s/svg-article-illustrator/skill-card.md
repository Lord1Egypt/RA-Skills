## Description: <br>
AI-driven SVG article illustration generator that supports dynamic SVG, static SVG, and PNG export modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cat-xierluo](https://clawhub.ai/user/cat-xierluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to analyze Markdown articles, plan illustration placement, generate focused SVG visuals, embed SVG code into the article, or export SVG illustrations to PNG when platform compatibility requires it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill edits the target Markdown article by inserting generated SVG or image references. <br>
Mitigation: Review the article diff before publishing and keep a backup of important source Markdown files. <br>
Risk: The skill may keep local archived copies of generated SVGs inside the skill directory. <br>
Mitigation: For confidential articles, review or delete the archive after use. <br>
Risk: PNG export renders local SVG content through Node.js and Puppeteer dependencies. <br>
Mitigation: Use PNG export only with trusted SVG content and trusted local dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/svg-article-illustrator) <br>
- [Publisher profile](https://clawhub.ai/user/cat-xierluo) <br>
- [Project homepage](https://github.com/cat-xierluo/legal-skills) <br>
- [Core design principles](references/core-principles.md) <br>
- [Dynamic SVG mode specification](references/dynamic-svg.md) <br>
- [Static SVG mode specification](references/static-svg.md) <br>
- [PNG export mode specification](references/png-export.md) <br>
- [Multi-agent generation guide](references/multi-agent-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, files, shell commands, guidance] <br>
**Output Format:** [Markdown with embedded SVG code, optional SVG and PNG files, and concise operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output embeds SVG directly in Markdown; PNG export uses local Node.js and Puppeteer dependencies; completed illustrations may be archived locally inside the skill directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and changelog, released 2026-03-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
