## Description: <br>
Session Cleanup periodically removes expired OpenClaw session, queue, Telegram, subagent, backup, and temporary memory files while reporting the cleanup results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to schedule or manually run cleanup of expired operational and conversation data. It is intended for environments where automatic deletion of stale session artifacts is acceptable after local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically delete OpenClaw session, queue, Telegram, subagent, backup, and memory files. <br>
Mitigation: Install only where unattended cleanup is intended, review the target paths before scheduling, and back up any data that may need to be retained. <br>
Risk: The documented cron command references run.sh, while the artifact entry point is cleanup.sh. <br>
Mitigation: Fix the schedule to call the actual entry point or add the missing wrapper before enabling cron. <br>
Risk: There is no dry-run or quarantine mode in the artifact behavior. <br>
Mitigation: Test manually in a non-critical environment and add dry-run, quarantine, or restore safeguards before production scheduling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xaiohuangningde/session-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Configuration] <br>
**Output Format:** [Shell script output and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a dated cleanup log under /tmp and reports remaining cron run and delivery queue counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
