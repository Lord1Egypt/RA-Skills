## Description:

Integrate SanctifAI Trust Proof-of-Human attestations when an app needs cryptographic proof a human performed a task or human-in-the-loop verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanctifai](https://clawhub.ai/user/sanctifai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to integrate SanctifAI Trust Proof-of-Human attestations into controlled apps, external worker flows, or agent chat workflows and receive participation IDs and certificate URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented flows may expand third-party data and code trust beyond the strongest privacy claims.

Mitigation: Keep taskData and resultData opaque; avoid PII, credentials, regulated data, and confidential business details; and compute commitments locally where possible.

Risk: Hosted script use can place third-party code on privileged application pages.

Mitigation: Require a pinned version, SRI, CSP controls, or self-hosting before using it on privileged application pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanctifai/skills/sanctifai-trust)
- [SanctifAI Trust homepage](https://trust.sanctifai.com)
- [SanctifAI Trust pricing](https://sanctifai.com/trust/pricing)
- [SanctifAI Trust chat bridge skill](https://bridge.trust.sanctifai.com/skill.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript, JSON, shell command, and API flow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes integration guidance for embedded, browser extension, and chat bridge attestation flows.]

## Skill Version(s):

1.0.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
