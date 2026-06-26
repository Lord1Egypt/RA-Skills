## Description: <br>
Launch Solana tokens on Pump.fun via the SolPaw platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LvcidPsyche](https://clawhub.ai/user/LvcidPsyche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to launch Solana tokens through SolPaw and Pump.fun after explicitly confirming token details, wallet settings, and payment information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend SOL and create irreversible public tokens through a third-party service. <br>
Mitigation: Use a fresh wallet with only the funds needed for the launch and require explicit confirmation of token details, creator wallet, fee signature, endpoint, and initial buy before every launch. <br>
Risk: The documentation and SDK disagree about who signs the launch and who becomes the on-chain creator. <br>
Mitigation: Avoid relying on the SDK launch path until the publisher reconciles the conflict, and prefer the documented local-signing flow when evaluating or using the skill. <br>
Risk: The skill depends on sensitive API keys and a Solana private key in environment variables. <br>
Mitigation: Keep secrets out of code and chat logs, never use a main wallet key, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/LvcidPsyche/solpaw-launcher) <br>
- [SolPaw homepage](https://solpaw.fun) <br>
- [SolPaw API reference](references/api-docs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, TypeScript snippets, configuration values, and API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user invocation and environment variables for the SolPaw API key, creator wallet, Solana private key, and API URL.] <br>

## Skill Version(s): <br>
3.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
