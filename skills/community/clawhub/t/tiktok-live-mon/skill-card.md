## Description: <br>
TikTok Live stream monitoring and recording automation using Playwright-based visual detection and network traffic monitoring to capture FLV stream URLs, check live status, record streams, and support notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor TikTok Live profiles, determine whether a profile is live, extract stream URLs, and record live streams when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe shell command handling can allow crafted input to run local commands on the user's machine. <br>
Mitigation: Review or patch command execution paths before installation, run only with trusted TikTok handles and fixed quality values, and prefer an isolated environment. <br>
Risk: Recording streams, temporary logs, and debug screenshots may create local privacy or storage exposure. <br>
Mitigation: Confirm local recording, temporary logging, and screenshot behavior is acceptable before use, and clean generated files according to the user's privacy and retention needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kikikari/tiktok-live-mon) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce stream URLs, live-status JSON, local recordings, temporary logs, and optional debug screenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
