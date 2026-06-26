## Description: <br>
SoulKeeper audits agent identity rules, detects behavioral drift in transcripts, and produces context-aware reminders before an agent responds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use SoulKeeper to convert SOUL.md, TOOLS.md, and AGENTS.md files into structured rules, check transcripts for drift, and request reminders before high-friction actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder output may actively influence agent behavior around credentials, logged-in sessions, social posting, trading, browser automation, memory files, and permission checks. <br>
Mitigation: Review and edit reminder content before use, and keep explicit confirmation gates for external posts, financial or account actions, secret access, and system changes. <br>
Risk: The security verdict is suspicious because the skill includes broad action-oriented prompts such as not asking permission and using available tools. <br>
Mitigation: Install only in controlled workspaces where the desired operating rules are understood, and scan or review the scripts before deployment. <br>


## Reference(s): <br>
- [SoulKeeper ClawHub page](https://clawhub.ai/cassh100k/soulkeeper) <br>
- [Publisher profile](https://clawhub.ai/user/cassh100k) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact clawpkg.yaml](artifact/clawpkg.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text, with generated JSON rule files and drift reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3.8+ standard library scripts; audit.py can write soul_rules.json for later drift and reminder checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/clawpkg.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
