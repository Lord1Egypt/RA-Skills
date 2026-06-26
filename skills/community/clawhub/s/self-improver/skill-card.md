## Description: <br>
Self-improving agent system for OpenClaw that enables continuous learning from interactions, errors, recoveries, and performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent learning, reviewable memory, and hook-based improvement workflows to agent sessions. It supports learning from sessions, errors, recoveries, and performance signals, with manual commands for review and export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning files may capture session, error, recovery, or performance details, including sensitive context. <br>
Mitigation: Use only in workspaces where persistent memory is intended, add redaction for sensitive sessions, and review or delete learning files before sharing or committing them. <br>
Risk: Automatic mode can execute Python hook files from the workspace hooks directory with limited user control. <br>
Mitigation: Review and trust all hook files before enabling automatic mode, keep auto-apply disabled where possible, and scan hooks before deployment. <br>
Risk: Stored learnings can preserve incorrect, stale, or misleading guidance and influence future agent behavior. <br>
Mitigation: Review learnings regularly, remove outdated entries, and require human review before applying learned guidance to sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leohuang8688/self-improver) <br>
- [Publisher profile](https://clawhub.ai/user/leohuang8688) <br>
- [README.md](README.md) <br>
- [USAGE.md](USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text with JSON learning records and optional Markdown exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores learning data in workspace learning files and can export a Markdown summary for review.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
