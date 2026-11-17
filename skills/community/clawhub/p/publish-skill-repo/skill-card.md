## Description:

Helps developers publish a local Skill project to GitHub and synchronize it to ClawHub, with automated setup for new projects and guided release steps for existing repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouchang1988](https://clawhub.ai/user/zhouchang1988)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to prepare and release Skill repositories by checking prerequisites, creating or updating GitHub repository assets, configuring ClawHub publishing, and tagging releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify GitHub repositories, commit non-ignored files, push branches, and create tags.

Mitigation: Verify the target repository and origin before publishing, review staged files for secrets or unintended content, and confirm the release tag before pushing.

Risk: The workflow handles a long-lived ClawHub token and stores it as a GitHub secret.

Mitigation: Confirm the destination repository before setting the secret, limit token exposure, and rotate the token if it may have been added to the wrong repository.

Risk: The generated workflow installs the ClawHub CLI without a pinned version.

Mitigation: Pin the ClawHub CLI version in the workflow when repeatable releases or supply-chain control are required.

## Reference(s):

- [README](README.md)
- [ClawHub skill page](https://clawhub.ai/zhouchang1988/skills/publish-skill-repo)
- [ClawHub](https://clawhub.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated repository or workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update repository files, GitHub Actions configuration, commits, branches, tags, and repository secrets.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
