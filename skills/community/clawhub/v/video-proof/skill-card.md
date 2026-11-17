## Description:

Records video and API proof artifacts for completed coding tasks, including screen recordings, screenshots, console logs, API results, and Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rikisann](https://clawhub.ai/user/rikisann)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and coding agents use this skill after implementation to run scripted UI or API proofs and attach evidence artifacts to pull requests or task deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proof specs can start applications using shell commands.

Mitigation: Run the skill in a disposable or project-limited environment and review every proof spec before execution.

Risk: Untrusted PR-provided specs may trigger unsafe local actions.

Mitigation: Do not run specs supplied by untrusted contributors until they have been reviewed and reduced to the expected proof steps.

Risk: Generated screenshots, videos, console logs, and API results may contain sensitive information.

Mitigation: Inspect and redact proof artifacts before committing, publishing, or sharing them.

Risk: The setup script can install mutable dependencies and request elevated system package installation.

Mitigation: Review setup.sh before running it and prefer controlled environments where dependency installation and sudo use are acceptable.

## Reference(s):

- [Proof Spec Reference](references/proof-spec.md)
- [ClawHub Skill Page](https://clawhub.ai/rikisann/skills/video-proof)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown reports, JSON API results, WebM or MP4 recordings, PNG screenshots, console logs, YAML proof specs, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pass/fail summaries and exits nonzero when proof steps or API requests fail.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
