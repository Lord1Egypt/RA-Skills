## Description: <br>
Checks installed ClawHub skills for available upgrades, interprets version and changelog differences, assesses risk, and runs confirmed upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaowh3613](https://clawhub.ai/user/zhaowh3613) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit installed ClawHub skills, compare local and registry versions, review upgrade risk, and execute selected updates after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update installed skills through the logged-in ClawHub CLI. <br>
Mitigation: Review the proposed skill names, version changes, risk ratings, and exact clawhub update commands before approving any update. <br>
Risk: Major upgrades may introduce breaking changes. <br>
Mitigation: Require separate confirmation for each major upgrade and perform manual review when changelog evidence is unavailable. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhaowh3613/skill-upgrade-checker) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown tables, summaries, recommendations, confirmation prompts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI and a logged-in ClawHub session; update commands are presented for confirmation before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
