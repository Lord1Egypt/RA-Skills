## Description:

Publish posts and threads to Threads (by Meta). Use when the user says 'post to Threads', 'create a thread', 'publish thread', 'write a Threads post', 'reply on Threads', or wants to create text posts, photo/video posts, carousels, or multi-post threads on Threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to publish, schedule, and reply to Threads posts through a Boring MCP connector after connecting a Threads account. It supports text posts, media posts, carousels, multi-post threads, and replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded authentication token with social publishing authority.

Mitigation: Treat the URL as a password, avoid sharing it, and regenerate or revoke it if exposed.

Risk: The connected Boring account may have access to multiple social or brand accounts.

Mitigation: Connect only intended accounts and verify the target Threads account before each publish, reply, or schedule action.

Risk: Publishing or scheduling can create public content, upload media, or post replies on behalf of the connected account.

Mitigation: Review post text, media, scheduling time, and target post before invoking publish, thread, reply, upload, or schedule tools.

Risk: Local-file upload instructions may cause unintended files to be sent to the third-party service.

Mitigation: Upload only explicit media files selected for the Threads post.

## Reference(s):

- [Threads Publisher on ClawHub](https://clawhub.ai/snoopyrain/skills/threads-publisher)
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring Documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool call examples and publishing result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Threads post IDs, thread URLs, scheduling details, uploaded media references, or error summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
