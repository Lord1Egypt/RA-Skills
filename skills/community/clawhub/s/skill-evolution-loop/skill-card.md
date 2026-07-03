## Description: <br>
三件套闭环引擎 v2 links Nuwa, Darwin, and workflow-engine automation with whitelist exclusion, human confirmation, task validation, and retirement checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx281227231](https://clawhub.ai/user/lgx281227231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation maintainers use this skill to scan recent Hermes session logs for repeated tool-backed tasks, generate skill candidates, evolve generated skills, orchestrate workflows, and identify stale auto-generated skills for review or removal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan local Hermes session logs, which may expose local task history. <br>
Mitigation: Run it only in an environment where the agent is permitted to read those logs, and review detected candidates before acting on them. <br>
Risk: Manual run modes can create or alter skills and workflow files under the local Hermes directories. <br>
Mitigation: Start with detect or run --auto, then review the generated candidate report before executing the full run path. <br>
Risk: The gc command can delete auto-generated skill directories when not run in dry-run mode. <br>
Mitigation: Use gc --dry-run first and approve the exact removal targets before running gc without dry-run. <br>
Risk: The skill documentation includes external publishing and synchronization commands. <br>
Mitigation: Approve exact git push, clawhub publish, and scp targets before allowing an agent to run those commands. <br>


## Reference(s): <br>
- [Whitelist Domains](references/whitelist-domains.md) <br>
- [Protected Cron Jobs](references/protected-cron-jobs.md) <br>
- [ClawHub Competitive Intel](references/clawhub-competitive-intel.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/lgx281227231/skill-evolution-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, generated SKILL.md files, workflow YAML, JSON state, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates files under the local Hermes skills and workflow directories when run outside dry-run or auto modes.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
