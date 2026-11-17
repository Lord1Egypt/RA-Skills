## Description:

SparkyFitness CLI for food diary, exercise tracking, biometric check-ins, and health summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronjanosch](https://clawhub.ai/user/aronjanosch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a separately installed sparky CLI against a self-hosted SparkyFitness server for food, exercise, biometric, mood, summary, and trend workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unverified third-party CLI executable and a separate SparkyFitness server.

Mitigation: Install only from trusted, pinned, and verified releases, and prefer a user-owned bin directory.

Risk: The workflow handles sensitive health data and API keys with limited privacy guidance in the artifact.

Mitigation: Use HTTPS, understand where the API key is stored, and avoid entering sensitive health data unless the server and CLI source are trusted.

Risk: Food and exercise searches can use external lookup providers and may return ambiguous results.

Mitigation: Prefer barcode or UUID-based logging, inspect brand and macro data before logging, and use explicit IDs in scripts.

## Reference(s):

- [SparkyFitness](https://github.com/CodeWithCJ/SparkyFitness)
- [sparky-cli](https://github.com/aronjanosch/sparky-cli)
- [sparky-cli releases](https://github.com/aronjanosch/sparky-cli/releases)
- [ClawHub skill page](https://clawhub.ai/aronjanosch/skills/sparky)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI command examples and JSON-mode workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a separately installed sparky executable and a reachable SparkyFitness server.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
