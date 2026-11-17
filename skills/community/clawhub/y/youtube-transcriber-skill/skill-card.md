## Description:

Automatically transcribes YouTube videos and produces timestamped transcripts and a structured summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bodysuperman](https://clawhub.ai/user/bodysuperman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to download YouTube audio, transcribe it with Whisper, and produce timestamped transcript text for review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command wrapper and installation examples can expose users to arbitrary-code-execution and supply-chain risk.

Mitigation: Review the package before installing, avoid the npx GitHub examples as written, and prefer a pinned, inspected release.

Risk: User-provided URL input is unsafe in the current command wrapper.

Mitigation: Use only trusted YouTube URLs and update the wrapper to spawn Python without a shell while validating exact YouTube hostnames.

Risk: Dependency installation executes package downloads during setup.

Mitigation: Inspect install scripts and dependency files before deployment, and pin dependency versions in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bodysuperman/skills/youtube-transcriber-skill)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text with Markdown-formatted transcript sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes progress messages, detected or selected language, and timestamped transcript segments.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
