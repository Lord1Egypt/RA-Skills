## Description: <br>
SkillScout helps agents find and evaluate OpenClaw AI skills using a curated catalog with trust scores and security review summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nashbot67](https://clawhub.ai/user/nashbot67) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use SkillScout before installing or recommending OpenClaw skills, especially when comparing skills by purpose, trust score, permissions, and review notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat SkillScout ratings as an authoritative security gate. <br>
Mitigation: Use the catalog as a discovery aid and manually verify each recommended skill before installation. <br>
Risk: Safe-rated entries can still involve network access, credentials, execution, or file writes. <br>
Mitigation: Review permissions, source behavior, and install instructions for each selected skill, especially before use in sensitive environments. <br>
Risk: Review helper scripts may be unsafe for untrusted or oddly formatted skill names until temporary-file handling and input validation are hardened. <br>
Mitigation: Avoid running those scripts on untrusted inputs; prefer read-only manual review or isolated execution until hardened. <br>


## Reference(s): <br>
- [ClawHub SkillScout listing](https://clawhub.ai/nashbot67/skillscout) <br>
- [SkillScout catalog](https://nashbot67.github.io/skillscout) <br>
- [SkillScout skills API](https://nashbot67.github.io/skillscout/data/skills.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON-style text returned through command-line examples or MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trust scores, ratings, permissions, install commands, categories, and review summaries may be included when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
