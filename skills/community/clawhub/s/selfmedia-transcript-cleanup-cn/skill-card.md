## Description:

接收用户拥有或获授权的中文原始转录文字、可选说话人和时间标记及清稿尺度，交付忠实原意的干净稿、逐项修改清单与待确认标记，适用于访谈、口述和视频字幕初稿；缺少文本或说话人无法区分时先请求补充，绝不凭空补词或校正专名数字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

内容创作者、编辑与制作团队可用它整理已获授权的中文访谈、口述或视频字幕转录稿。它保留原意、说话人和时间标记，并交付干净稿、修改清单及待确认项。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installation command leaves the installer version and repository revision unpinned.

Mitigation: Pin the installer version and repository revision before installation, following the security guidance.

Risk: Transcript names, numbers, and unclear passages may remain uncertain without audio evidence.

Mitigation: Process only transcripts you own or are authorized to use, then review edits and uncertainty markers; retain or flag details that cannot be verified.

## Reference(s):

- [Skill instructions](SKILL.md)
- [Successful cleanup example](fixtures/success.md)
- [Insufficient evidence example](fixtures/failure.md)
- [OpenAI Whisper project (usage context cited by README)](https://github.com/openai/whisper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a clean transcript, itemized edit log, and confirmation items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves supplied speaker and timestamp markers; uncertain passages are flagged rather than guessed.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
