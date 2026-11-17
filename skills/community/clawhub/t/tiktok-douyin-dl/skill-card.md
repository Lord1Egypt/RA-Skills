## Description:

Provides guidance and shell commands for using Linux CLI tools to batch download no-watermark TikTok and Douyin videos and photo posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[francis-xavier-code](https://clawhub.ai/user/francis-xavier-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, update, and run douyin-dl and tiktok-dl workflows for TikTok and Douyin media downloads. It is most relevant when an agent needs to provide concise command-line usage, first-run setup notes, and risk-aware installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent third-party executables are installed or updated from release URLs without integrity verification.

Mitigation: Verify hashes or signatures where available, install in an isolated environment, and avoid running the binaries with elevated privileges.

Risk: Unpinned dependency installation and --break-system-packages can alter the host Python environment.

Mitigation: Use a virtual environment or container for browser setup and avoid --break-system-packages unless the host-level change has been reviewed.

Risk: Downloading platform media can create intellectual-property, terms-of-service, or legal exposure.

Mitigation: Use the tool only for content the user is authorized to download and retain the skill's disclaimer in user-facing guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/francis-xavier-code/skills/tiktok-douyin-dl)
- [Repository URL mentioned in artifact](https://github.com/Xynrin/tiktok-douyin-dl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is guidance for local Linux command execution and may include installation, update, and first-run browser setup steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
