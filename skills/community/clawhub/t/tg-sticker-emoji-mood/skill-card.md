## Description: <br>
Automatically send Telegram stickers and emojis that match the mood and vibe of the conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandysuper](https://clawhub.ai/user/dandysuper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to make Telegram conversations more expressive by letting an agent choose mood-matched stickers and emojis during chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can autonomously post Telegram stickers on the user's behalf. <br>
Mitigation: Enable it only for expected Telegram chats, test in a private chat first, and honor user opt-out requests immediately. <br>
Risk: The helper script has a confirmed code-injection weakness in the sticker-set plus emoji path. <br>
Mitigation: Fix emoji argument handling before enabling that path, or send only known sticker file IDs until the script is corrected. <br>
Risk: A Telegram bot token can grant posting access beyond the intended conversation. <br>
Mitigation: Use a dedicated low-privilege bot token and avoid deploying it in formal or group chats unless participants expect automated stickers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandysuper/tg-sticker-emoji-mood) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dandysuper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Conversational text with emojis and bash commands that call the Telegram Bot API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and Telegram chat context.] <br>

## Skill Version(s): <br>
3.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
