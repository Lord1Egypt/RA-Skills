## Description: <br>
Create and publish Xiaohongshu (RED) notes through API posting, browser automation, or draft generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antaeus001](https://clawhub.ai/user/antaeus001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to prepare Xiaohongshu note content, create drafts, and publish through approved API credentials or personal-account browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser mode can expose logged-in page contents to an external analyzer model. <br>
Mitigation: Prefer API mode or draft mode where possible; if browser mode is required, use a local or trusted analyzer endpoint and avoid external model keys for sensitive sessions. <br>
Risk: Browser automation can publish automatically from a persistent Xiaohongshu account session. <br>
Mitigation: Use a dedicated account, review prepared content before publishing, and protect or delete the persistent browser profile when finished. <br>
Risk: Debug and step capture can retain screenshots or HTML from sensitive logged-in sessions. <br>
Mitigation: Avoid debug or step capture on sensitive accounts and delete captured files after review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antaeus001/xiaohongshu-post-antaeus) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/antaeus001) <br>
- [Xiaohongshu API setup guide](references/api-setup.md) <br>
- [Xiaohongshu Open Platform](https://open.xiaohongshu.com) <br>
- [Xiaohongshu Open Platform documentation](https://school.xiaohongshu.com/open) <br>
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text drafts, JSON command output, and shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports title, body, tags, and 1-9 JPG/PNG images; platform constraints include short titles, bounded body length, content review, and rate limits.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
