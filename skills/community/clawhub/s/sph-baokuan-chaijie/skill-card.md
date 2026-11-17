## Description:

视频号爆款拆解流水线 accepts one or more WeChat Channels share links, downloads the videos, extracts audio, transcribes speech with local Whisper, collects title/tag/interaction/account metadata, and helps generate a structured HTML report that analyzes viral content patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikogeyu-cell](https://clawhub.ai/user/mikogeyu-cell)

### License/Terms of Use:

MIT

## Use Case:

Content operators, marketers, and developers use this skill to process WeChat Channels video links, collect transcripts and engagement metadata, and produce repeatable analysis of viral title, tag, structure, and interaction patterns. It is intended for user-provided links and does not claim complete account crawling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a logged-in Yuanbao/browser session to process WeChat Channels links.

Mitigation: Install and run it only when that session use is acceptable, and confirm the required login state before processing links.

Risk: The workflow stores downloaded videos, extracted audio, transcripts, metadata, and HTML reports on local disk.

Mitigation: Use an appropriate output directory, process only content you are authorized to analyze, and delete local outputs when they are no longer needed.

Risk: WeChat Channels does not provide a public full-account video API, so discovered links may be incomplete.

Mitigation: Treat account-level conclusions as coverage-limited and supplement web-discovered links with links supplied by the user from WeChat.

## Reference(s):

- [视频号爆款拆解分析框架](references/analysis_framework.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Shell commands, Guidance]

**Output Format:** [JSON metadata, plain text transcripts, downloaded media files, and an HTML analysis report, with Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local outputs including result.json, videos/*.mp4, audio/*.wav, transcripts/*.txt, and 爆款拆解报告.html under the selected output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence, manifest.yaml, and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
