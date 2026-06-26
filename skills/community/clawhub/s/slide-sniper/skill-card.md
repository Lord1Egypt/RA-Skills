## Description: <br>
后台监控全屏视频或直播，利用视觉模型检测幻灯片翻页，自动截图提取文字并排版到笔记软件中。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnotherJ1](https://clawhub.ai/user/AnotherJ1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Students, instructors, and knowledge workers use this skill to monitor full-screen course videos, livestreams, or webinars, detect slide changes, capture each slide, extract key text, and assemble local notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous screen monitoring and screenshot capture could include private or unrelated screen content. <br>
Mitigation: Use the skill only for content you are allowed to record, confirm the monitored area before starting, and stop monitoring when note capture is complete. <br>
Risk: Saved screenshots and OCR notes may retain accidental private captures in ~/Documents/Notes/SlideSniper. <br>
Mitigation: Review saved files after each session, delete accidental captures, and restrict access to the notes directory when it contains sensitive material. <br>
Risk: Network use for vision or OCR processing is not clearly bounded by the evidence. <br>
Mitigation: Confirm whether screenshots or extracted text are processed by remote services before using the skill with confidential material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AnotherJ1/slide-sniper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown or Word notes with saved screenshots and extracted slide text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes notes and slide screenshots to ~/Documents/Notes/SlideSniper.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
