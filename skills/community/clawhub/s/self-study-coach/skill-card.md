## Description:

自学教练 helps teachers turn course handouts and exam questions into single-file HTML study guides and interactive quiz applications for self-study and test preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhilei951](https://clawhub.ai/user/duzhilei951)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and training creators use this skill to convert handouts, outlines, past exam questions, and mock questions into shareable HTML learning pages and quiz tools. Students use the generated files locally in a browser for guided review, practice, exam simulation, and wrong-answer review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local HTML can run JavaScript in the viewer's browser.

Mitigation: Share generated HTML only between trusted teachers and students, and review files before broader distribution.

Risk: Imported progress JSON can change saved quiz progress and review state.

Mitigation: Import progress JSON only from trusted sources and keep backups before migrating records across devices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhilei951/skills/self-study-coach)
- [ClawHub publisher profile](https://clawhub.ai/user/duzhilei951)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with generated single-file HTML, CSS, JavaScript, and optional progress JSON import/export structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated quiz pages may use browser localStorage for progress, wrong answers, and scores.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
