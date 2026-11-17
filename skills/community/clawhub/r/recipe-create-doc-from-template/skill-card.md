## Description:

Copy a Google Docs template, fill in content, and share with collaborators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace automation users use this recipe to copy a Google Docs template, add specified content, and share the resulting document with collaborators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Placeholder template or document IDs could be left unchanged or replaced with the wrong Google Doc target.

Mitigation: Replace TEMPLATE_DOC_ID and NEW_DOC_ID with the intended document IDs before execution.

Risk: Granting writer access to the wrong collaborator can expose or alter document contents.

Mitigation: Confirm the collaborator email and that writer access is appropriate before creating the permission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/recipe-create-doc-from-template)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command and the gws-drive and gws-docs skills; uses placeholder document IDs, content, and collaborator email values.]

## Skill Version(s):

1.0.12 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
