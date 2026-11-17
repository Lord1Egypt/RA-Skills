## Description:

英语学习材料生成器：从课文中提取单词、生成音频、创建互动学习页面（课文学习+单词测验+原文理解+句子测验）。Use when user asks to create English learning materials, vocabulary exercises, or 英语学习资料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

English learners and teachers use this skill to turn an English lesson into vocabulary materials, speech audio, a lesson page, and interactive vocabulary, reading-comprehension, and sentence quizzes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted quiz content can run unwanted browser code when a generated page is opened.

Mitigation: Have the quiz generators fixed to handle text safely before using untrusted lessons or sharing generated pages.

Risk: Audio generation sends lesson text, vocabulary, and definitions to an online speech service.

Mitigation: Avoid confidential material when generating audio.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bjbook/skills/zhz-english-learning)
- [Project homepage](http://openclaw.bjbook.net/)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, Text, Audio]

**Output Format:** [Vocabulary Markdown, quiz JSON, interactive HTML pages, lesson text, and MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates four linked, responsive learning pages and audio for lesson text and vocabulary.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
