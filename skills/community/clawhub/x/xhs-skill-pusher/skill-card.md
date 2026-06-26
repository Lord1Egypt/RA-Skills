## Description: <br>
Provides Xiaohongshu content publishing support with cookie file management and xhs-kit based automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glittering](https://clawhub.ai/user/Glittering) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Xiaohongshu session cookies, manage active accounts, validate login state, and publish posts with titles, content, images, tags, and optional scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Xiaohongshu logged-in session cookies. <br>
Mitigation: Use a test or non-critical account, avoid pasting cookies into shell commands, keep cookie files out of git, cloud sync, and logs, and store them with restrictive file permissions. <br>
Risk: The skill can publish live content to an account. <br>
Mitigation: Run status checks and debug-only validation first, and require explicit confirmation before executing an actual publish action. <br>
Risk: Server security evidence flags unsafe secret-handling and command-execution patterns for review. <br>
Mitigation: Review or patch scripts before deployment so secrets are redacted and shell command construction is constrained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Glittering/xhs-skill-pusher) <br>
- [README](README.md) <br>
- [Quick Start](docs/QUICK_START.md) <br>
- [Final Solution Guide](docs/XHS_FINAL_SOLUTION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update cookie JSON files and run xhs-kit publishing commands when executed in an agent environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
