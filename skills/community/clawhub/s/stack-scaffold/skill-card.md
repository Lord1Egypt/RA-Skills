## Description:

Scaffolds a full-stack project with Next.js App Router, Supabase, Firebase Auth, Vercel, and Cloudflare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Stack Scaffold to create new full-stack Next.js projects with Supabase, Firebase Auth, Vercel configuration, Cloudflare-oriented follow-up steps, tests, and starter environment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs live npm and npx scaffolding and dependency installation commands that may resolve changing package versions.

Mitigation: Review the generated plan before execution, run it only in a new or empty project directory, and pin package or CLI versions when repeatability is required.

Risk: The scaffold includes Firebase admin credential environment variables that should not be collected during initial project creation.

Mitigation: Do not provide production private keys while scaffolding; populate credentials later in a restricted environment or secret manager.

Risk: The workflow creates files, initializes git, and makes commits in the target directory.

Mitigation: Confirm the target path before execution and review generated files before deploying or connecting production services.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file paths, code blocks, shell commands, configuration snippets, and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a new project scaffold, environment template guidance, dependency installation steps, and recommended follow-up skill sequence.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
