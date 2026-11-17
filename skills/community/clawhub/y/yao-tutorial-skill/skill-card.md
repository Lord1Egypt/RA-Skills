## Description:

Create standalone beginner tutorial packages from a topic or supplied references, with adaptive research, course-style outline design, chapter visuals, and Markdown/DOCX/PDF/HTML exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sat-99](https://clawhub.ai/user/sat-99)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, writers, and developers use this skill to turn a topic or supplied references into a source-backed beginner tutorial package with an outline, chapter visuals, quality review artifacts, and Markdown, Word, PDF, and HTML exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering user-controlled Markdown, HTML, or SVG may trigger unintended network requests through embedded images, CSS, or links.

Mitigation: Run the skill in a dedicated workspace with renderer network access blocked when possible, and review embedded images, CSS, and links before export.

Risk: The skill creates local tutorial, research, visual, screenshot, and export files.

Mitigation: Direct outputs to a disposable or project-specific workspace and review generated artifacts before sharing or publishing them.

Risk: The skill may default to Chinese-style tutorial formatting when the task does not specify language or style.

Mitigation: State the desired language, audience, style, and export formats explicitly in the prompt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sat-99/skills/yao-tutorial-skill)
- [Diataxis tutorials](https://diataxis.fr/tutorials/)
- [X API post search introduction](https://docs.x.com/x-api/posts/search/introduction)
- [X API search operators](https://docs.x.com/x-api/posts/search/integrate/operators)
- [Semantic Scholar Academic Graph API](https://www.semanticscholar.org/product/api)
- [GitHub repository search documentation](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
- [Input adaptation reference](references/input-adaptation.md)
- [Research sourcing reference](references/research-sourcing.md)
- [Tutorial outline and writing reference](references/tutorial-outline-and-writing.md)
- [Course design principles reference](references/course-design-principles.md)
- [Visual HTML workflow reference](references/visual-html-workflow.md)
- [Export workflow reference](references/export-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tutorial package with JSON planning files, HTML/SVG visual assets, shell-command export steps, and DOCX/PDF/HTML deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local output files including brief.json, outline.md, tutorial.md, research registers, visual specifications, screenshots, and export artifacts.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
