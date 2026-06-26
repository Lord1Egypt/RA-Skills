## Description: <br>
Provides agent-accessible Z-Sight app functions for live streams, trending topics, variety and short-video browsing, app navigation, content publishing, messages, user content lists, and article deletion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[295522894](https://clawhub.ai/user/295522894) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users with a configured Z-Sight authorization token use this skill to search and browse Z-Sight live, variety, short-video, and trending content, open app links, publish posts or short videos, inspect messages and user content, and delete selected articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that authorized account actions use an unencrypted raw IP endpoint that conflicts with the HTTPS documentation. <br>
Mitigation: Review carefully before installing; do not authorize with a real account token until the publisher moves MCP and authorization endpoints to a verified HTTPS domain and documents token scope and revocation. <br>
Risk: Authorized actions can publish posts or short videos and delete user articles. <br>
Mitigation: Require explicit user confirmation before publishing or deleting, and verify article IDs from the user's own content lists before any deletion. <br>
Risk: Bearer tokens enable account-scoped actions and may expose messages or user content if mishandled. <br>
Mitigation: Keep tokens out of prompts, logs, and shared files; configure them only in trusted clients and rotate or revoke them after expiry or suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/295522894/zmg-zsj-skill) <br>
- [Z-Sight authorization page](https://zmg-mcp.cztv.com) <br>
- [Live response examples](artifact/references/live.json) <br>
- [Search response examples](artifact/references/search.json) <br>
- [Short-video response examples](artifact/references/short_video.json) <br>
- [Variety response examples](artifact/references/variety.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, MCP tool parameters, result summaries, and links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bearer-token authorization for publishing, messages, user content, and deletion actions; browsing and search actions may return ranked lists and URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
