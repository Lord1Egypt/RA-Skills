## Description: <br>
Post or schedule content to X (Twitter) using the Publora API for tweets, scheduled tweets, and X/Twitter threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, social media operators, and agents use this skill to create or schedule X/Twitter posts through Publora, including single tweets, auto-split threads, explicit thread splits, and supported media attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Publora key can act on connected X/Twitter accounts and create or schedule posts. <br>
Mitigation: Confirm the target account, post text, media, and scheduled time before allowing any create-post request. <br>
Risk: X/Twitter API limits can cause failed or altered posts, especially for long videos, mixed media, thread media, emojis, and URLs. <br>
Mitigation: Check content against the documented Publora limits before posting: Pro or Premium access, 280-character standard tweets, 120-second videos, no mixed image/video posts, and media only on the first thread tweet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sergebulaev/publora-twitter) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript fetch examples and API parameter notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guidance for Publora create-post requests, X/Twitter platform IDs, character limits, media limits, and scheduling timestamps.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
