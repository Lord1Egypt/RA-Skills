## Description: <br>
Manages storage, naming, classification, and verification for user-provided files and agent-generated outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buptlihang](https://clawhub.ai/user/buptlihang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to organize user input files and generated outputs into predictable workspace folders, apply naming conventions, and run validation or cleanup scripts before handing files back to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The repair flow can delete /workspace/my_outputs/output after attempting to move nested output files, which may remove valuable generated outputs if the move did not preserve them as expected. <br>
Mitigation: Review and back up /workspace/my_outputs/output before running fix-nested.sh, and use the skill only when explicit file organization is intended. <br>
Risk: move.sh copies arbitrary local paths into managed workspace folders without stronger path validation. <br>
Mitigation: Avoid passing sensitive or unintended local paths to move.sh until safer validation is added. <br>


## Reference(s): <br>
- [Smart File Manager on ClawHub](https://clawhub.ai/buptlihang/smart-file-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides workspace file organization conventions and scripts for initialization, movement, verification, and nested-output cleanup.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
