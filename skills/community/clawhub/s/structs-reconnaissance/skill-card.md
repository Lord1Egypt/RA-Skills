## Description: <br>
Gathers Structs game intelligence on players, guilds, planets, fleets, and galaxy state, then persists findings to local memory/intel notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Structs players and operators use this skill to scout targets, assess planet defenses and fleet status, monitor guild strength, and maintain local competitive intelligence before combat or raids. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reconnaissance results can persist sensitive Structs game intelligence in local memory/intel files. <br>
Mitigation: Review the files the skill creates or updates, redact sensitive notes when needed, and avoid using it when reconnaissance should remain temporary. <br>
Risk: Local Guild Stack database queries may expose or summarize sensitive local game intelligence. <br>
Mitigation: Use the PostgreSQL workflow only against an intended local database and limit access to generated dossiers and threat notes. <br>


## Reference(s): <br>
- [Structs intelligence memory README](https://structs.ai/memory/intel/README) <br>
- [Structs database schema](https://structs.ai/knowledge/infrastructure/database-schema) <br>
- [Structs Guild Stack skill](https://structs.ai/skills/structs-guild-stack/SKILL) <br>
- [Threat detection](https://structs.ai/awareness/threat-detection) <br>
- [Opportunity identification](https://structs.ai/awareness/opportunity-identification) <br>
- [Combat mechanics](https://structs.ai/knowledge/mechanics/combat) <br>
- [Reading opponents](https://structs.ai/playbooks/meta/reading-opponents) <br>
- [ClawHub skill page](https://clawhub.ai/abstrct/structs-reconnaissance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell commands, SQL snippets, and local intel file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory/intel Markdown files.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
