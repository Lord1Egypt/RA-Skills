## Description: <br>
Delete an OpenClaw child session cleanly by removing its transcript, trajectory files, and sessions.json index entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kid0114](https://clawhub.ai/user/kid0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to remove a selected OpenClaw child session from local transcript files and the sessions.json index after confirming the target session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executing the skill deletes local OpenClaw session transcripts, trajectory files, and sessions.json records for the selected child session. <br>
Mitigation: Run without --execute first, confirm the exact session key or session id, and back up important transcripts or sessions.json before executing. <br>
Risk: A wrong or active session target could remove data that is still needed. <br>
Mitigation: Do not guess the target session; stop and ask before deleting active or running sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kid0114/subsession-delete) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Markdown response with shell commands and JSON execution results from the deletion script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode reports candidate deletions; execute mode deletes matching local session files and updates sessions.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
