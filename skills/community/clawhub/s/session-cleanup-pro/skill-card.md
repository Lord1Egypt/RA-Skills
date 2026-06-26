## Description: <br>
Session Cleanup Pro helps review and clean orphan .jsonl files and stale OpenClaw sessions through a scan-first, confirmation-based workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[irideas](https://clawhub.ai/user/irideas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local session storage, identify orphan files and stale sessions, and apply cleanup only after reviewing the scan results and confirming the action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session cleanup can remove session history that a user later needs. <br>
Mitigation: Run the scan first, inspect orphan and stale sessions, and prefer archiving or backing up sessions before approving deletion. <br>
Risk: Hard deletion of stale session files can be irreversible. <br>
Mitigation: Require explicit confirmation before cleanup, use the 72-hour protection window, never delete agent:main:main, and require a second confirmation for hard deletion. <br>


## Reference(s): <br>
- [Session Cleanup Pro release page](https://clawhub.ai/irideas/session-cleanup-pro) <br>
- [Session cleanup policy](artifact/references/policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown summary with inline shell commands and JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and node; scan results include orphan files, stale sessions, protected sessions, and estimated reclaimable bytes.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata; artifact metadata and changelog use 0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
