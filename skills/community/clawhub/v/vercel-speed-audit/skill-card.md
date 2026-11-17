## Description:

Optimize Vercel build and deploy speed — audit checklist for new and existing projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to audit Vercel projects, choose relevant build and deployment speed optimizations, and document findings for new or existing applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CI deployment examples affect production infrastructure and may copy unpinned tooling or broad production deployment tokens into workflows.

Mitigation: Review workflow examples before copying them, pin the Vercel CLI and GitHub Actions to reviewed versions or commit SHAs, and use narrowly scoped Vercel tokens with protected GitHub environments for production deploys.

Risk: Build and deployment optimization guidance can change production deployment behavior.

Mitigation: Apply changes incrementally, test them in preview or staging environments, and keep rollback procedures documented before changing production settings.

## Reference(s):

- [Vercel Speed Audit skill page](https://clawhub.ai/brennerspear/skills/vercel-speed-audit)
- [Detailed checklist](docs/checklist.md)
- [Framework-agnostic Vercel optimizations](docs/general.md)
- [GitHub Actions prebuilt deployment guide](docs/github-actions-prebuilt.md)
- [SvelteKit-specific Vercel optimizations](docs/sveltekit.md)
- [Vercel token settings](https://vercel.com/account/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, shell commands, configuration snippets, and CI workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project-specific report files such as vercel-speed-report.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
