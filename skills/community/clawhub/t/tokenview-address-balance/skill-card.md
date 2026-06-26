## Description: <br>
Query the balance of a blockchain address through the Tokenview API, defaulting to BTC and requiring a Tokenview API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bdonglobal](https://clawhub.ai/user/bdonglobal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check blockchain wallet balances during user-requested balance lookups. It is useful when an agent needs to call Tokenview with a wallet address and return a concise balance result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses are sent to Tokenview. <br>
Mitigation: Use the skill only when the user intends to query that address, and avoid submitting sensitive or private wallet addresses unnecessarily. <br>
Risk: The Tokenview API key is placed in a request URL and could appear in logs or error output. <br>
Mitigation: Use a low-privilege or disposable Tokenview API key and redact API-key values from logs and errors before sharing output. <br>
Risk: Broad address-detection triggers can cause unintended lookups from ambiguous prompts. <br>
Mitigation: Require explicit user confirmation before sending an address to Tokenview when the prompt is ambiguous. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bdonglobal/tokenview-address-balance) <br>
- [Tokenview Balance API Host](https://services.tokenview.io/vipapi/addr/b) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the helper script, mapped to concise user-facing balance text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOKENVIEW_API_KEY. Sends the requested address and coin to Tokenview; BTC is the documented default.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
