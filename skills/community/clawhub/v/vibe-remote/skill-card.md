## Description:

Vibe Remote helps agents guide users through installing, running, configuring, and filing GitHub issues for the Vibe Remote remote AI coding tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firetable](https://clawhub.ai/user/firetable)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to help operate Vibe Remote, connect an iOS app to a Mac or Linux coding environment, or prepare GitHub bug and feature reports for the project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Headless usage examples include account and password values directly in a shell command.

Mitigation: Use a secret manager, environment variables, or an interactive prompt instead of placing real passwords in commands, scripts, shell history, or CI logs.

Risk: Issue media may be uploaded to a third-party file host.

Mitigation: Inspect the exact file before upload, remove secrets and metadata, and confirm the user accepts sending the media to the third-party host.

## Reference(s):

- [Vibe Remote documentation](https://docs.vibe-remote.com)
- [Vibe Remote GitHub repository](https://github.com/ymzuiku/vibe-remote)
- [Catbox upload endpoint](https://catbox.moe/user/api.php)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline bash commands and issue templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub issue body text and media upload links when the user requests issue submission support.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
