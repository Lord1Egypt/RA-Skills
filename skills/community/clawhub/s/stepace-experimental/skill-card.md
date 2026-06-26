## Description: <br>
Generate, queue, or schedule AI music on an Android phone through the StepAce Experimental app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckadirt](https://clawhub.ai/user/ckadirt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and music creators use this skill to turn natural-language music requests into immediate or scheduled StepAce generation jobs, including optional lyrics, tempo, key, duration, language, and time signature settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pairing token can queue music on the user's phone if exposed. <br>
Mitigation: Treat STEPACE_TOKEN like a password, avoid sharing it, and regenerate it in the StepAce Experimental app if it is exposed. <br>
Risk: The skill sends outbound requests to a disclosed third-party bridge endpoint. <br>
Mitigation: Install only if the user trusts StepAce Experimental and the disclosed bridge endpoint, and review casual or scheduled music requests before sending them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckadirt/stepace-experimental) <br>
- [Publisher profile](https://clawhub.ai/user/ckadirt) <br>
- [StepAce homepage](https://cronicaia.com) <br>
- [OpenClaw bridge queue endpoint](https://openclaw-bridge.torrico-villanueva-cesar-kadir.workers.dev/openclaw/queue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses STEPACE_TOKEN for pairing, supports immediate and scheduled generation, and produces user-facing queue status details when the bridge accepts a job.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
