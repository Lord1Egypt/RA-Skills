## Description: <br>
Face recognition and identity memory for AI assistants that enrolls known people with reference photos, identifies faces in inbound images with names, confidence scores, and an llm_context string, and runs locally without cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonacox-sam](https://clawhub.ai/user/jasonacox-sam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent local face memory for intentionally shared photos, including enrolling known people, identifying faces, and managing unknown-face crops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically identify people in user-shared photos. <br>
Mitigation: Use it only in workspaces where local biometric recognition is acceptable, and avoid identifying or enrolling people who have not agreed to it. <br>
Risk: The skill retains face-related data, including enrolled face records and unknown-face crops. <br>
Mitigation: Review and periodically delete the workspace face database and unknown-face crops when retained biometric data is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonacox-sam/sam-faces) <br>
- [Publisher profile](https://clawhub.ai/user/jasonacox-sam) <br>
- [Skill metadata homepage](https://github.com/jasonacox-sam/sam-faces) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI output is JSON and optional annotated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the sam-faces CLI and stores a local face database plus unknown-face crops in the workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
