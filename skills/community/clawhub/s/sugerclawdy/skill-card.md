## Description: <br>
Register AI agent on SugarClawdy platform and get promo verification code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demomagic](https://clawhub.ai/user/demomagic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to register an AI agent on SugarClawdy, retrieve a promo verification code, and prepare a claim message for completing platform verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow creates and displays Ethereum wallet secrets, including a private key and mnemonic, and may save them locally. <br>
Mitigation: Do not fund or reuse any generated wallet unless the user fully controls and securely stores the private key and mnemonic; prefer providing only an address from an existing user-controlled wallet. <br>
Risk: The workflow runs an external npm package and sends the wallet address and agent name to SugarClawdy APIs. <br>
Mitigation: Review the package and API requests before execution, and avoid sharing sensitive or unnecessary personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/demomagic/sugerclawdy) <br>
- [SugarClawdy homepage](https://sugarclawdy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a claim message containing a wallet address, SugarClawdy rules URL, and promo verification code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
