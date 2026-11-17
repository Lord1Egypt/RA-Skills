## Description:

Guides an agent to use the Vox CLI to transcribe one explicitly specified media URL or local audio/video file, and to handle explicitly requested Vox setup and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casatwy](https://clawhub.ai/user/casatwy)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to transcribe one user-specified media link or exact local audio/video file with Vox. It also guides explicitly requested CLI installation, authentication, status checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI or using Vox authentication can expose the user to an untrusted package or credential-handling workflow.

Mitigation: Confirm trust in the Vox CLI and npm package before installing; request authorization for installation and login, and keep API keys out of commands and chat.

Risk: Transcribing private media can send content outside the local environment.

Mitigation: Use only the exact media URL or file the user authorizes and confirm sensitive content fits their Vox account and data expectations.

## Reference(s):

- [Vox skill on ClawHub](https://clawhub.ai/casatwy/skills/vox)
- [Vox API keys](https://vox.reka.cc/me/api-keys)

## Skill Output:

**Output Type(s):** [Text, Subtitles, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, SRT, VTT, JSON, or JSONL transcript; concise status or setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One explicitly specified input at a time; output remains on stdout unless the user requests a file.]

## Skill Version(s):

1.0.13 (source: ClawHub release and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
