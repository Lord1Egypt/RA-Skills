## Description:

Validate Rollup config files (rollup.config.js/mjs/ts) for output format conflicts, plugin ordering issues, deprecated options, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build engineers use this skill to validate JSON Rollup config exports, audit build pipeline settings, migrate Rollup versions, and produce CI-friendly findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Node require() conversion command can execute project code when converting a Rollup JavaScript config.

Mitigation: Run that conversion only for trusted repositories, or use a disposable sandbox with no secrets and no network access before validating the resulting JSON.

Risk: Validation coverage is limited for normal Rollup JS, MJS, and TS configs because the validator checks JSON config representations.

Mitigation: Export or translate configs to reviewed JSON first and treat findings as static guidance rather than a complete Rollup compatibility assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/rollup-config-validator)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and validator output in text, JSON, or summary format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes; strict mode can promote warnings to errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
