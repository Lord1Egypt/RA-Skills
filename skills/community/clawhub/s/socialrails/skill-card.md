## Description: <br>
Manage social media by scheduling posts, viewing analytics, generating AI captions, and listing connected accounts via the SocialRails API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BuildsbyMatt](https://clawhub.ai/user/BuildsbyMatt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and social media operators use this skill to manage SocialRails-connected accounts from an agent, including scheduling posts, reviewing analytics, generating captions, and listing posts or accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect connected social media accounts by scheduling or drafting content through the SocialRails API. <br>
Mitigation: Review generated or scheduled content before write actions and use least-privilege API scopes for the intended commands. <br>
Risk: A misconfigured API base URL could send requests to an unintended endpoint. <br>
Mitigation: Keep the API base URL set to the intended SocialRails endpoint and verify configuration before deployment. <br>


## Reference(s): <br>
- [SocialRails ClawHub listing](https://clawhub.ai/BuildsbyMatt/socialrails) <br>
- [SocialRails API Documentation](https://socialrails.com/documentation/api-overview) <br>
- [SocialRails OpenClaw Setup Guide](https://socialrails.com/documentation/openclaw-setup) <br>
- [SocialRails Dashboard](https://socialrails.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and structured command results from SocialRails API operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return scheduled post identifiers, analytics summaries, generated caption text, post listings, connected account listings, or API error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact skill.json, artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
