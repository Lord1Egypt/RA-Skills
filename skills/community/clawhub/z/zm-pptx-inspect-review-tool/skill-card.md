## Description: <br>
ZM PPTX 检查与审核工具用于读取、解析、提取、检查、拆分、合并或审核 PPTX 文件，重点支持渲染核验、文本抽取、备注/版式/资源检查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxn](https://clawhub.ai/user/jerryxn) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, presentation authors, and reviewers use this skill to inspect, extract, render-check, edit, split, merge, and audit PowerPoint decks. It is especially oriented toward PPTX review workflows that need text extraction, notes/layout/resource checks, screenshots or render evidence, and PASS / NEEDS_REVISION / BLOCKED conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local commands and modify unpacked Office files while processing PPTX content. <br>
Mitigation: Use it in an isolated workspace or container, review commands before execution, and avoid processing untrusted Office files outside a controlled environment. <br>
Risk: Server security evidence reports an under-disclosed native LibreOffice workaround that may compile and preload code from a shared temporary location in some sandboxed environments. <br>
Mitigation: Run LibreOffice conversion steps only in a sandboxed environment with controlled temporary directories, and inspect or disable native shim behavior when local policy does not allow it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jerryxn/skills/zm-pptx-inspect-review-tool) <br>
- [SKILL.md](SKILL.md) <br>
- [Editing Presentations](editing.md) <br>
- [PptxGenJS Tutorial](pptxgenjs.md) <br>
- [PPTX Review AI Readiness Checklist](checklists/ai_readiness_checklist.md) <br>
- [Subagent Execution Prompt](templates/subagent_execution_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, review checklists, and file-oriented workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or modify PPTX-related files, unpacked Office XML, thumbnails, screenshots, and review reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
