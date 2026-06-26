## Description: <br>
Syncs team skills from a configured Git repository into a local OpenClaw skills directory, with setup, scheduled sync, manual sync, log viewing, and uninstall workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzj666666](https://clawhub.ai/user/wzj666666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and team administrators use this skill to install shared skills from a trusted team Git repository and keep them updated through scheduled or manual syncs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic sync can keep changing local OpenClaw skill behavior from an unpinned Git repository. <br>
Mitigation: Use only trusted repositories, review repository changes before syncing, and pin the configured source to a trusted commit or branch when stability matters. <br>
Risk: Syncing replaces local skill directories and may affect future OpenClaw sessions. <br>
Mitigation: Back up ~/.openclaw/skills before enabling sync and open a new OpenClaw session only after reviewing the updated skills. <br>
Risk: Scheduled cron jobs continue pulling updates until removed. <br>
Mitigation: Remove the qg-skill-sync OpenClaw cron jobs when continuing automatic updates are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzj666666/qg-skill-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and bash; setup commands configure local sync state and OpenClaw cron jobs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
