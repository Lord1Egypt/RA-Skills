## Description:

Teaching Knowledge Visualizer helps teachers turn lesson topics, chapters, and textbook text into classroom-ready visual learning materials and interactive HTML pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maguangcaii](https://clawhub.ai/user/maguangcaii)

### License/Terms of Use:

MIT-0

## Use Case:

External teachers and education content creators use this skill to structure course knowledge, choose suitable visualization forms, and generate projected classroom materials, including interactive HTML pages for concepts, formulas, examples, quizzes, and graph or diagram exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated graph-expression pages may run unsafe JavaScript when lesson data is pasted, imported, or sourced from the web.

Mitigation: Review generated HTML before classroom use and replace dynamic expression execution with a real math parser or strict AST evaluator before broad deployment.

Risk: Chinese-language and Chinese-curriculum defaults may be unsuitable for other teaching contexts.

Mitigation: Confirm curriculum, language, terminology, and textbook-version assumptions with the teacher before using the generated materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maguangcaii/skills/teaching-knowledge-visualizer)
- [data-format.md](artifact/data-format.md)
- [pedagogy.md](artifact/pedagogy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON outlines, and self-contained HTML/CSS/JavaScript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce one or two standalone HTML pages; Mermaid, PlantUML, or Markdown graph source is produced only when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
