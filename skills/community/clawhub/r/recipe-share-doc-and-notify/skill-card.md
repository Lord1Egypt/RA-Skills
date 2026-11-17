## Description:

Share a Google Docs document with edit access and email collaborators the link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace operators use this recipe to locate a Google Docs document, share it with a collaborator, and email the document link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can grant writer access to the wrong Google Docs file or recipient if placeholders are not checked.

Mitigation: Confirm the document ID, recipient email address, and required permission level before executing the sharing command.

Risk: Editor access may be broader than necessary for some review workflows.

Mitigation: Use viewer or commenter access unless the collaborator explicitly needs edit permission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/recipe-share-doc-and-notify)
- [Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Google Workspace CLI commands and requires gws plus gws-drive, gws-docs, and gws-gmail.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
