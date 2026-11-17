## Description:

Helps developers diagnose blocked or failed Vercel deployments, static-export 404s, oversized webhooks, and deployment routing issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify the actual deployment state, troubleshoot configuration and routing errors, and plan safe fixes for oversized webhook events or DNS cutovers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Vercel access token may expose team deployment information.

Mitigation: Use a team-scoped token from an environment variable and do not print or commit it.

Risk: The optional webhook relay may retain events containing personal data or lose events on ephemeral storage.

Mitigation: Use protected persistent storage, forward only necessary fields, and schedule deletion of quarantined events.

Risk: Unverified webhook input or an untrusted forward destination could expose data.

Mitigation: Verify webhook signatures on raw payloads and use a trusted HTTPS forward target.

Risk: Enabling npm install scripts can run third-party code.

Mitigation: Review the package before allowing its install scripts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alexbloch-ia/skills/vercel-deploy)
- [Vercel documentation](https://vercel.com/docs)
- [Vercel configuration schema](https://openapi.vercel.sh/vercel.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with diagnostic summaries and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnosis identifies supporting evidence and whether the proposed fix was verified.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
