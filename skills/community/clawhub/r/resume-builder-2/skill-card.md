## Description:

Build, rewrite, and tailor premium white-collar resumes from real candidate information, then render the final resume to PDF with Typst.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hilaraklesantosw-art](https://clawhub.ai/user/hilaraklesantosw-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to build, rewrite, or tailor factual white-collar resumes and produce structured resume data, Typst source, and a rendered PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles personal resume and contact details.

Mitigation: Keep candidate information local, review generated files before sharing, and avoid adding unsupported facts.

Risk: PDF rendering depends on Typst and a resume template that evidence says may be missing.

Mitigation: Confirm python3, typst, and the Typst template are present before relying on PDF output; treat compilation failure as incomplete.

Risk: Resume tailoring can overstate a candidate's background if facts are not constrained.

Mitigation: Use only candidate-provided facts, avoid invented metrics or responsibilities, and make important gaps explicit.

## Reference(s):

- [Resume schema](references/resume-schema.md)
- [Role writing guidelines](references/role-writing-guidelines.md)
- [Project homepage](https://github.com/hilaraklesantosw-art/skills)
- [ClawHub skill page](https://clawhub.ai/hilaraklesantosw-art/skills/resume-builder-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON resume data, Typst source, file paths, and PDF output status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and typst; PDF output is complete only when resume.pdf exists.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
