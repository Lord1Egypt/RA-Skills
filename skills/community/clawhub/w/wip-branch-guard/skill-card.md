## Description: <br>
Wip Branch Guard is a Claude Code and OpenClaw hook that enforces branch discipline, blocks destructive commands, requires repo onboarding before first write, tracks blocked-file retries, and gates external pull request creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to keep coding agents off protected branches, require onboarding reads before repository writes, and surface unsafe or out-of-scope mutation attempts before they execute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The current command allowlist can let some writes through that users may expect a strict branch guard to block. <br>
Mitigation: Review before installing as a strict main-branch protection control, and patch or validate the allowlist against actual write destinations if stronger enforcement is required. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/parkertoddbrooks/wip-branch-guard) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces hook decisions, denial guidance, SessionStart warnings, and installation configuration for agent workflows.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
