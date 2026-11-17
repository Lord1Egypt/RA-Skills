## Description:

Generates Chinese software copyright application materials, including application-form content, software manual text, technical document checklists, and source-code formatting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grancy-zgs](https://clawhub.ai/user/grancy-zgs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and applicants preparing Chinese software copyright registration materials use this skill to turn basic software details into application-form content, a software manual, a technical document checklist, and source-code submission guidance.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The helper script can automatically run an unpinned package install for python-docx when the dependency is missing.

Mitigation: Review the script before use, run it in an isolated environment, or remove the automatic install behavior and install reviewed dependencies explicitly.

Risk: The security verdict is suspicious despite no listed risk findings.

Mitigation: Review the skill before installing or running it, and treat generated filing materials as drafts that require user verification before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grancy-zgs/skills/software-copyright-doc-generator)
- [Software copyright source-code format requirements](references/源代码格式要求.md)
- [Software copyright application-form instructions](references/申请表填写说明.md)
- [Software manual template](references/软件说明书模板.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown guidance plus generated DOCX and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a copyright application form, software manual, and technical document checklist in a local output directory.]

## Skill Version(s):

1.0.0 (source: server release and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
