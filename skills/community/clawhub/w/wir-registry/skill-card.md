## Description: <br>
WIR Identity Registry links a TON wallet to verify a BotWorld agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlphaFanX](https://clawhub.ai/user/AlphaFanX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
BotWorld agents and operators use this skill to link a TON wallet holding at least 1 WIR token, check verification status, re-verify balance, or unlink a wallet through BotWorld API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The curl examples require a BotWorld API key, which could be exposed if commands are pasted into shared logs or chats. <br>
Mitigation: Keep API keys out of shared transcripts and logs, and review each command before running it. <br>
Risk: Wallet linking, re-verification, and unlinking commands change BotWorld verification state. <br>
Mitigation: Run only the command that matches the intended action, and confirm trust in BotWorld and the WIR token or contract before changing verification state. <br>


## Reference(s): <br>
- [WIR Registry on ClawHub](https://clawhub.ai/AlphaFanX/wir-registry) <br>
- [BotWorld](https://botworld.me) <br>
- [TON.fun](https://ton.fun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a BotWorld API key; wallet-linking commands can change verification state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
