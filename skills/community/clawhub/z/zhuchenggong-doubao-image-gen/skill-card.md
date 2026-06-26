## Description: <br>
豆包AI图片生成技能 - 视觉设计师专用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Visual designers use this skill to guide an agent through Doubao web image generation, including prompt confirmation, aspect-ratio selection, preview sharing, user selection, and saving confirmed images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated images are sent through Doubao and the message channel. <br>
Mitigation: Install only when this data handling is acceptable, and avoid entering sensitive prompts or sharing sensitive generated images. <br>
Risk: Confirmed generated images are saved under D:\OpenClaw\downloads\images\. <br>
Mitigation: Manually delete saved images when they are no longer needed. <br>


## Reference(s): <br>
- [Doubao image creation page](https://www.doubao.com/chat/create-image) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Images, Files, Shell commands] <br>
**Output Format:** [Markdown guidance with user-visible image previews and saved local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Confirmed downloads are copied to D:\OpenClaw\downloads\images\.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
