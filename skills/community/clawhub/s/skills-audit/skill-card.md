## Description: <br>
Security audit + append-only logging + monitoring for OpenClaw skills (file-level diff, baseline approval, SHA-256 integrity). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucloud-sec](https://clawhub.ai/user/ucloud-sec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to statically audit installed skills, keep local audit history, inspect file-level diffs, manage approved baselines, and generate change notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill indexes and snapshots local OpenClaw skills for audit history. <br>
Mitigation: Install only when local skill indexing and snapshot history are intended, and review the files written under the local skills-audit state directory. <br>
Risk: Optional QianXin reputation lookup can contact an external service using a bundle-level MD5 lookup. <br>
Mitigation: Keep QianXin intelligence disabled unless that lookup is acceptable, and enable it only with a user-provided token after reviewing the configured endpoint. <br>
Risk: Monitoring notifications may send summaries or diff-related details to an external channel. <br>
Mitigation: Review cron jobs and notification targets before enabling monitoring, and send concise summaries by default rather than raw diffs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucloud-sec/skills-audit) <br>
- [scripts/README.md](scripts/README.md) <br>
- [templates/README.md](templates/README.md) <br>
- [QianXin SafeSkill service](https://safeskill.qianxin.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, plus local JSON/NDJSON audit files and notification text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit logs, state, baseline files, git snapshots, and optional notification text; optional remote MD5 reputation lookup is disabled by default.] <br>

## Skill Version(s): <br>
1.5.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
