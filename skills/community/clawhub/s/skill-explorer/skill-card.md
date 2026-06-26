## Description: <br>
Systematically discover, evaluate, compare, and assess OpenClaw skills to find a suitable and safe option for a specific task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riverfor](https://clawhub.ai/user/riverfor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to search for OpenClaw skills, compare candidates, inspect metadata, review safety signals, and produce recommendation reports before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can force-install arbitrary third-party skills during inspection. <br>
Mitigation: Prefer metadata inspection and manual review first; run download or analyze actions only in a disposable or tightly scoped environment after user approval. <br>


## Reference(s): <br>
- [Skill Explorer on ClawHub](https://clawhub.ai/riverfor/skill-explorer) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [explore.sh](artifact/scripts/explore.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with comparison tables, recommendation summaries, safety notes, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include candidate metrics, trade-offs, installation guidance, and manual review findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
