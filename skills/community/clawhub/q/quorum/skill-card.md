## Description:

Multi-agent validation framework where independent AI critics evaluate artifacts against rubrics with evidence-grounded findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dacervera](https://clawhub.ai/user/dacervera)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Quorum to validate AI-generated research, configuration, code, and multi-file project artifacts against domain rubrics. It produces grounded findings, verdicts, and remediation guidance before shipping or relying on agent output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed artifacts may be transmitted to configured external model providers.

Mitigation: Do not run the skill on secrets, customer data, or proprietary code unless the configured provider and data policy are approved.

Risk: Installation uses mutable source and dependency resolution paths.

Mitigation: Install in an isolated environment from a reviewed commit and pin dependencies for controlled deployments.

Risk: Persistent local learning memory can influence future reviews.

Mitigation: Use --no-learning or remove project-local known_issues.json when auditing untrusted repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dacervera/skills/quorum)
- [OpenClaw metadata source](https://github.com/SharedIntellect/quorum)
- [Quorum specification](https://github.com/SharedIntellect/quorum/blob/main/SPEC.md)
- [Model requirements](https://github.com/SharedIntellect/quorum/blob/main/docs/getting-started/MODEL_REQUIREMENTS.md)
- [Configuration reference](https://github.com/SharedIntellect/quorum/blob/main/docs/configuration/CONFIG_REFERENCE.md)
- [Beginner guide](https://github.com/SharedIntellect/quorum/blob/main/docs/getting-started/FOR_BEGINNERS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured validation outputs such as JSON verdicts and reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Run outputs include per-critic findings, prescreen results, verdict JSON, and a human-readable report.]

## Skill Version(s):

0.7.3 (source: release evidence, changelog, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
