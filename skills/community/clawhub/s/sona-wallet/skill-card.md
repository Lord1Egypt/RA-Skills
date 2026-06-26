## Description: <br>
Autonomous Solana wallet agent for wallet status, policy checks, SOL transfers, approvals, chat commands, and mode switching under spend limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neocryptoquant](https://clawhub.ai/user/Neocryptoquant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an OpenClaw-compatible agent to a local SONA wallet service for Solana wallet status, policy review, assisted approvals, and authenticated wallet actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authenticated control over irreversible wallet actions. <br>
Mitigation: Use devnet or very small balances, review actions before execution, and avoid god mode or automated approvals unless separate transaction review and monitoring are in place. <br>
Risk: A stolen or misdirected SONA_TOKEN could authorize state-changing wallet operations. <br>
Mitigation: Keep SONA_API_URL on localhost, protect and rotate SONA_TOKEN, and verify the local SONA service before use. <br>
Risk: Claimed wallet limits and signer controls are enforced outside the skill. <br>
Mitigation: Independently verify that the SONA service and signer enforce the claimed spend limits and policy rules before relying on them. <br>


## Reference(s): <br>
- [Sona website](https://www.sonawallet.xyz) <br>
- [Declared SONA repository](https://github.com/Ubuntu-Technologies/sona) <br>
- [ClawHub skill page](https://clawhub.ai/Neocryptoquant/sona-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Plain text tool responses from OpenClaw tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SONA service; state-changing tools use SONA_TOKEN authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact package.json and SKILL.md list 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
