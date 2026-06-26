## Description: <br>
Optimize Vercel build and deploy speed \u2014 audit checklist for new and existing projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to triage Vercel build speed, deploy queue bottlenecks, rollback readiness, and framework-specific optimization opportunities for new or existing projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow examples use Vercel credentials and project identifiers; mishandling them could expose deployment access. <br>
Mitigation: Scope Vercel tokens narrowly, store them only in GitHub Secrets or equivalent secret storage, and keep .vercel/.env* files out of commits, caches, artifacts, and logs. <br>
Risk: Deployment, rollback, or CI workflow changes can affect production availability if applied without review. <br>
Mitigation: Review workflows before committing them, and use approvals or branch protections before production deploys or rollbacks. <br>
Risk: Applying ISR to auth-gated or per-user pages can cache content that should remain user-specific. <br>
Mitigation: Follow the skill's triage guidance to skip ISR for auth-gated apps and review route behavior before enabling cacheable dynamic responses. <br>


## Reference(s): <br>
- [Detailed Vercel Speed Optimization Checklist](docs/checklist.md) <br>
- [Framework-Agnostic Vercel Optimizations](docs/general.md) <br>
- [GitHub Actions + vercel deploy --prebuilt Guide](docs/github-actions-prebuilt.md) <br>
- [SvelteKit-Specific Vercel Optimizations](docs/sveltekit.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and workflow YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend Vercel dashboard settings, CLI checks, CI workflow changes, and report notes based on build-time triage.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
