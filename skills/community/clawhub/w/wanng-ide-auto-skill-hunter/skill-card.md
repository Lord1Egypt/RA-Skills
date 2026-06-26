## Description: <br>
Proactively discovers, ranks, and installs high-value ClawHub skills by mining unresolved user needs and agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to find, rank, preview, and install ClawHub skills when current capabilities do not cover a task or when repeated unresolved needs appear in recent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect prior conversations, task memory, and profile or personality files to identify capability gaps. <br>
Mitigation: Review the local data sources before use and avoid running it in workspaces containing sensitive session history. <br>
Risk: The skill can modify the local skills directory by cloning or scaffolding selected skills and running their self-tests. <br>
Mitigation: Start with --dry-run, cap installs with --max-install 1 or --max-install 2, and manually review selected repositories before enabling live installation. <br>
Risk: The skill can send recommendation reports outside the local environment when reporting is enabled. <br>
Mitigation: Set SKILL_HUNTER_NO_REPORT=1 unless external reporting is explicitly approved for the workspace. <br>
Risk: Scheduled --auto runs may repeatedly add new skill code without direct operator review. <br>
Mitigation: Avoid scheduled --auto runs in sensitive environments and require human review before keeping newly installed skills. <br>


## Reference(s): <br>
- [Wanng Ide Auto Skill Hunter on ClawHub](https://clawhub.ai/terrycarter1985/wanng-ide-auto-skill-hunter) <br>
- [terrycarter1985 Publisher Profile](https://clawhub.ai/user/terrycarter1985) <br>
- [Memory Mesh Core on ClawHub](https://clawhub.ai/wanng-ide/memory-mesh-core) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style recommendation report with command-line output and installed skill files when live installation is enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write SKILL.md, index.js, and .hunter.json files for selected skills unless run with --dry-run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
