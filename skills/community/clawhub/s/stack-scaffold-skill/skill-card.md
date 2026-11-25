## Description:

Scaffold a runnable Next.js 15 app with Tailwind, a Supabase client, and Stripe checkout plus a signature-verified webhook. Runs in mock mode with zero keys, and an environment check blocks "done" until the required variables are present and valid. Use when asked to scaffold or start a new fullstack app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winsoftlabs30](https://clawhub.ai/user/winsoftlabs30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold a runnable Next.js app with Supabase and Stripe integration, including mock mode for development without service keys. It guides setup and environment checks for switching to real integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer is not version-pinned and could fetch changed code later.

Mitigation: Review the release source and confirm the installed version before relying on it.

Risk: Some paths referenced in SKILL.md were absent from the scan, leaving those references unverified.

Mitigation: Check the referenced files and review their contents before using those parts of the workflow.

## Reference(s):

- [Stack Scaffold on ClawHub](https://clawhub.ai/winsoftlabs30/skills/stack-scaffold-skill)
- [Publisher profile: winsoftlabs30](https://clawhub.ai/user/winsoftlabs30)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Next.js TypeScript project files with Markdown setup guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mock mode is supported by default; real Supabase and Stripe integrations require valid environment variables.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
