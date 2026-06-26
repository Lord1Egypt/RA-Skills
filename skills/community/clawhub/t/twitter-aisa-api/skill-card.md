## Description: <br>
Search and read Twitter/X profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish user-approved posts with OAuth and media attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to research Twitter/X content, inspect accounts and trends, and publish explicit user-approved posts, replies, quotes, images, or videos through an OAuth workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorization and posting commands can print the raw AISA API key into normal output. <br>
Mitigation: Treat command output and logs as sensitive, avoid sharing them, and rotate the AISA API key if it is exposed. <br>
Risk: The skill can post externally to Twitter/X and upload approved local media files through the AISA relay. <br>
Mitigation: Review the exact post text, authorized account, reply or quote target, and attachments before allowing publication. <br>
Risk: Using the skill requires trusting the AISA relay with OAuth flow data, post content, media files, and the AISA API key. <br>
Mitigation: Install and run it only where that relay trust model and data exposure are acceptable. <br>


## Reference(s): <br>
- [Post Twitter workflow](references/post_twitter.md) <br>
- [ClawHub release page](https://clawhub.ai/bibaofeng/twitter-aisa-api) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and may return authorization links, Twitter/X account status, tweet IDs, tweet links, search results, or relay error messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
