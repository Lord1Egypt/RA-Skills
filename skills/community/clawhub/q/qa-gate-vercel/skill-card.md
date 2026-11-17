## Description:

Pre-production validation gate for Vercel, Supabase, and Firebase stacks that generates test plans, runs validation suites, checks APIs, UI, toast behavior, LLM output quality, and produces go/no-go reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill before production deployment to plan and run QA validation for Vercel, Supabase, and Firebase applications. It helps validate API routes, server actions, auth flows, UI behavior, toast notifications, LLM-powered features, database integrity, and deployment readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QA prompts and model outputs may be sent to OpenRouter for LLM-as-judge evaluation.

Mitigation: Use test accounts and non-production data, avoid sensitive prompts, and ensure OPENROUTER_API_KEY is scoped for validation use.

Risk: npx-based test tooling may run dependencies in the project environment.

Mitigation: Prefer preinstalled or pinned test dependencies and review generated commands before execution.

Risk: Validation workflows reference Vercel and Supabase tokens and service endpoints.

Mitigation: Scope Vercel and Supabase credentials minimally, use test environments, and redact secrets from generated reports.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, TypeScript test files, and shell command sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces qa-reports and qa-tests artifacts; generated validations may call OpenRouter, Vercel, and Supabase services when configured.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
