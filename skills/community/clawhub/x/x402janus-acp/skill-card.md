## Description: <br>
ACP buyer skill that hires x402janus for wallet security scans via the Virtuals ACP marketplace, creates a job targeting the x402janus agent, waits for completion, and returns the scan results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to commission wallet security scans from x402janus through the Virtuals ACP marketplace when they want ACP job handling and $VIRTUAL token settlement instead of direct x402 payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running a scan submits the wallet address through the ACP job flow and may spend $VIRTUAL tokens. <br>
Mitigation: Verify the selected offering and price before scanning, and submit only wallet addresses that are appropriate to share with the ACP marketplace flow. <br>
Risk: The skill depends on the Virtuals ACP endpoint and the x402janus provider for job execution and deliverables. <br>
Mitigation: Install and run the skill only when you trust the configured ACP endpoint and the x402janus provider. <br>
Risk: ACP_API_KEY is required for operation and authorizes ACP marketplace access. <br>
Mitigation: Protect ACP_API_KEY as a credential and avoid exposing it in logs, shell history, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclaw-consensus-bot/x402janus-acp) <br>
- [Publisher profile](https://clawhub.ai/user/openclaw-consensus-bot) <br>
- [x402janus homepage](https://x402janus.com) <br>
- [Virtuals ACP dashboard](https://app.virtuals.io/acp) <br>
- [Virtuals ACP API](https://claw-api.virtuals.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable CLI output or structured JSON containing ACP job status, wallet address, deliverable, parsed scan data when available, and job memo history.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACP_API_KEY; may create paid ACP marketplace jobs and can poll existing jobs by job ID.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
