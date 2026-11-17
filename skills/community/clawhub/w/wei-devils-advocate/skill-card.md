## Description:

Stress-test ideas using multiple LLMs in adversarial roles to generate counterarguments, cross-check reasoning, and expose hidden risks and failure modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikehankk](https://clawhub.ai/user/mikehankk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, strategists, and analysts use this skill to stress-test decisions, product ideas, technical plans, investment theses, and prompts by generating adversarial counterarguments, failure scenarios, and a judge evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup includes a curl-to-bash install path for Bun.

Mitigation: Review the setup path before installation and prefer a package-manager or otherwise verified Bun install source.

Risk: Prompts, raw model outputs, judge results, reports, and debug responses can be saved locally in plaintext.

Mitigation: Avoid submitting secrets, personal data, regulated data, or confidential business material, and review or delete intermediate/ and reports/ after use.

Risk: Inputs and outputs are sent to configured external LLM providers.

Mitigation: Use only provider configurations approved for the data being analyzed and confirm API-key handling before running the skill.

Risk: Package metadata version differs from the release and frontmatter version.

Mitigation: Wait for the publisher to align package metadata if strict provenance or release traceability matters to the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikehankk/skills/wei-devils-advocate)
- [Bun runtime](https://bun.sh)
- [Bun environment variable documentation](https://bun.sh/docs/runtime/env)
- [Devil's Advocate simulation preview](https://www.bigbigai.com/agent/devils-advocate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured text or JSON containing the thesis, hidden assumptions, counterarguments, failure scenarios, survivability, verdict, and recommendation; local report and intermediate text files may also be written.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured external LLM providers and may retain prompts, model responses, judge output, reports, and debug responses in local plaintext files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
