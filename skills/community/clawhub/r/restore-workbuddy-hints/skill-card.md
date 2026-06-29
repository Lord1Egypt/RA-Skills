## Description: <br>
Restore WorkBuddy UI hints and tips that were dismissed via the '不再显示' button. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WorkBuddy users use this skill to list or restore UI hints that were hidden after selecting 'Don't show again'. It can restore all dismissed hints or a specific hint key by editing the local WorkBuddy user-state file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The restore script modifies the local WorkBuddy user-state file. <br>
Mitigation: Confirm the target action with the user, close WorkBuddy before making changes, and restart WorkBuddy after the script runs. <br>
Risk: Restoring all hints may re-enable more dismissed prompts than the user intended. <br>
Mitigation: Use the list mode first when the user wants to restore only one hint, then run the key-specific mode for that hint. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes list, restore-all, and restore-by-key modes for local WorkBuddy hint state.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
