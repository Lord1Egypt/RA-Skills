## Description:

Video Proof records Playwright-driven proof artifacts after coding tasks, including UI recordings, screenshots, console logs, API results, and Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rikisann](https://clawhub.ai/user/rikisann)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and coding agents use this skill after implementation work to create visual or API proof that a feature works and to attach the resulting artifacts to a task or pull request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node packages, Playwright browser dependencies, and ffmpeg through local package managers or sudo-capable commands.

Mitigation: Review setup scripts before installation, prefer manual dependency installation when possible, and run setup in a development or disposable environment.

Risk: Proof specs and CLI options can start arbitrary local commands to launch an application before recording.

Mitigation: Use only trusted proof specs and start commands, and avoid running the skill against production systems or sensitive authenticated pages.

Risk: Generated videos, screenshots, console logs, Markdown summaries, and API results may capture sensitive data.

Mitigation: Inspect and redact generated artifacts before committing, sharing, or attaching them to a pull request.

## Reference(s):

- [Proof Spec Reference](artifact/references/proof-spec.md)
- [ClawHub Skill Page](https://clawhub.ai/rikisann/skills/video-proof-skill)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with YAML proof specs, shell commands, and generated proof artifacts such as WebM or MP4 video, PNG screenshots, logs, and JSON API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local proof-artifacts with pass/fail summaries and may return a nonzero exit code when proof steps fail.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
