## Description:

Optimizes SRT subtitle files by removing filler words, correcting ASR transcription errors, preserving timestamps, and sending the refined file with token usage details through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truetechlabs](https://clawhub.ai/user/truetechlabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to clean SRT subtitles for videos by removing spoken filler words, correcting common ASR mistakes, and preserving subtitle numbering and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and subtitle contents may be exposed through verbose request, response, and payload logging.

Mitigation: Remove raw token and payload logging before use, avoid pasting real API keys into chat, and review logs for subtitle or credential leakage.

Risk: Subtitle content is processed by SiliconFlow and the optimized file is automatically delivered through Feishu.

Mitigation: Do not use confidential subtitles unless those external transfers are acceptable; add explicit user confirmation before external processing and Feishu delivery.

Risk: The exact data sent to external services is not fully documented in the release evidence.

Mitigation: Document the data sent to SiliconFlow and Feishu, including subtitle text, prompts, output files, and token usage details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/truetechlabs/skills/subtitle-refiner)
- [Source repository referenced by artifact](https://gitee.com/real__cool/subtitle_refiner)
- [SiliconFlow chat completions endpoint](https://api.siliconflow.cn/v1/chat/completions)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [SRT file with a text processing summary and token usage details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an optimized subtitle file under the workspace subtitle_refine directory and can send the file through Feishu.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
