## Description:

SparkyFitness CLI for food diary, exercise tracking, biometric check-ins, and health summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronjanosch](https://clawhub.ai/user/aronjanosch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate the sparky CLI against a self-hosted SparkyFitness server for logging food, exercise, weight, steps, mood, and reviewing health summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned third-party CLI that may be installed into a system path.

Mitigation: Use trusted release sources, prefer pinned releases with checksum or signature verification, and install into a user-local bin directory when possible.

Risk: The CLI handles API keys, health notes, biometrics, and other sensitive personal data.

Mitigation: Use HTTPS for the SparkyFitness server, protect the API key, and treat logged health data as sensitive.

Risk: Food and exercise search results can be ambiguous or imported from external providers.

Mitigation: Prefer barcode or ID-based logging, verify brands and macros before logging, and remove incorrect imported products from the local library.

## Reference(s):

- [SparkyFitness ClawHub page](https://clawhub.ai/aronjanosch/skills/sparkyfitness)
- [SparkyFitness application repository](https://github.com/CodeWithCJ/SparkyFitness)
- [sparky CLI repository](https://github.com/aronjanosch/sparky-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-mode sparky commands when structured CLI output is useful.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
