## Description: <br>
智能提取并生成围棋实战选点题，支持恶手检测、实战对比、交互答题、试下演练及保存SGF功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Go/Weiqi players, coaches, and developers use this skill to convert SGF records with AI analysis into offline interactive move-selection quizzes for practice and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted SGF metadata and comments can be carried into the generated HTML quiz page. <br>
Mitigation: Use SGF files from trusted sources and avoid opening generated quiz pages created from hostile or unknown SGF files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-move) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated single-file HTML quiz output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated quizzes are local HTML files; the page can also save SGF positions.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
