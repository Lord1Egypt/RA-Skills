## Description: <br>
UnionSkill复古怀旧广告PPT。图像型工作流：内容分析→大纲确认→逐页生图→PPTX装配。适合文化展示、餐饮推介、文创项目。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn documents, notes, or presentation ideas into UnionSkill-branded retro advertising decks for cultural showcases, restaurant promotions, creative projects, business pitches, exhibitions, and proposals. The workflow requires outline confirmation before generating slide images and assembling the PPTX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs PPTX assembly against local image directories and output paths. <br>
Mitigation: Confirm the intended image directory, topic, and output path before running assembly commands. <br>
Risk: Generated slide images may contain incorrect or unreadable text, especially for Chinese headings. <br>
Mitigation: Review every generated slide image and the final PPTX before delivery. <br>
Risk: The workflow is explicitly UnionSkill-branded and adds watermarks, metadata, and a brand tail page. <br>
Mitigation: Use a different PPT workflow for non-UnionSkill or unbranded deliverables. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/timo2026/union-ad-retro) <br>
- [Retro vintage style guide](artifact/references/style_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated file paths, and optional structured run results from the assembler script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce slide PNGs, an image ZIP archive, a UnionSkill-branded PPTX, a cooperation note, and an optional full-screen HTML deck when the agent has the required image generation and PPTX assembly tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
