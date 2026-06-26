## Description: <br>
Skill Alchemy Main helps an agent turn a person, method, experience, or existing skills into installable skills by coordinating Lens analysis and LEAP execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to distill personas, methods, or workflows into reusable agent skills, or to fuse existing skills into a combined workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch untrusted remote skill files and produce installed-agent behavior changes. <br>
Mitigation: Review LEAP and Lens before installation, run only where network search and generated output files are acceptable, and inspect generated SKILL.md and references before copying them into an agent skills directory. <br>
Risk: All-default operation may skip review points for sensitive or proprietary targets. <br>
Mitigation: Use explicit checkpoints for sensitive work, confirm source URLs used for exemplars, and avoid all-default mode when generated skills could affect confidential or high-impact workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentsope/skill-alchemy-main) <br>
- [Publisher profile](https://clawhub.ai/user/agentsope) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Lens README_EN.md](artifact/skills/Lens/README_EN.md) <br>
- [LEAP README_EN.md](artifact/skills/LEAP/README_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated skill files and JSON planning artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated skills, references, plans, and audit artifacts under an output directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
