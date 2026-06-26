## Description: <br>
SkillMe helps agents search ClawHub and skills.sh in parallel, compare discovered skills, install selected ClawHub skills, and convert skills.sh skills into OpenClaw-compatible SKILL.md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GHesericsu](https://clawhub.ai/user/GHesericsu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use SkillMe to discover skills across ClawHub and skills.sh, compare candidates, and install or convert selected skills into an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing discovered skills can add persistent third-party agent instructions, including global installs shared across workspaces. <br>
Mitigation: Inspect third-party SKILL.md content before enabling it and prefer workspace installs unless a global install is intentionally needed. <br>
Risk: Search queries and installation commands are passed through shell commands, which can be unsafe if queries include shell metacharacters. <br>
Mitigation: Quote or sanitize search terms and avoid shell metacharacters when running registry searches or install commands. <br>
Risk: The converter can fetch remote skill content and write a SKILL.md file to a chosen path. <br>
Mitigation: Verify the converter path points to this reviewed script, confirm the destination path, and review the converted file before use. <br>


## Reference(s): <br>
- [ClawHub SkillMe listing](https://clawhub.ai/GHesericsu/skillme) <br>
- [skills.sh registry](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with comparison results, inline shell commands, and generated SKILL.md content when converting skills.sh entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a converted SKILL.md file when the conversion script is run with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
