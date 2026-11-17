## Description:

Guides an agent through deploying local code to Railway with `railway up`, including detach and CI modes, target selection, commit messages, and common deployment errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dbanys](https://clawhub.ai/user/dbanys)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to deploy local application changes to Railway, choose an appropriate deploy mode, target a linked or specified service, and respond to common build or linking errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide Railway deployments and broad infrastructure changes using the user's Railway CLI authentication.

Mitigation: Require explicit confirmation of the target project, environment, and service before running Railway commands.

Risk: The referenced Railway environment configuration can include service, volume, or variable deletion.

Mitigation: Do not perform deletion or admin changes unless the user intentionally requested them and has backups or a rollback plan.

## Reference(s):

- [Railpack Reference](references/railpack.md)
- [Environment Config Reference](references/environment-config.md)
- [Monorepo Reference](references/monorepo.md)
- [Variables Reference](references/variables.md)
- [Railpack documentation](https://railpack.com/llms.txt)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct use of the Railway CLI with the user's active Railway authentication and selected project, environment, and service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
