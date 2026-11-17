## Description:

UXLens audits websites for UX, UI, and accessibility issues with 600+ checkpoints, detailed reports, full-site crawls, and redesign comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misothecod](https://clawhub.ai/user/misothecod)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agencies, indie builders, and AI agents use UXLens to audit websites for UX, UI, accessibility, Core Web Vitals, and redesign regressions before launch or handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs and pages reached during full-site crawls are processed by the UXLens third-party service.

Mitigation: Avoid private, internal, staging, localhost, authenticated, or client-sensitive sites unless authorized and comfortable with that exposure.

Risk: The skill requires a UXLENS_API_KEY credential.

Mitigation: Protect the API key like any other service credential and avoid committing or sharing it.

## Reference(s):

- [UXLens homepage](https://uxlens.io)
- [UXLens dashboard](https://uxlens.io/dashboard)
- [ClawHub skill page](https://clawhub.ai/misothecod/skills/uxlens)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Configuration]

**Output Format:** [Structured JSON with an agent-readable text summary, scores, issue lists, and prioritized fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UXLENS_API_KEY and sends submitted URLs to the UXLens API for audit processing.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
