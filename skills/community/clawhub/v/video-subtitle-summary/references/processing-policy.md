---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '5ccc1d0c-dbe9-4be8-8d7b-209b64fe0fdf'
  PropagateID: '5ccc1d0c-dbe9-4be8-8d7b-209b64fe0fdf'
  ReservedCode1: '627fc8c8-212b-48f4-b834-c8a062271e35'
  ReservedCode2: '627fc8c8-212b-48f4-b834-c8a062271e35'
---

# Processing Policy

## 安全与访问规则

所有在线学习平台（包括智学云 zhixueyun.com）均为公开互联网网站。需要登录时仅视为普通网站用户认证，不存储任何凭据，不绕过任何登录限制。本技能的 Playwright 自动化仅以非 headless 模式启动浏览器，由用户手动完成登录后提取字幕。

## Allowed Assistance

- Summarize videos using only exposed subtitles or transcripts.
- Extract or use subtitles exposed by the page or supplied by the user.
- Use browser-visible transcript panels as context.
- Generate learning notes, review outlines, concept explanations, self-study checklists, and self-test questions from already available subtitle/transcript material.
- Export the Markdown report to docx/pdf/html upon user request.

## Disallowed Assistance

- Perform any form of audio extraction, audio transcription (ASR), speech-to-text, or real-time playback capture. This skill is subtitle-only; if subtitles are not available, stop and inform the user.
- Bypass DRM, paywalls, login restrictions, completion gates, or anti-download protections.
- Request, store, reuse, or expose any form of authentication material, login artifacts, or secrets.
- Answer live quizzes, exams, certification tests, compliance assessments, graded questions, or assessment prompts.
- Automate course completion, attendance, watch progress, check-ins, playback progress, participation signals, or progress farming.
- Help misrepresent user participation, identity, progress, completion status, or assessment results.

## Refusal for Prohibited Assessment or Completion Requests

```text
我不能帮助代答考试、测验或认证题，也不能绕过平台的学习或考核机制。我可以帮你整理课程知识点、生成复习提纲、解释概念，或根据已学习内容制作自测题。
```

## Refusal for Audio Transcription Requests

```text
本技能仅处理可提取字幕的视频内容，不进行音频转写。如果该视频源未暴露字幕，建议你提供 SRT/VTT 字幕文件，或换用有字幕的视频源，或让我读取浏览器中可见的 transcript 面板。
```