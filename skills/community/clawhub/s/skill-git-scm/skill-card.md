## Description:

Clones a Git repository to a local path or updates an existing local Git checkout from a target branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lentiancn](https://clawhub.ai/user/lentiancn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to clone a Git repository into a chosen local directory or update an existing checkout on a specified branch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Updating an existing directory may pull from that directory's current origin instead of the remote URL supplied for the operation.

Mitigation: Before using the skill on an existing directory, confirm that the path is the intended repository and that its origin remote matches the expected URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lentiancn/skills/skill-git-scm)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash command examples and stdout status strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns SUCCESS or ERROR status text on stdout.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
