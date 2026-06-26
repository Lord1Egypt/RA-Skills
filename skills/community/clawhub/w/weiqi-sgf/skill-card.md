## Description: <br>
SGF围棋棋谱转HTML打谱工具 - 将棋谱文件生成可在浏览器中交互回放的网页，支持多级变化分支、试下功能、真实音效。当用户需要"SGF转网页"、"打谱"、"棋谱查看"、"变化图浏览"时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Go players, and reviewers use this skill to convert SGF Go game records into local interactive HTML replay pages for move review, branch exploration, and trial play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated HTML output to a user-selected or default path, which could overwrite an existing file if the path is chosen carelessly. <br>
Mitigation: Choose output paths deliberately and review the generated file location before relying on or sharing the replay page. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-sgf) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Replay generator script](artifact/scripts/replay.py) <br>
- [SGF parser module](artifact/scripts/sgf_parser.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated output is a local HTML replay file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected SGF input files and writes generated HTML to user-selected or default output paths.] <br>

## Skill Version(s): <br>
2.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
