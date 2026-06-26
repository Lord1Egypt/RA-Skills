## Description: <br>
Adds mood-aware sticker images to casual or emotional conversations by selecting a keyword, fetching a third-party sticker API result, and returning one image with text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensanle](https://clawhub.ai/user/chensanle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to make assistants respond with one context-aware sticker plus text in casual, emotional, celebratory, greeting, apology, or encouragement exchanges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is broad and always on, so it may add sticker images proactively in casual or emotional conversations. <br>
Mitigation: Use it only where proactive stickers are acceptable, and opt out or disable it when image reactions are unwanted. <br>
Risk: The skill contacts a third-party sticker API with a selected keyword. <br>
Mitigation: Avoid using it in sensitive conversations, and disable it in environments where outbound third-party requests are not allowed. <br>
Risk: Sticker image content is returned by an external service. <br>
Mitigation: Review generated stickers in managed or commercial settings, and disable external media if unvetted images are unsuitable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chensanle/sticker) <br>
- [Sticker API endpoint](https://api.tangdouz.com/a/biaoq.php?return=json&nr=关键词) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Media, API Calls] <br>
**Output Format:** [Plain text with a MEDIA token for the selected sticker image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [At most one sticker per reply; retries once with a related keyword if the API returns no results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
