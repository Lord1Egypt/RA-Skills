## Description:

AI Question Generator helps educators and trainers create multi-format questions, answers, explanations, Bloom-level labels, and interactive HTML quizzes from topics or learning materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, trainers, and content authors use this skill to generate quizzes or exam drafts across K12, higher education, and professional training scenarios. It supports topic-based and material-based question generation with answer keys, explanations, difficulty labels, and Bloom taxonomy coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can run injected JavaScript from quiz content.

Mitigation: Use trusted quiz source material and inspect generated HTML before opening or sharing it.

Risk: Inline shell arguments can expose or mangle quiz JSON content.

Mitigation: Pass quiz JSON through stdin or a file instead of inline shell arguments.

Risk: Output paths outside the intended workspace can put generated files in unexpected locations.

Mitigation: Keep output paths inside the current workspace.

## Reference(s):

- [Bloom Taxonomy Question Guide](references/bloom-taxonomy.md)
- [Question Quality Checklist](references/quality-checklist.md)
- [Question Type Design Guide](references/question-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with quiz JSON and interactive HTML output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce an HTML quiz file with answer mode, print mode, answer navigation, folded explanations, difficulty labels, and coverage statistics.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
