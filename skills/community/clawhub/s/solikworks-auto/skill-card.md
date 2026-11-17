## Description:

Generates Python automation scripts that control SolidWorks through pywin32 and the SolidWorks COM interface for part creation, sketching, feature generation, drawing export, and file saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2009730](https://clawhub.ai/user/2009730)

### License/Terms of Use:

MIT-0

## Use Case:

CAD users, mechanical engineers, and developers use this skill to turn SolidWorks modeling and drawing-export requests into runnable Python automation code with setup, execution, and result-checking guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated automation can create, modify, export, save, or overwrite CAD files.

Mitigation: Confirm the target model, dimensions, save and export paths, filenames, and overwrite behavior before running the script.

Risk: A script generated for the wrong part, dimensions, or file path could produce incorrect CAD output or affect important files.

Mitigation: Test generated automation on copies of important CAD files before using it on production models.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2009730/skills/solikworks-auto)
- [ClawHub publisher profile](https://clawhub.ai/user/2009730)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python code blocks and step-by-step operating guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code is expected to include Chinese comments, COM initialization, SolidWorks connection handling, exception handling, and user-specified dimensions, filenames, paths, and save/export behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
