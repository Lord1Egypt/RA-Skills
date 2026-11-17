## Description:

Sends images, videos, audio, and documents to WhatsApp by downloading media, copying it into the OpenClaw workspace, sending it with the WhatsApp message tool, and cleaning up temporary files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekeyl](https://clawhub.ai/user/seekeyl)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill when an agent needs to send a local or downloaded media file to a WhatsApp recipient, including images, screenshots, videos, audio, and documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell-command templates may handle user-controlled URLs, filenames, recipients, captions, and paths.

Mitigation: Use structured APIs or safely escaped argument arrays, validate URLs and recipients, and confirm the recipient, file, and caption before sending.

Risk: Temporary and workspace media copies may expose sent files longer than intended.

Mitigation: Generate private temporary filenames and explicitly confirm retention or cleanup expectations for both temporary and workspace copies.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WhatsApp recipient, source file or URL, optional caption, and workspace-accessible media path.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
