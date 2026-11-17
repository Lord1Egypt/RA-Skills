## Description:

A cross-border commerce compliance helper that returns structured Yufluent cloud recommendations for certification checklists, tariff estimates, labeling requirements, and platform rule checks, with legal and tax review required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce operators use this skill to route product, market, material, HS-code, and platform details to Yufluent for cross-border compliance reference output. It supports certification, tariff, labeling, and marketplace-rule workflows, but its results are advisory and require human verification against official sources and current regulations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and business data can be sent to a configured cloud endpoint.

Mitigation: Install only when the Yufluent service is trusted, protect TOKENAPI_KEY as a reusable credential, and leave TOKENAPI_BASE_URL unset unless a trusted HTTPS endpoint is intentionally configured.

Risk: Free-form compliance context may contain unnecessary secrets, personal data, or commercially sensitive details.

Mitigation: Provide only the product and trade details needed for the compliance question and avoid including unrelated secrets or personal data.

Risk: Compliance, tariff, labeling, and platform-rule outputs may be incomplete or stale for legal or tax decisions.

Mitigation: Treat outputs as reference guidance and require human review against official sources and current regulations before acting.

Risk: The package has a local import-path weakness identified by security evidence.

Mitigation: Run the skill in a controlled environment and review local files and dependency paths before installation or execution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/metahuan/skills/yufluentcn-compliance-guard)
- [Yufluent homepage](https://claw.changzhiai.com)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Structured JSON recommendations and formatted text from a cloud skill run, usually invoked through CLI shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY. Optional TOKENAPI_BASE_URL changes the API endpoint. Outputs are non-legal, non-tax advisory references that require human review.]

## Skill Version(s):

1.1.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
