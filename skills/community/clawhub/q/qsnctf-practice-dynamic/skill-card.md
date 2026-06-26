## Description: <br>
Fetches the QSNCTF practice platform leaderboard and recent solve activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and CTF practitioners use this skill to check the QSNCTF leaderboard and recent solve activity from public QSNCTF endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends lookup requests to www.qsnctf.com. <br>
Mitigation: Use it only where outbound requests to the public QSNCTF service are acceptable. <br>
Risk: The helper script depends on the Python requests package. <br>
Mitigation: Install dependencies from a trusted Python environment before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/qsnctf-practice-dynamic) <br>
- [QSNCTF leaderboard API](https://www.qsnctf.com/api/5dboard/playlist) <br>
- [QSNCTF solve activity API](https://www.qsnctf.com/api/5dboard/viewlist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text tables from CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to www.qsnctf.com and the Python requests package.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
