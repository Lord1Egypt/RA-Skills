## Description: <br>
Stream editor for filtering and transforming text using scripts. Use for find-and-replace, text manipulation, and batch file editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to transform text streams and apply find-and-replace, deletion, insertion, and file-editing operations from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In-place editing can overwrite or remove unintended file content. <br>
Mitigation: Test substitutions without in-place mode first, confirm target paths, and keep backups for important files. <br>
Risk: The command name may resolve to an unexpected executable in the user's environment. <br>
Mitigation: Confirm what executable the sed-tool command runs before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/sed-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and text-editing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or describe in-place file edits; users should review target files before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
