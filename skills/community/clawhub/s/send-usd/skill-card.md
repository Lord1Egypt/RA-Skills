## Description: <br>
Simulates a USD transfer from one agent to another. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeef23](https://clawhub.ai/user/afeef23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to simulate agent-to-agent USD transfer flows and receive a structured transaction result for testing or workflow orchestration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the simulated transfer result for movement of real funds. <br>
Mitigation: Treat outputs as simulation results and verify any future payment-provider integration requires explicit user confirmation for recipient and amount before transfer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/afeef23/send-usd) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [JSON-like transfer result with success status, transaction identifier, message, and optional error code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Simulation-only; no real payment rails, wallets, bank APIs, or account credentials are accessed according to the security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
