## Description: <br>
Compresses agent skills to reduce token cost; trigger it with /skill-compressor or when users ask to optimize, compress, or slim down a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david0ming](https://clawhub.ai/user/david0ming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to analyze a SKILL.md path, classify skill content, and write a reduced copy plus a reduction report under .reduced without overwriting originals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local skill files and may read directories that contain private keys or secrets. <br>
Mitigation: Use an explicit SKILL.md path and avoid running it on skill directories that contain private keys or secrets. <br>
Risk: Compressed skill output may omit or alter behavior if accepted without review. <br>
Mitigation: Review the generated .reduced/ files and REDUCTION_REPORT.md before replacing originals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/david0ming/skill-compressor) <br>
- [SkillReducer methodology paper](https://arxiv.org/abs/2603.29919) <br>
- [README.md](artifact/README.md) <br>
- [background.md](artifact/background.md) <br>
- [examples.md](artifact/examples.md) <br>
- [templates.md](artifact/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and concise report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes compressed outputs under the target skill's .reduced/ directory and leaves originals unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
