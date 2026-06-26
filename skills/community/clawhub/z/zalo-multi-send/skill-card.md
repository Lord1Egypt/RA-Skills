## Description: <br>
Send multiple images or files in a single Zalo message using zca-js with an existing OpenClaw Zalo credential profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanbi97](https://clawhub.ai/user/tuanbi97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents or developers with configured OpenClaw Zalo credentials use this skill to send multiple selected local files or URL downloads to a Zalo user or group in one message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can share selected local files or downloaded URL content through the user's existing Zalo session. <br>
Mitigation: Before running it, verify the recipient ID, group flag, credential profile, caption, and every file path or URL. <br>
Risk: Private files or internal URLs may be disclosed to the chosen Zalo recipient if included in the file list. <br>
Mitigation: Avoid sending sensitive local files or private/internal URLs unless the recipient is intended to receive that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanbi97/zalo-multi-send) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, API Calls] <br>
**Output Format:** [Command-line execution with console status text and JSON send result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing OpenClaw Zalo credential profile; selected local files must be readable and URL sources must be intentionally shareable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
