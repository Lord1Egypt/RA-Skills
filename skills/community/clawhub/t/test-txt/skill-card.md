## Description: <br>
Selects and outputs a Chinese poem based on user input, mapping A to "Yong Liu" and B to "Chun Xiao", with results intended for /workspace/assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luokeer52](https://clawhub.ai/user/luokeer52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can request one of two Chinese poems and receive the selected text. Reviewers should treat this release as a remote Prana/OpenClaw wrapper rather than a purely local poem selector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this release suspicious because its artifacts operate as a credentialed remote Prana/OpenClaw wrapper, not only as a local poem selector. <br>
Mitigation: Install only when remote Prana/OpenClaw execution is intended; for simple poem selection, prefer a local implementation that writes the selected poem directly. <br>
Risk: The artifacts can obtain or use PRANA API keys, send prompts to claw-uat.ebonex.io, persist conversation thread IDs, and access purchase-history links. <br>
Mitigation: Review credential and network access before running, isolate required environment variables, avoid sharing secrets, and clear persisted session state when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luokeer52/test-txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text poem output, file output, and command-oriented Markdown guidance; wrapper clients may emit JSON for status or errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require PRANA/OpenClaw credentials and network access; wrapper clients can persist conversation thread state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
