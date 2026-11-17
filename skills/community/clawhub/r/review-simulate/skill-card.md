## Description:

进行中文求职语音模拟面试。适用于用户想围绕目标岗位进行多轮中文面试练习，并通过 ASR 识别回答、由 LLM 决定追问或换题、由 TTS 播报面试官问题，最终输出结构化评估报告、改进建议和示例优化回答的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cows21](https://clawhub.ai/user/cows21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a Chinese job-interview practice session for a target role, with ASR-based answer capture, LLM-guided follow-up questions, optional TTS playback, and a structured final feedback report. It is intended for practice feedback rather than real hiring decisions or candidate ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interview audio, transcripts, prompts, and summaries may be sent to configured LLM, ASR, and TTS cloud providers.

Mitigation: Use the skill only when this data sharing is acceptable, avoid sensitive personal details in practice answers, and configure providers according to the user's privacy requirements.

Risk: The skill saves final reports and optional generated audio locally, which may contain personal interview practice content.

Mitigation: Use private output locations and delete saved reports or audio after use when retention is not needed.

Risk: TTS adds an additional cloud-service call and local audio output.

Mitigation: Run with --no-tts when voice playback is unnecessary.

Risk: Dependencies are declared with minimum versions, which can allow unreviewed newer package versions during installation.

Mitigation: Prefer pinned dependency versions in controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cows21/skills/review-simulate)
- [Prompt templates reference](artifact/references/prompts_cn.md)
- [State schema reference](artifact/references/state_schema_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus JSON interview state and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces interview questions, ASR transcripts, per-round scores, decisions, optional MP3 TTS audio, and a final_report.json output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
