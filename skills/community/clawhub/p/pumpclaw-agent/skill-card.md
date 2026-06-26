## Description: <br>
Generate customer-ready Telegram polling bots and an Express-style web server that integrate Pump.fun Tokenized Agent payments using @pump-fun/agent-payments-sdk to build invoices, accept payments, and verify invoices on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[belimad](https://clawhub.ai/user/belimad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to scaffold Telegram polling bots and web services for Pump.fun Tokenized Agent payment flows on Solana. It helps configure invoices, server-side payment verification, run instructions, and smoke-test checklists for customer projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled template may take custody of user crypto funds despite the skill text warning against signing transactions on behalf of users. <br>
Mitigation: Redesign the payment flow to use user-signed wallet transactions before any production use, or add explicit custody disclosures, encrypted key management, audit controls, and withdrawal or recovery handling. <br>
Risk: Running the scaffold with real user funds as-is could expose users to payment custody and recovery failures. <br>
Mitigation: Use only test funds until the custody model, operational controls, and dependency updates have been reviewed and implemented. <br>


## Reference(s): <br>
- [Pumpfun Agent Integration on ClawHub](https://clawhub.ai/belimad/pumpclaw-agent) <br>
- [Pump Tokenized Agents Integration Notes](artifact/references/PUMP_TOKENIZED_AGENTS.md) <br>
- [Pump.fun Tokenized Agents Reference Skill](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with project files, code snippets, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a customer project scaffold, run instructions, and a smoke-test checklist.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
