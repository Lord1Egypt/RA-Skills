## Description:

后台监控全屏视频或直播，利用视觉模型检测幻灯片翻页，自动截图提取文字并排版到笔记软件中。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anotherj1](https://clawhub.ai/user/anotherj1)

### License/Terms of Use:


## Use Case:

External users can use this skill while watching full-screen courses, livestreams, or webinars to detect slide changes, capture slide screenshots, extract OCR text, and assemble local study notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill monitors and screenshots the user's screen while network access is requested but not explained.

Mitigation: Review before installing on devices that may display private meetings, chats, documents, or credentials; prefer disabling network access or requiring explicit confirmation and a clear stop command before monitoring starts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anotherj1/skills/slide-sniper)
- [Publisher profile](https://clawhub.ai/user/anotherj1)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown notes with screenshot file references and extracted slide text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes notes and screenshots to a local SlideSniper notes directory when executed by an agent with the required capabilities.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
