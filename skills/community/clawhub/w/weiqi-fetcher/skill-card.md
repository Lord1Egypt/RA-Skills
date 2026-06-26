## Description: <br>
围棋分享棋谱下载器 - 从分享链接自动下载SGF棋谱 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangbin2025](https://clawhub.ai/user/zhangbin2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Go players use this skill to download SGF game records from supported public Go platform share links. It can auto-detect supported sources, save SGF files, list supported sources, or use an explicitly selected source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts supported Go platforms and may launch a headless browser for some share links. <br>
Mitigation: Use trusted public share links and review network behavior before deployment. <br>
Risk: The skill writes SGF files locally, with default output under /tmp/weiqi_fetch. <br>
Mitigation: Use an explicit -o output path for files that should be retained or controlled. <br>
Risk: Debug capture or browser automation may leave raw payload files in temporary storage. <br>
Mitigation: Avoid debug capture unless temporary raw payload files are acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Text] <br>
**Output Format:** [SGF files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SGF files to a user-specified path or to /tmp/weiqi_fetch by default.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
