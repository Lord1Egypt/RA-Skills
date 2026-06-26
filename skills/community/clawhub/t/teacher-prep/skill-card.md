## Description: <br>
教师备课助手，用于小学语文教学备课。支持古诗、现代文、寓言、童话等各类课文。当用户提出备课需求时，自动执行：(1)搜索课文相关资料（原文、作者、背景、生字词、段落分析等），生成markdown备课资料；(2)生成教案PPT；(3)生成Word格式课后练习题及参考答案。适用于小学各年级语文备课场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[870021840](https://clawhub.ai/user/870021840) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Elementary Chinese-language teachers and teaching-support agents use this skill to gather lesson material for poems, modern prose, fables, fairy tales, and other primary-school texts, then generate classroom preparation files. It supports lesson planning by producing Markdown preparation notes, PowerPoint lesson plans, and Word exercise sheets with reference answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search-backed lesson research may expose sensitive student or proprietary details if those details are included in prompts. <br>
Mitigation: Use a scoped Tavily key and avoid including sensitive student, school, or proprietary information in prompts. <br>
Risk: Generated classroom materials may contain inaccurate, incomplete, or unsuitable content for the target grade or lesson. <br>
Mitigation: Review generated Markdown, PowerPoint, and Word materials before classroom use. <br>
Risk: The skill creates local files and may overwrite or clutter working directories during repeated lesson preparation. <br>
Mitigation: Run the skill in a dedicated folder and review generated files before sharing or deploying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/870021840/teacher-prep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, PowerPoint .pptx, and Word .docx files, with local Python script commands when document generation is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped TAVILY_API_KEY for search-backed lesson research and local python-pptx/python-docx support for file generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
