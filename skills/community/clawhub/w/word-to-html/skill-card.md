## Description:

Converts Word documents (.docx and .doc) to clean HTML through mineru-open-api, preserving formatting, tables, images, and layout when supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and publishing teams use this skill to convert Word documents into HTML for web publishing, CMS migration, email templates, and document digitization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents may be sent to the third-party MinerU service without an explicit privacy confirmation step.

Mitigation: Use the skill only for documents approved for that data flow and avoid confidential or regulated files unless that transfer has been reviewed.

Risk: The installation guidance uses an unpinned global npm package.

Mitigation: Prefer a pinned, local, non-admin install in a restricted environment and review the package before use.

## Reference(s):

- [MinerU API token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown guidance with bash commands and generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an output directory under ~/MinerU-Skill/<name>_<hash>/ and may require a MinerU token for precision extraction or HTML export.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
