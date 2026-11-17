## Description:

Mise en place d'un workspace agent dedie pour un nouveau client TNCG, couvrant la creation du workspace, les fichiers de base, la configuration OpenClaw, le lien WhatsApp, le sandbox, l'escalation et le monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superworldsavior](https://clawhub.ai/user/superworldsavior)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to onboard a dedicated OpenClaw agent workspace for a TNCG client, including base Markdown files, WhatsApp routing, sandbox configuration, escalation, credential setup, and final verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client agents may receive broad messaging, session, network, and credential access during onboarding.

Mitigation: Install only in a controlled OpenClaw environment and tighten tenant boundaries before use.

Risk: Wildcard outbound WhatsApp sending can allow messages beyond the intended client scope.

Mitigation: Replace wildcard outbound sending with explicit allowlists for approved recipients.

Risk: Global session visibility and shared host-service bridges can expose cross-agent or cross-tenant access paths.

Mitigation: Use tenant-aware authenticated access, avoid global session visibility for client agents, and review host-service bridge exposure.

Risk: Shared production secrets or weak credential storage can leak credentials across sandboxes.

Mitigation: Use per-agent credentials, avoid shared production secrets in sandboxes, and harden credential storage.

Risk: Unpinned installed skills, sandbox images, or legacy hardcoded cron and Git token URL patterns can create unstable or unsafe deployments.

Mitigation: Pin installed skills and sandbox images, and avoid legacy hardcoded cron jobs or Git token URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superworldsavior/skills/setup-client-workspace)
- [Workflow - Setup client workspace](artifact/references/workflow.md)
- [OpenClaw config - client workspace](artifact/references/openclaw-config.md)
- [Checklist finale + securite](artifact/references/security-checklist.md)
- [Templates fichiers workspace](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace setup instructions and file/configuration templates for an agent operator.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
