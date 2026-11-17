## Description: <br>
长篇网文拆文分析工具免费版,帮助网文作者与文学爱好者提取章节大纲、分析故事节奏、梳理人物关系、追踪伏笔并导出分析报告. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and literary-analysis users use this skill to study long-form web novels, compare story structure, and improve their own writing through outline, pacing, character, foreshadowing, and thrill-point analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read manuscript files and write analysis reports in the local workspace. <br>
Mitigation: Run it only in a workspace prepared for the manuscript content and review output paths before writing reports. <br>
Risk: The skill describes command execution for local analysis workflows. <br>
Mitigation: Review generated commands before execution and install optional dependencies only from trusted package sources. <br>
Risk: The optional callback_url could send private or copyrighted text analysis to an external endpoint. <br>
Mitigation: Use callback_url only with trusted destinations, or omit it for sensitive manuscripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/story-analyze-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports, structured text, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local analysis report files from user-provided manuscript inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
