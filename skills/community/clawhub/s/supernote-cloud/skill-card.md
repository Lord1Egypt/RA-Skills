## Description:

Access a self-hosted Supernote Private Cloud instance to browse files and folders, upload documents (PDF, EPUB) and notes, convert web articles to EPUB/PDF and send them to the device, check storage capacity, and navigate the directory tree.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickian](https://clawhub.ai/user/nickian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage files on a self-hosted Supernote Private Cloud instance, upload documents or notes, and convert web articles into e-reader-friendly EPUB or PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Supernote account credentials and caches an access token while interacting with a self-hosted cloud endpoint.

Mitigation: Use a trusted HTTPS endpoint, avoid elevated privileges, and review token handling before uploading sensitive content.

Risk: Article conversion fetches user-provided web URLs from the agent host and may process third-party page content and images.

Mitigation: Treat article conversion as network access, avoid private or sensitive URLs until the security issues are addressed, and review generated files before upload.

Risk: The Supernote API is described as reverse-engineered and unofficial, so endpoint behavior may change without notice.

Mitigation: Validate commands against the target Supernote Private Cloud instance before routine use and review failures before retrying uploads.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local EPUB, PDF, or HTML files before upload when converting web articles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
