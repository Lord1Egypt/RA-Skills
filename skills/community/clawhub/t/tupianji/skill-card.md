## Description: <br>
图片姬 is an image-prompt and visual-design skill that helps agents create illustration prompts and optional image-generation outputs through AI-driven style analysis, parameter customization, and recommendation or user-selection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, educators, and developers use this skill to turn topics, teaching concepts, poems, or design goals into structured image-generation prompts. It recommends or confirms visual style, audience, mood, composition, color, knowledge structure, and text-treatment choices before producing the final prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers and confirmation-skip shortcuts can cause the agent to move from recommendation to final prompt generation before the user has reviewed the design direction. <br>
Mitigation: Use explicit commands when skipping confirmation and review the selected style, audience, structure, and text content before using generated prompts for important work. <br>
Risk: AI-inferred visual style, audience, or composition choices may be unsuitable or misleading for high-stakes educational or commercial material. <br>
Mitigation: Review inferred recommendations against the intended audience and purpose, then ask the agent to revise any mismatched style, color, layout, or explanatory text. <br>
Risk: Private reference material or sensitive file content supplied to the skill may be incorporated into generated prompt text or browser-backed workflows. <br>
Mitigation: Avoid providing sensitive files or private references unless those details are intended to appear in prompt outputs, and redact confidential details before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/tupianji) <br>
- [参数系统与决策流程](artifact/docs/参数系统.md) <br>
- [智能推荐系统](artifact/docs/智能推荐.md) <br>
- [文字处理系统](artifact/docs/文字处理.md) <br>
- [Prompt模板库](artifact/docs/模板库.md) <br>
- [优秀prompt示例](artifact/examples.md) <br>
- [参考素材](artifact/reference.md) <br>
- [知识可视化专家](artifact/知识可视化专家.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prompt proposals and final image-generation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include two to three visual方案 for user selection before producing a final prompt.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
