## Description:

Analyze Vercel project configurations, including vercel.json, framework detection, build settings, edge functions, headers, redirects, rewrites, environment variables, and deployment performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review, debug, and optimize Vercel deployments before production issues occur. It focuses on configuration correctness, security headers, environment-variable exposure, routing behavior, serverless and edge runtime choices, and build performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment-variable reviews could expose secret values if the agent prints raw .env or Vercel variable contents.

Mitigation: Report variable names, exposure risks, and configuration fixes without printing secret values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/vercel-config-analyzer)

## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown report with findings, recommendations, and optional configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity-grouped findings, security-header review, environment-variable exposure notes, performance observations, and a suggested vercel.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
