## Description:

Start a local HTTP server to preview static HTML pages. Use when testing static pages, previewing HTML files, or when browser tools cannot access file:// URLs. Provides localhost URL for browser testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujintao-2021](https://clawhub.ai/user/liujintao-2021)

### License/Terms of Use:


## Use Case:

Developers and test automation agents use this skill to serve static HTML files or directories over localhost for browser preview and automated testing when file:// access is unsuitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The preview server listens on all network interfaces and may expose the selected file's parent directory or chosen directory to other machines that can reach the host and port.

Mitigation: Run it on trusted networks, serve a dedicated directory containing only preview files, and stop the server when testing is complete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces localhost preview URLs, served-directory information, and stop instructions for the running server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
