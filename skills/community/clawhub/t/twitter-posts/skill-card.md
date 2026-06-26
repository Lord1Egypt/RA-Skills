## Description: <br>
Draft, publish, and manage posts on X (Twitter), inspect timelines, manage profiles, and automate social media workflows via the X API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an X account through ClawLink, inspect X data, draft social content, and perform account actions such as posting, deleting, following, liking, bookmarking, direct messaging, and uploading media after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved write actions can change public content or account state on X. <br>
Mitigation: Review previews carefully and execute posts, deletes, follows, likes, bookmarks, direct messages, and media uploads only after explicit approval. <br>
Risk: The skill requires connecting an X account through ClawLink OAuth. <br>
Mitigation: Install only when comfortable granting the requested X account access, and use the connected account scope shown during the ClawLink flow. <br>
Risk: Tweet deletion is irreversible and media or posting requests can fail because of X API limits, permissions, or file constraints. <br>
Mitigation: Confirm destructive actions before execution, preserve important content outside the skill, and follow backoff or correction guidance when X rejects a request. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hith3sh/twitter-posts) <br>
- [X API Documentation](https://developer.x.com/en/docs) <br>
- [X API Reference](https://developer.x.com/en/docs/api-reference) <br>
- [ClawLink](https://claw-link.dev) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink tool calls for X account reads and confirmed write actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
