## Description: <br>
AI-powered YouTube comment moderation that fetches comments, classifies them as spam, question, praise, hate, neutral, or constructive, drafts replies, and can delete spam through YouTube OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhruvkar](https://clawhub.ai/user/dhruvkar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
YouTube creators and channel operators use this skill to guide setup and operation of an AI-assisted moderation pipeline that reads comments, classifies them, drafts replies, and optionally applies reply or deletion actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post replies and reject comments on a YouTube channel when OAuth write access is granted. <br>
Mitigation: Begin in monitor or dry-run mode, use approval mode for human review, and enable full auto only after the channel owner has reviewed representative results. <br>
Risk: OAuth tokens, API keys, local configuration, and the SQLite database may expose channel access or moderation history if mishandled. <br>
Mitigation: Protect .env, oauth.json, config.json, and the database with appropriate file permissions, avoid sharing full OAuth callback URLs, and delete local credentials or data when no longer needed. <br>
Risk: Automated classification and reply drafting may misclassify comments or generate unsuitable replies. <br>
Mitigation: Review the approval queue and sample moderation reports before approving deletions, posting replies, or scheduling recurring runs. <br>


## Reference(s): <br>
- [YouTube OAuth Setup Guide](references/oauth-setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dhruvkar/youtube-comment-moderator) <br>
- [Google Cloud Credentials](https://console.cloud.google.com/apis/credentials) <br>
- [Google AI Studio API Keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce moderation reports, approval queues, reply drafts, and local configuration or SQLite-backed state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
