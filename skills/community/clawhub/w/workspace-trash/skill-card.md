## Description: <br>
Soft-delete protection for workspace files that redirects deletion requests into a recoverable trash workflow instead of immediate permanent removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crewhaus](https://clawhub.ai/user/crewhaus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when deleting, removing, or cleaning workspace files so files are moved to recoverable trash with list, restore, empty, and size actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may route many delete, remove, or cleanup requests through this skill. <br>
Mitigation: Require explicit confirmation before delete or trash-empty actions and verify the exact paths before approving them. <br>
Risk: Emptying trash permanently deletes trash contents and cannot be undone. <br>
Mitigation: Show the trash contents first and require explicit user confirmation before running the empty action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crewhaus/workspace-trash) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions with shell command examples and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Moves files into a workspace trash directory and records restore metadata in a manifest.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
