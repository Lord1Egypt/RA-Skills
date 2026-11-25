## Description:

Probe any OpenAI-compatible LLM endpoint to list all model IDs, verify which actually work, and diff against local config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxpj](https://clawhub.ai/user/frankxpj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to inspect model IDs exposed by an OpenAI-compatible endpoint, test whether configured models are callable, and compare endpoint results with local provider configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy credentials may be exposed when sent over plaintext HTTP.

Mitigation: Avoid using sensitive proxy credentials until their handling and validation behavior have been independently verified.

## Reference(s):

- [XPJ Probe Models on ClawHub](https://clawhub.ai/frankxpj/skills/xpj-probe-models)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain-text terminal report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports model IDs, callability checks, and differences from local provider configuration.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
