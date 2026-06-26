## Description: <br>
Query AI agent trust scores, behavioral DNA, and identity verification via SoulLedger protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to check an AI agent's trust score, behavioral profile, and identity signals before interaction. They can also register an agent with SoulLedger and audit identity through hash-chain verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected agent identifiers, display names, and registration details are sent to the SputnikX/SoulLedger service. <br>
Mitigation: Use only approved agent identifiers and avoid submitting sensitive internal names or registration details without authorization. <br>
Risk: Registration can return an API key that functions as a secret. <br>
Mitigation: Store returned API keys in approved secret management and avoid pasting them into logs, prompts, or shared documents. <br>
Risk: Chain-integrity verification may involve a paid x402 USDC action. <br>
Mitigation: Confirm cost, recipient, and policy approval before performing paid verification. <br>


## Reference(s): <br>
- [SoulLedger homepage](https://soulledger.sputnikx.xyz) <br>
- [ClawHub release page](https://clawhub.ai/drivenbymyai-max/soulledger-trust) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote API responses containing agent identifiers, trust scores, behavioral profiles, passport hashes, event counts, and API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
