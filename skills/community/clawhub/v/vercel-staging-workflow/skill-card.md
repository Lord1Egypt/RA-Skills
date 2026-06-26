## Description: <br>
Set up a staging and production workflow for Vercel projects using GitHub Actions and stable URL aliases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgrobelny](https://clawhub.ai/user/danielgrobelny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create a GitHub Actions workflow that keeps a stable Vercel staging alias pointed at the latest main-branch deployment while keeping production separate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broadly reused or mishandled Vercel token could expose deployment control beyond the intended staging workflow. <br>
Mitigation: Store the token only in GitHub Actions secrets, scope and rotate it where possible, and avoid broad organization-level reuse unless necessary. <br>
Risk: If the workflow cannot match the triggering commit, falling back to the latest ready deployment could point staging at an unintended build. <br>
Mitigation: Consider changing the workflow to fail when it cannot find the exact deployment for the triggering commit. <br>
Risk: Using the alias outside staging could blur the separation between staging and production releases. <br>
Mitigation: Verify that the configured alias is only for staging and keep production deployment promotion separate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielgrobelny/vercel-staging-workflow) <br>
- [GitHub Action template](references/github-action-template.yml) <br>
- [Vercel account tokens](https://vercel.com/account/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with YAML workflow configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a GitHub Actions workflow template and setup steps for Vercel staging aliases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
