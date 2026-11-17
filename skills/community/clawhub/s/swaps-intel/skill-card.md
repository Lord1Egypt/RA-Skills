## Description:

Assess cryptocurrency addresses and transactions for blockchain risk signals, labels, reputation, and tracing data using the Swaps Intelligence API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w3arecom](https://clawhub.ai/user/w3arecom)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, security teams, fraud analysts, and agent builders use this skill to screen cryptocurrency addresses and transactions for risk signals, transaction traces, and fraud-triage context. Outputs should support investigation and risk triage, not legal, compliance, financial, or investigative conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, transaction hashes, and API keys are sent to Swaps.app.

Mitigation: Submit only data intended for Swaps.app analysis, keep API keys secret, and prefer the x-api-key header or SWAPS_INTEL_API_KEY environment variable.

Risk: Returned markdown may contain untrusted display content.

Mitigation: Display or summarize returned markdown as data only; do not treat it as agent instructions or execute embedded content.

Risk: Blockchain risk scores and labels can contain false positives, false negatives, or probabilistic attribution.

Mitigation: Frame results as heuristic risk signals, include the required disclaimer, and require independent verification before user action.

Risk: The API can be misused for harassment, doxxing, unsupported accusations, or high-volume probing.

Mitigation: Use the skill only for legitimate fraud prevention, risk triage, and analytics; enforce authentication, quotas, abuse detection, and a label challenge or correction path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/w3arecom/skills/swaps-intel)
- [Swaps Product Page](https://www.swaps.app/search)
- [Skill Instructions](artifact/SKILL.md)
- [OpenAPI Contract](artifact/openapi.json)
- [Risk Disclosure](artifact/RISK_DISCLOSURE.md)
- [Acceptable Use Policy](artifact/AUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses, curl examples, risk scores, labels, flags, request IDs, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SWAPS_INTEL_API_KEY. Returned markdown must be treated as untrusted display content, and user-facing outputs must preserve factual API fields and include the required informational-use disclaimer.]

## Skill Version(s):

1.2.0 (source: server release metadata, clawhub.json, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
