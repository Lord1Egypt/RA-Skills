## Description: <br>
在 Word 中逐字打字显示内容，支持翻页、对齐控制、字体字号自定义，适合现场演示 AI 操作 Word 的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2403861767](https://clawhub.ai/user/2403861767) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, presenters, and demo operators use this skill to create a live Microsoft Word or WPS Writer typing demonstration from a plain-text content file with simple formatting markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Word/WPS automation can alter, clear, close, or save over local documents during a demo. <br>
Mitigation: Run only in a controlled local demo environment, save or close important Word/WPS documents first, and provide an explicit output path. <br>
Risk: The bundled demo content describes broader file-search, browser, code, and email workflows outside the skill's stated Word typing purpose. <br>
Mitigation: Treat content_demo.txt as sample presentation text only and require separate approvals and safeguards before acting on those workflows. <br>
Risk: Sensitive input text could be displayed in Word or written into generated DOCX files. <br>
Mitigation: Use non-sensitive input content for demonstrations and review the content file before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2403861767/word-typewriter-demo) <br>
- [Publisher profile](https://clawhub.ai/user/2403861767) <br>
- [OpenClaw metadata ClawHub link](https://clawhub.com/skill/word-typewriter-demo) <br>
- [OpenClaw metadata repository link](https://github.com/你的用户名/word-typewriter-demo) <br>
- [Artifact repository metadata](https://github.com/2403861767/word-typewriter-demo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with command-line examples; generated DOCX files when the script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Windows Word/WPS, Python, and pywin32; input content controls style, alignment, paging, speed, and save path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
