## Description:

Guide pas a pas pour coder avec OpenAI Codex CLI, gerer un repo GitHub, et deployer sur un serveur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikiane](https://clawhub.ai/user/mikiane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a French step-by-step guide for installing and authenticating Codex CLI, managing GitHub repositories, and deploying applications through Coolify, Railway, SSH, Docker, or related provider tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes examples using Codex CLI with sandbox isolation disabled, which can expose local files or credentials if run on a sensitive machine.

Mitigation: Avoid danger-full-access unless necessary, and run it only in an isolated disposable environment without production credentials.

Risk: GitHub tokens, deployment tokens, and SSH keys are required for some workflows and may grant broad access if overprivileged or committed to source control.

Mitigation: Use least-privilege credentials, store secrets in environment variables or deployment secret stores, and never commit real tokens, keys, passwords, or .env files.

Risk: Deployment commands can affect live infrastructure when copied into a real project or server environment.

Mitigation: Review commands before execution, test in staging, configure rollback steps, and require human validation before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikiane/skills/qapten-codex)
- [OpenAI Codex docs](https://developers.openai.com/codex/)
- [Coolify docs](https://coolify.io/docs)
- [Railway docs](https://docs.railway.app)
- [Cloudflare DNS API](https://developers.cloudflare.com/api/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks, checklists, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [French-language operational guidance with placeholders for user-specific credentials, repository names, deployment endpoints, and server paths]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
