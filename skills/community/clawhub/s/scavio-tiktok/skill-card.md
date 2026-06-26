## Description: <br>
Look up TikTok profiles, search videos and users, explore hashtags, read comments, and traverse the social graph (followers/followings). Eleven endpoints, all at 1 credit per request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scavio-ai](https://clawhub.ai/user/scavio-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve TikTok profile, video, hashtag, comment, and follower/following data through the Scavio API for creator research, trend analysis, RAG enrichment, or content performance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Scavio API key and sends user-directed TikTok queries to a third-party service. <br>
Mitigation: Use a dedicated key with appropriate access, avoid exposing it in prompts or logs, and rotate it if it may have been shared. <br>
Risk: TikTok comments, profiles, and follower or following lists may contain personal or sensitive social graph data. <br>
Mitigation: Limit collection to necessary queries and pagination, and review privacy, consent, platform-policy, and retention requirements before reuse. <br>
Risk: Paginated calls consume credits and can expand collection scope quickly. <br>
Mitigation: Inform users before broad pagination, keep result counts narrow, and stop when the requested analysis has enough data. <br>


## Reference(s): <br>
- [Scavio TikTok API documentation](https://scavio.dev/docs/tiktok-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, code, text] <br>
**Output Format:** [Markdown with API endpoint guidance, JSON-oriented examples, and inline bash or Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; Scavio metadata sets a 90 second timeout and 1 request per second throttle.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
