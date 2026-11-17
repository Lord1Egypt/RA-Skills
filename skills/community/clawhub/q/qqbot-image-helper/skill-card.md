## Description:

Helps agents copy locally downloaded QQBot images from a tool-restricted directory into an allowed media directory so the image tool can analyze them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hahh9527](https://clawhub.ai/user/hahh9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a locally downloaded QQBot image is outside the image tool's allowed directories and must be copied to an approved media path before analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies images from a tool-restricted QQBot download directory into an allowed media directory, bypassing a local access boundary.

Mitigation: Install only when this behavior is acceptable, prefer a platform-approved attachment import path, and authorize each file explicitly before copying.

Risk: Copied private images can remain in ~/.openclaw/media after analysis.

Mitigation: Use unique temporary filenames and delete copied images immediately after processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hahh9527/skills/qqbot-image-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local file paths under ~/.openclaw/qqbot/downloads and ~/.openclaw/media.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
