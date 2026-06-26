## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help agents record command failures, user corrections, missing capabilities, and reusable lessons in local learning files for later review and promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture private conversation details, secrets, raw transcripts, or command output if used without controls. <br>
Mitigation: Require explicit user approval for persistent logging, redact secrets and private data, avoid raw transcripts or full command output, and keep .learnings local unless sharing is intentional. <br>
Risk: Promoting unresolved learnings into agent memory can preserve incorrect or misleading guidance. <br>
Mitigation: Review entries before promotion, resolve or correct stale items, and scan modified memory or skill files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tigertamvip/self-improving-agent-5) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to append structured entries to .learnings Markdown files and update project memory files after review.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
