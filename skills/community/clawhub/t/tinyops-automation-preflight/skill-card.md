## Description:

Audits public webpages for automation and integration readiness through TinyOps paid service endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinyopsstudio](https://clawhub.ai/user/tinyopsstudio)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to request evidence-backed readiness findings, launch gates, acceptance tests, and remediation priorities for public, unauthenticated webpages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid third-party page-analysis service receives the submitted target URL.

Mitigation: Submit only public, unauthenticated HTTP or HTTPS URLs and confirm current payment requirements before any purchase.

Risk: The bundled Action and CLI handle a RapidAPI key.

Mitigation: Store the key in GitHub Actions secrets or an equivalent secret store, do not write it to reports, and avoid exposing it in logs.

Risk: The API base URL can be overridden in the environment.

Mitigation: Set AUTOMATION_PREFLIGHT_API_BASE_URL only in controlled tests and use pinned commits or exact release versions for installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinyopsstudio/skills/tinyops-automation-preflight)
- [TinyOps x402 OpenAPI document](https://x402-preflight.tinyopsstudio.com/openapi.json)
- [Automation Integration Preflight API on RapidAPI](https://rapidapi.com/tinyopsstudio/api/automation-integration-preflight)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Concise Markdown summaries with optional raw JSON artifacts and shell or workflow snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-authorized x402 payment or a RapidAPI key; outputs should preserve uncertainty and distinguish observed page evidence from recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
