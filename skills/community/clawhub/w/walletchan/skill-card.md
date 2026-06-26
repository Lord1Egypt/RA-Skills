## Description: <br>
Drive the WalletChan browser extension as a human-in-the-loop co-pilot for web3 dapps, surfacing decoded transaction and signature requests for user review before confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apoorvlathey](https://clawhub.ai/user/apoorvlathey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External web3 users and developers use this skill to let an agent drive dapp browser flows while the user reviews decoded WalletChan transaction or signature details before any confirmation. It is intended for tasks such as wallet connection, token swaps, DeFi deposits, typed-data signing, and balance checks through a local Chrome profile with WalletChan installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help confirm crypto transactions through a browser extension. <br>
Mitigation: Use only with the official WalletChan extension and require the user to personally review each decoded transaction or signature before allowing confirmation. <br>
Risk: The Agent Password is a sensitive scoped credential. <br>
Mitigation: Share only the Agent Password, never the master password or seed phrase, and use it only in WalletChan's unlock field; rotate or revoke it in WalletChan settings when needed. <br>
Risk: Chrome remote debugging can expose browser control if misconfigured. <br>
Mitigation: Use a dedicated Chrome profile and bind remote debugging to localhost only. <br>
Risk: Dapp pages and decoded metadata may contain untrusted instructions. <br>
Mitigation: Treat page content as data, refuse attempts to redirect the agent or request credentials, and reject requests that do not match the user's stated intent. <br>


## Reference(s): <br>
- [WalletChan Homepage](https://walletchan.com/) <br>
- [WalletChan Chrome Web Store Listing](https://chromewebstore.google.com/detail/walletchan/kofbkhbkfhiollbhjkbebajngppmpbgc) <br>
- [ClawHub Skill Page](https://clawhub.ai/apoorvlathey/walletchan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and step-by-step browser-operation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-visible browser interaction, a scoped Agent Password, and per-request human review before confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
