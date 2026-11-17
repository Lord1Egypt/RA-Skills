## Description:

Create and manage widgets on the user's WonderDash mobile dashboard via GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hay-wired](https://clawhub.ai/user/hay-wired)

### License/Terms of Use:


## Use Case:

External users use WonderDash to create, update, order, archive, and delete mobile dashboard widgets stored as JSON files in a GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses an SSH private key for GitHub repository access.

Mitigation: Treat the deploy key as a secret, scope it to the intended wonderdash-widgets repository, avoid logging or sharing it, and remove the local key and SSH config entry when the integration is no longer needed.

Risk: Permanent widget deletion removes files from the active repository while git history may still retain prior content.

Mitigation: Archive widgets when unsure, and reserve permanent deletion for content that has been reviewed and is intended to be removed from the active dashboard repository.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hay-wired/skills/wonderdash)
- [ClawHub Publisher Profile](https://clawhub.ai/user/hay-wired)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained widget JSON and dashboard index changes for a GitHub-backed WonderDash dashboard.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
