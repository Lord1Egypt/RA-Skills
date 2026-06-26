## Description: <br>
Control Roborock robot vacuums for status checks, cleaning commands, maps, consumables, and related device settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dru-ca](https://clawhub.ai/user/dru-ca) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with Roborock or compatible Xiaomi robot vacuums use this skill to turn cleaning, status, maintenance, map, and settings requests into roborock CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that control a physical vacuum and change device settings. <br>
Mitigation: Confirm the target device ID, room IDs, and intended action before running cleaning or settings commands. <br>
Risk: Roborock/Xiaomi account credentials, device IDs, and map images can expose private home and account information. <br>
Mitigation: Enter credentials only into the CLI prompt, keep device IDs and map images out of shared chats or logs, and treat generated map files as private. <br>
Risk: The skill depends on the third-party python-roborock CLI package. <br>
Mitigation: Install only if the package and its account permissions are trusted in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dru-ca/robo-rock) <br>
- [python-roborock](https://github.com/humbertogontijo/python-roborock) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the roborock CLI and a user-provided device ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
