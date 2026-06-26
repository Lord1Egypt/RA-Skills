## Description: <br>
Generates a Node.js CLI tool that scans OpenClaw skill dependency declarations and can report or fix missing npm, pip, Homebrew, and system binary dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianteohx](https://clawhub.ai/user/christianteohx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate a CLI that checks installed OpenClaw skills for missing dependency declarations and optionally installs fixable dependencies after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fix or upgrade modes can change local Homebrew, npm, or pip packages. <br>
Mitigation: Run dry-run or targeted checks first, then review proposed package actions before using fix or upgrade commands. <br>
Risk: Dependency installation may pull packages from untrusted or unexpected sources. <br>
Mitigation: Prefer trusted package sources or verified releases when accepting installation actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, markdown, guidance] <br>
**Output Format:** [Markdown with JavaScript code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run, fix, JSON, report, and targeted skill-check command options for the generated CLI.] <br>

## Skill Version(s): <br>
2.0.9 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
