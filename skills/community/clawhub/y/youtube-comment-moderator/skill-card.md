## Description:

AI-powered YouTube comment moderation that fetches comments, classifies them as spam, question, praise, hate, neutral, or constructive, drafts replies, and can delete spam through YouTube OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhruvkar](https://clawhub.ai/user/dhruvkar)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel operators use this skill to set up a YouTube comment moderation workflow that fetches recent comments, classifies them with Gemini, drafts replies, queues approvals, reports statistics, or performs configured reply and deletion actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto mode can delete comments and post replies based on LLM-generated classification and reply text.

Mitigation: Prefer monitor or approval mode, run dry runs first, and review the approval queue before enabling automatic replies or deletions.

Risk: OAuth tokens, callback URLs, API keys, config files, and the SQLite database can expose channel access or comment data if shared.

Mitigation: Keep token, config, database, and environment files private; do not paste full OAuth callback URLs into chat; restrict or rotate exposed keys.

Risk: The security verdict is suspicious because write operations are possible and safeguards around OAuth and stored tokens are limited.

Mitigation: Install only when YouTube comment write access is acceptable and avoid scheduled auto operation until local safeguards and review practices are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dhruvkar/skills/youtube-comment-moderator)
- [YouTube OAuth Setup Guide](references/oauth-setup.md)
- [Google AI Studio API Key](https://aistudio.google.com/apikey)
- [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce dry-run moderation reports, approval queues, reply drafts, statistics, and setup instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
