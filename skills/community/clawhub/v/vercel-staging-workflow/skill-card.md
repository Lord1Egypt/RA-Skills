## Description:

Set up a Vercel staging and production workflow using GitHub Actions and stable URL aliases that automatically update a permanent staging URL after pushes to main.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgrobelny](https://clawhub.ai/user/danielgrobelny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add a GitHub Actions workflow that keeps a Vercel staging alias pointed at the latest main deployment while leaving production promotion separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can point a trusted staging URL at the wrong Vercel deployment if the deployment for the triggering commit is not found.

Mitigation: Remove the fallback to the latest READY deployment and fail closed unless the workflow verifies that the deployment belongs to the triggering commit and main branch.

Risk: A broadly scoped Vercel token could increase impact if the workflow or repository secrets are misused.

Mitigation: Use a least-privilege Vercel token scoped to the intended project and store it only in the required GitHub secret.

## Reference(s):

- [GitHub Action Template](references/github-action-template.yml)
- [ClawHub Skill Page](https://clawhub.ai/danielgrobelny/skills/vercel-staging-workflow)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with YAML workflow and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a project-specific Vercel staging alias workflow that requires user-provided Vercel token and project or team identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
