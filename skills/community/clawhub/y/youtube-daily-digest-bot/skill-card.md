## Description: <br>
A Python bot that monitors configured YouTube channels through RSS, summarizes new videos with Google Gemini using transcripts or audio fallback, and sends bilingual Chinese and English summaries to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Inkiy](https://clawhub.ai/user/Inkiy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a daily YouTube monitoring workflow that detects new videos from selected channels, summarizes their content, and posts digest messages to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored video transcripts or downloaded audio are sent to Google Gemini for summarization. <br>
Mitigation: Install only when this external processing is acceptable for the selected channels, and avoid monitoring sensitive or private content. <br>
Risk: Generated summaries are posted to the configured Telegram chat. <br>
Mitigation: Restrict the bot token and chat ID to intended destinations and review channel configuration before long-running use. <br>
Risk: The bot depends on API tokens and third-party Python packages for network operations. <br>
Mitigation: Provide secrets through environment variables, keep them out of source files, and pin dependency versions before production deployment. <br>
Risk: Audio fallback can leave downloaded media on local disk. <br>
Mitigation: Periodically clear temporary audio files when retention is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Inkiy/youtube-daily-digest-bot) <br>
- [YouTube channel ID helper referenced by the skill](https://commentpicker.com/youtube-channel-id.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration] <br>
**Output Format:** [Telegram Markdown messages, log text, and local JSON state for processed video IDs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are chunked for Telegram message length limits and include bilingual Chinese and English sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
