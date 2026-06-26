## Description: <br>
Use when performing study tasks on browser-based platforms such as Yuketang, Xuexitong, Zhihuishu, and Pintia, including answering quizzes and page actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amiracleta](https://clawhub.ai/user/amiracleta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and learning-platform users use this skill to guide an agent through browser-based study workflows, including reading practice questions, returning answers, filling page controls, recording artifacts, and submitting work only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive a logged-in browser profile for study sites. <br>
Mitigation: Use a dedicated browser profile and confirm the active site, tab, and account before allowing page actions. <br>
Risk: The skill can save screenshots and answer records that may contain course, score, or account information. <br>
Mitigation: Store records in the documented auto-study workspace only and delete them periodically when they contain sensitive information. <br>
Risk: The skill can submit quizzes or assignments when explicitly requested. <br>
Mitigation: Avoid formal exams or prohibited automation, and require explicit user confirmation before any submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amiracleta/test-auto-study) <br>
- [Project homepage](https://github.com/AmiracleTa/Auto-Study-Skill) <br>
- [Agent Browser CLI](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser Skill](https://clawhub.ai/MaTriXy/agent-browser-clawdbot) <br>
- [Yuketang guidance](references/yuketang.md) <br>
- [Xuexitong guidance](references/xuexitong.md) <br>
- [Zhihuishu guidance](references/zhihuishu.md) <br>
- [Pintia guidance](references/pintia.md) <br>
- [Windows runtime guidance](references/runtime-windows.md) <br>
- [WSL runtime guidance](references/runtime-wsl.md) <br>
- [macOS runtime guidance](references/runtime-macos.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and concise text with browser action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local markdown records and screenshots under an auto-study workspace when used to perform study tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
