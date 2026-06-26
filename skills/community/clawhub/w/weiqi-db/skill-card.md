## Description: <br>
weiqi-db 围棋棋谱数据库是本地棋谱管理工具，支持SGF导入、元数据编辑、标签管理、全文搜索，并将数据存储于单个JSON文件，提供AI友好的JSON接口。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Go/weiqi users use this skill to manage a local SGF game-record database, search records, edit metadata and tags, and export SGF files for review or replay workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local database commands can modify or permanently delete game records. <br>
Mitigation: Keep backups of ~/.weiqi-db/database.json and review proposed delete, clear, overwrite, update, and tag commands before execution. <br>
Risk: The get -o export option can write SGF content to arbitrary local paths. <br>
Mitigation: Use explicit temporary or intended output paths and avoid paths that point to important existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangbin2025/weiqi-db) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, delete, and export local SGF database records under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
