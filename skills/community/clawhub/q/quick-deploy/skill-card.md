## Description:

Quick Deploy helps agents deploy projects to Vercel, Netlify, or Fly.io by detecting the framework, choosing a hosting target, running deployment commands, and reporting the resulting URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanthienha199](https://clawhub.ai/user/vanthienha199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent detect common web and backend project types, select Vercel, Netlify, or Fly.io, and run the corresponding deploy, status, rollback, log, or domain commands. It defaults to preview or staging deployment and requires confirmation before production deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install mutable external deployment CLIs globally and run the Fly.io remote installer before deployment.

Mitigation: Review the skill before installing, prefer manually installed and trusted pinned CLIs, and only allow remote installer use after explicit approval.

Risk: The skill can deploy real projects and affect production environments.

Mitigation: Default to preview or staging deployment, require explicit confirmation for production targets, and verify the selected platform, project, and environment before execution.

Risk: Deployment workflows may involve service credentials or API tokens.

Mitigation: Use each provider CLI's built-in authentication flow and do not store, print, or expose API tokens.

## Reference(s):

- [Quick Deploy on ClawHub](https://clawhub.ai/vanthienha199/skills/quick-deploy)
- [Fly.io installer referenced by artifact](https://fly.io/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and deployment status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment URLs, framework detection results, platform recommendations, command output, errors, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
