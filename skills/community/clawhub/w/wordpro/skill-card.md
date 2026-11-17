## Description:

Helps agents create, read, edit, validate, convert, and manipulate Microsoft Word .docx documents, including formatted documents, tracked changes, comments, images, and content extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-focused agents use this skill to produce polished Word documents and to inspect or modify existing DOCX files, including tracked changes, comments, images, tables, and Office XML validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unsafe LibreOffice macro and LD_PRELOAD mechanisms.

Mitigation: Review before installing, run only in a contained workspace, and avoid sensitive documents until the LibreOffice macro/profile and LD_PRELOAD temp-file issues are fixed.

Risk: The security scan reports broader Office-file handling than the advertised DOCX scope.

Mitigation: Treat PPTX and XLSX support as outside the advertised DOCX scope unless separately reviewed and approved.

Risk: The skill depends on local tools and packages such as LibreOffice, pandoc, poppler utilities, and docx-js.

Mitigation: Pin and install dependencies locally in a controlled environment before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/wordpro)
- [Publisher profile](https://clawhub.ai/user/fslong520)
- [Artifact license terms](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create or modify DOCX files and to run local validation, conversion, unpacking, packing, commenting, and tracked-change helper scripts.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
