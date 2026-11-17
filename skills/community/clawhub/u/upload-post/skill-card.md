## Description:

Publish and schedule content to 15 social platforms through one Upload-Post API call: TikTok, Instagram, YouTube, LinkedIn, Facebook, X, Threads, Pinterest, Bluesky, Reddit, Discord, Telegram, Mastodon, WordPress and Google Business Profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victorcavero14](https://clawhub.ai/user/victorcavero14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to have an agent draft Upload-Post API calls for publishing, scheduling, status checks, analytics, and post management across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live publish, edit, and cancel authority over connected social accounts.

Mitigation: Require the agent to show the exact profile, target platforms, content, schedule time, and job_id before any publish, retry, edit, or cancel action.

Risk: The Upload-Post API key can publish to connected accounts if exposed or misused.

Mitigation: Store UPLOAD_POST_API_KEY only in the skill-specific environment, limit who can invoke the skill, and rotate or revoke the key if exposure is suspected.

Risk: Unpinned npx installation can pull a changed package in sensitive environments.

Mitigation: Use a reviewed and pinned release artifact or installation path when deploying in sensitive environments.

Risk: Retries can duplicate posts or amplify a partial failure if per-platform results are not inspected.

Mitigation: Read per-platform status results, retry only failed platforms, and use an Idempotency-Key for retried publish requests.

## Reference(s):

- [Upload-Post API documentation](https://docs.upload-post.com)
- [Upload-Post LLM-friendly API documentation](https://docs.upload-post.com/llm.txt)
- [Upload-Post dashboard and API keys](https://upload-post.com)
- [Platform-specific parameters](references/platforms.md)
- [Media format requirements](references/requirements.md)
- [Upload-Post MCP connector](https://mcp.upload-post.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and UPLOAD_POST_API_KEY; may also use UPLOAD_POST_PROFILE.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
