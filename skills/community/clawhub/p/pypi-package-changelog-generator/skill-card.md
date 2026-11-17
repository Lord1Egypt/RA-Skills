## Description:

Analyzes changes between PyPI package versions and generates structured changelog evidence for upgrade notes, release notes, dependency changes, compatibility risks, and breaking changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[annangela](https://clawhub.ai/user/annangela)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to compare PyPI package versions or version ranges and produce upgrade-focused changelog evidence, including release notes, dependency changes, compatibility risks, and breaking-change signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to PyPI and GitHub.

Mitigation: Install and run it only in environments where those outbound requests are acceptable.

Risk: The skill can process source archives from requested PyPI packages, including untrusted or unusually large packages.

Mitigation: Run it with normal agent time, memory, and temporary-storage limits.

Risk: The artifact includes a plaintext GitHub token configuration example.

Mitigation: Prefer no GitHub token, or inject a short-lived read-only token through environment or apiKey configuration instead of storing direct plaintext token values.

## Reference(s):

- [Project homepage](https://github.com/AnnAngela/pypi-package-changelog-generator)
- [Output schema](references/output-schema.md)
- [Failure modes](references/failure-modes.md)
- [OpenClaw config](references/openclaw-config.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON evidence and concise Markdown summary sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report truncation, archive fallback, weak evidence, warnings, or errors when those conditions appear in the JSON result.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
