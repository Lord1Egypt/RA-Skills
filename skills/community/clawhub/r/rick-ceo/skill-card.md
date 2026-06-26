## Description: <br>
Turn an OpenClaw agent into an operator for daily briefings, revenue monitoring, task prioritization, heartbeat checks, and weekly synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricksmartbrain-boop](https://clawhub.ai/user/ricksmartbrain-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo founders and developers use this skill to have an agent prepare daily business briefings, rank work by revenue impact, check project health, and summarize weekly operating progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad operator-style authority to inspect local repositories, processes, sessions, uptime, and possible financial accounts. <br>
Mitigation: Run it only in intended workspaces and require approval before file edits, deployments, customer contact, purchases, account changes, process termination, or authenticated business-tool use. <br>
Risk: Daily briefing output may include promotional upsell text. <br>
Mitigation: Set RICK_QUIET=1 when promotional output is not desired. <br>


## Reference(s): <br>
- [Rick's Revenue-First Prioritization Framework](references/prioritization-framework.md) <br>
- [ClawHub skill page](https://clawhub.ai/ricksmartbrain-boop/rick-ceo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefings, ranked lists, health summaries, and memos with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect local git status, TODO markers, tmux sessions, site uptime, and Stripe CLI data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
