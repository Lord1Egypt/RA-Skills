## Description: <br>
Builds real-time collaboration apps with whiteboard, live code editing, chat, CRDT sync, and presence indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to plan or build realtime collaboration experiences such as shared whiteboards, pair-programming editors, chat, collaborative documents, and live dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact references create-collab.sh and dev.sh, but those scripts are not included in the release evidence. <br>
Mitigation: Inspect any create-collab.sh or dev.sh script obtained separately before running it. <br>
Risk: Realtime collaboration apps may require Node.js 18+ and Redis services to run locally. <br>
Mitigation: Confirm the local environment and service configuration before installing dependencies or starting the app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/realtime-collab-app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code, shell command, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; review any generated app code and setup scripts before running them.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
