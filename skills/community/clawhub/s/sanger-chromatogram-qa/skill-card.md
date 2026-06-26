## Description: <br>
Use sanger chromatogram qa for data analysis workflows that need structured execution, explicit assumptions, and clear output boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, lab informatics teams, and sequencing analysts use this skill to guide Sanger chromatogram quality checks, mutation verification, clone confirmation, genotyping QC, and SNP validation with explicit assumptions and bounded outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local script execution may read input files and write outputs in the workspace. <br>
Mitigation: Confirm intended input and output paths before running the script, and keep execution inside a project-specific workspace or sandbox. <br>
Risk: The Python dependency is declared without a pinned version. <br>
Mitigation: Install the skill in a project-specific virtual environment and consider pinning numpy before operational use. <br>
Risk: Sequencing QA conclusions can be misleading when required trace, reference, variant position, or threshold inputs are missing or ambiguous. <br>
Mitigation: Require the minimum inputs before analysis and report assumptions, unresolved items, and repeat recommendations explicitly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/sanger-chromatogram-qa) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Packaged Python workflow](artifact/scripts/main.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and text QA report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report quality scores, low-quality base counts, mutation calls, mixed-peak considerations, repeat recommendations, assumptions, risks, and unresolved validation needs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
