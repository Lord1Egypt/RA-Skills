## Description:

Fork, clone, and set up a GitHub repository for development or contribution by handling fork creation, clone authentication, upstream remote configuration, branch creation from upstream, and dependency installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliverp](https://clawhub.ai/user/sliverp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare GitHub repositories for contribution, onboarding, or codebase exploration by forking, cloning, configuring remotes, creating branches, and installing project dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub tokens can be exposed if cloned through token-in-URL patterns or stored in shell profiles.

Mitigation: Use GitHub CLI authentication, SSH, or a credential helper, and avoid storing GH_TOKEN in a shell profile.

Risk: Dependency installation and build commands from target repositories can execute untrusted project logic in the user's normal environment.

Mitigation: Run install and build commands only for trusted repositories, or use an isolated environment without unrelated secrets.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local repository setup workflow with command examples and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
