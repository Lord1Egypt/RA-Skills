## Description:

Smart image loader that handles both URLs and local files, automatically downloads URLs to temporary locations, and displays images using the read tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tingwei1123](https://clawhub.ai/user/tingwei1123)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to resolve an image URL or workspace file path into a local file path suitable for display. It is useful when an agent needs to fetch a remote image, verify a local image path, and return display-oriented status information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads images from user-provided URLs, which can expose agents to untrusted remote content.

Mitigation: Use only trusted image URLs, validate content type and file size before display, and review the downloaded file before using it in downstream workflows.

Risk: The skill accepts local paths without documented workspace confinement.

Mitigation: Restrict local image paths to the active workspace and reject paths that resolve outside approved directories.

Risk: The artifact documentation recommends shell-based cleanup with `rm <file_path>`.

Mitigation: Perform cleanup through a safe non-shell file API and avoid interpolating user-controlled paths into shell commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text status output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script reports success status, input type, local file path, message, and whether cleanup is needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
