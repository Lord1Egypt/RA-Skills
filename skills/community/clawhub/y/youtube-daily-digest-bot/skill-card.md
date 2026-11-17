## Description:

A Python bot that monitors YouTube channels via RSS, summarizes new videos using Google Gemini AI with transcript extraction or audio fallback, and sends bilingual Chinese and English summaries to a Telegram chat daily.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inkiy](https://clawhub.ai/user/inkiy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation operators use this skill to monitor selected YouTube channels, summarize newly published videos with Gemini, and deliver bilingual daily digests to Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens may be exposed through logs or deployment practices.

Mitigation: Run the bot in an isolated non-privileged environment and redact Telegram tokens from all logs.

Risk: Downloaded audio fallback files may remain on disk after processing.

Mitigation: Delete local audio files after summarization and constrain temporary storage permissions.

Risk: Video transcripts or audio can influence generated summaries.

Mitigation: Treat generated summaries as untrusted, review important outputs, and avoid allowing summary text to trigger privileged actions.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Pin dependencies before installation and review updates before deployment.

Risk: Network calls to YouTube, Gemini, and Telegram can hang or fail.

Mitigation: Add request timeouts, retry boundaries, and operational monitoring for long-running deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inkiy/skills/youtube-daily-digest-bot)
- [Publisher profile](https://clawhub.ai/user/inkiy)
- [YouTube RSS feed endpoint](https://www.youtube.com/feeds/videos.xml?channel_id={channel_id})
- [YouTube channel ID helper](https://commentpicker.com/youtube-channel-id.php)

## Skill Output:

**Output Type(s):** [Markdown, Text, Configuration, Shell commands]

**Output Format:** [Markdown summaries and setup guidance for a Python Telegram bot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bilingual Chinese and English digest messages; long Telegram messages are chunked before delivery.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
