## Description: <br>
Token Stats scans OpenClaw session JSONL files and reports prompt, cache, and output token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ASauler](https://clawhub.ai/user/ASauler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to measure token consumption across local session history, including daily totals, per-session rankings, cache usage, and date-filtered reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session history, which may contain sensitive usage context. <br>
Mitigation: Run it only in trusted local environments and avoid sharing generated reports unless the session-derived information is appropriate to disclose. <br>
Risk: Using --include-deleted can include deleted or backup session files in reports. <br>
Mitigation: Use --include-deleted only when intentionally reconstructing full history, and review the resulting report before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ASauler/token-stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON token-usage reports with shell commands for running the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include global totals, daily breakdowns, per-session rankings, date ranges, and optional deleted or backup session files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
