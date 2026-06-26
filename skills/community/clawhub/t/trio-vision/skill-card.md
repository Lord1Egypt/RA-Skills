## Description: <br>
Turn any live camera into a smart camera: describe what to watch for in plain English, ask questions about live streams, set up continuous monitoring with custom conditions, or get periodic summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drandrewlaw](https://clawhub.ai/user/drandrewlaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw agents to Trio by MachineFi for live video question answering, event monitoring, and periodic stream digests. It is intended for authorized camera, livestream, RTSP, RTSPS, and HLS sources where the user can provide a Trio API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live camera frames or stream-derived observations may be sent to Trio, webhooks, or chat destinations. <br>
Mitigation: Use only streams you own or are authorized to monitor, avoid private or regulated spaces unless consent and compliance obligations are handled, and disclose where outputs are sent. <br>
Risk: Continuous monitoring jobs can keep running and continue sending surveillance-derived alerts. <br>
Mitigation: Prefer finite monitoring durations, retain job IDs, and cancel jobs when monitoring is no longer needed. <br>
Risk: The Trio API key is required to call the service. <br>
Mitigation: Store TRIO_API_KEY securely and never expose or log the key in user-visible output. <br>


## Reference(s): <br>
- [Trio API Docs](https://docs.machinefi.com) <br>
- [Trio Console](https://console.machinefi.com) <br>
- [Trio by MachineFi](https://machinefi.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/drandrewlaw/trio-vision) <br>
- [Publisher Profile](https://clawhub.ai/user/drandrewlaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples, JSON API response handling, and concise user-facing summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIO_API_KEY and curl or python3; may produce job IDs, trigger explanations, status summaries, and API error remediation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
