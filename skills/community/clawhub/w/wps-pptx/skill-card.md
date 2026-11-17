## Description:

Supports creating, reading, and editing .pptx presentation files, including generating slides, extracting content, modifying layouts, and applying templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to inspect existing PowerPoint files, create new presentations, or edit slide content and layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references workflow guide files that are not included, so reading, creation, or editing flows may fail or behave inconsistently.

Mitigation: Supply and review the referenced PPTX guide files before deployment, then test the read, create, and edit workflows with representative presentations.

Risk: The skill reads and writes presentation files, which can expose document content or overwrite outputs if filenames and paths are not checked.

Mitigation: Run it in a controlled workspace, review input and output paths before execution, and inspect generated files before sharing them.

Risk: The workflow is written in Chinese, which may make behavior harder to review for teams that do not read Chinese.

Mitigation: Have a Chinese-capable reviewer confirm the workflow and operational guidance before enabling it for broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/skills/wps-pptx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, code snippets, shell commands, configuration notes, and .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presentation-file workflows may require referenced guide files that are not present in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
