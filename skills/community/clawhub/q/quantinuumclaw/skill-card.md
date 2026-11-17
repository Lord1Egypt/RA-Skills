## Description:

Enables building and deploying quantum computing applications with Quantinuum, Guppy, Selene, and Fly.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:


## Use Case:

Developers, engineers, and healthcare hackathon participants use this skill to scaffold, customize, and deploy quantum-powered web applications and APIs for clinical, healthcare, and general quantum computing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and deploy public cloud services that may be unsuitable for production without hardening.

Mitigation: Review generated services before deployment, add authentication and rate limits, restrict CORS, and avoid the one-command deployment path for production releases.

Risk: Clinical workflows could expose PHI or PII to quantum backends or Fly.io services.

Mitigation: Use synthetic or de-identified data unless a compliance plan, data residency review, and required agreements are in place.

Risk: Secrets may be exposed through frontend environment variables or uploaded to Fly.io without sufficient review.

Mitigation: Keep API keys server-side, do not put API keys in VITE_* frontend variables, and manually review each secret before setting or importing it.

Risk: Installer and dependency guidance includes commands and placeholder package versions that need verification.

Mitigation: Inspect installer scripts before execution and replace placeholder dependency guidance with verified pinned packages.

## Reference(s):

- [Clinical Use Cases](references/clinical-use-cases.md)
- [Fly.io Configuration](references/flyio_config.md)
- [Guppy Guide](references/guppy_guide.md)
- [Lovable Patterns](references/lovable_patterns.md)
- [Selene API](references/selene_api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, configuration files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold FastAPI backend files, Fly.io deployment configuration, and React/TypeScript frontend files.]

## Skill Version(s):

0.1.0 (source: server release metadata and frontend package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
