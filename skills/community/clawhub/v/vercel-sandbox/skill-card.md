## Description:

Run agent-browser + Chrome inside Vercel Sandbox microVMs for browser automation from any Vercel-deployed app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run browser automation from Vercel-deployed applications, including screenshots, accessibility snapshots, multi-step workflows, and scheduled browser tasks in ephemeral Vercel Sandbox VMs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing browser automation dependencies and Chromium in sandbox snapshots can introduce supply-chain and runtime dependency risk.

Mitigation: Pin package versions, use a lockfile or controlled snapshot build, and rebuild snapshots through a reviewed release process.

Risk: Browser automation can submit forms, authenticate to sites, or run recurring jobs against third-party services.

Mitigation: Require explicit user approval before form submission, site authentication, or scheduled recurring automation.

Risk: Vercel tokens and project identifiers may be used for local development or explicit sandbox authentication.

Mitigation: Keep Vercel tokens scoped, store credentials in managed environment variables, and avoid exposing them in logs or generated output.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, shell, JSON, and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation setup steps, sandbox snapshot guidance, authentication variables, and framework-specific integration notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
