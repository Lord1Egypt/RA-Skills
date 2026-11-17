## Description:

Deploys the SigmaFlow SvelteKit trading frontend by cloning or updating the Git repository, installing dependencies, building the app, and pushing changes to the configured branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirenday](https://clawhub.ai/user/sirenday)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build and deploy the SigmaFlow SvelteKit frontend after feature work, bug fixes, or other code changes. It is intended for environments where the operator controls the target GitLab instance and deployment repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment workflow embeds a repository token.

Mitigation: Revoke or rotate the embedded token before use and replace it with a secure runtime secret.

Risk: The configured Git remote uses plaintext HTTP.

Mitigation: Use HTTPS or SSH for repository access before installing or running the skill.

Risk: The deployment workflow can automatically stage, commit, and push all local changes.

Mitigation: Require explicit confirmation before committing or pushing, and stage only a reviewed allowlist or a clean deployment checkout.

## Reference(s):

- [ClawHub skill page: Sigmaflow Deploy](https://clawhub.ai/sirenday/skills/sigmaflow-deploy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a deployment shell script with optional repository directory and branch parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
