## Description: <br>
Search Reddit posts or fetch a full post with threaded comments by URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavio-ai](https://clawhub.ai/user/scavio-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent builders use this skill to search Reddit discussions, retrieve full Reddit posts with comments, and gather community context for research, monitoring, sentiment analysis, or RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit search terms and post URLs are sent to Scavio using the configured API key. <br>
Mitigation: Avoid sending secrets, private customer details, or sensitive business strategy unless the organization has approved Scavio for that use. <br>
Risk: The skill depends on a sensitive API credential. <br>
Mitigation: Store SCAVIO_API_KEY in the agent runtime environment and avoid logging or embedding it in prompts, code examples, or shared files. <br>
Risk: Reddit content is user-generated and may be incomplete, misleading, stale, or sensitive. <br>
Mitigation: Preserve author attribution and metadata, surface NSFW flags, and do not fabricate titles, authors, scores, or comment content. <br>


## Reference(s): <br>
- [Scavio Reddit API documentation](https://scavio.dev/docs/reddit-api) <br>
- [Scavio homepage](https://scavio.dev) <br>
- [ClawHub skill page](https://clawhub.ai/scavio-ai/scavio-reddit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples and shell configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; Reddit requests may take 5-15 seconds and consume Scavio credits.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
