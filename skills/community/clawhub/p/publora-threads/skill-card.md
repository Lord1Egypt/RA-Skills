## Description:

Post or schedule content to Threads using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social media operators use this skill to have an agent draft API calls and guidance for publishing or scheduling Threads posts through Publora, including media upload and reply-control settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Publora API key could be exposed or reused outside the intended workspace.

Mitigation: Treat the Publora API key as sensitive, keep it out of shared transcripts and committed files, and rotate it if exposure is suspected.

Risk: The agent could prepare a post for the wrong Threads account, content, media, or scheduled time.

Mitigation: Confirm the target platform ID, post text, media attachments, reply-control setting, and scheduled timestamp before allowing publication.

Risk: Nested Threads posts are temporarily unavailable, so long content may not publish as an expected reply chain.

Mitigation: Keep posts under the single-post limit or wait for Publora support to confirm nested threading has been restored.

## Reference(s):

- [Publora API Base URL](https://api.publora.com/api/v1)
- [Publora Create Post Endpoint](https://api.publora.com/api/v1/create-post)
- [Publora Upload URL Endpoint](https://api.publora.com/api/v1/get-upload-url)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript fetch examples and concise platform guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Publora API endpoints, API-key header usage, Threads platform IDs, scheduling fields, media upload flow, reply-control settings, platform limits, and temporary nested-thread restrictions.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
