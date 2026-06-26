## Description: <br>
Guides Aptos dApp developers through SmoothSend gasless transaction sponsorship, including wallet adapter setup, Script Composer stablecoin transfers, pricing, and common integration mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building Aptos dApps use this skill to add SmoothSend-sponsored gasless transactions, configure wallet adapter submission, and handle paid-credit or insufficient-credit behavior before mainnet use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frontend SmoothSend API keys and npm package trust affect the security of the integration. <br>
Mitigation: Use only API keys intended for frontend use, keep keys in environment variables, and confirm you trust SmoothSend and the npm packages before installing. <br>
Risk: Sponsoring every wallet-adapter transaction can create billing or abuse exposure on mainnet. <br>
Mitigation: Start on testnet, confirm the app's billing policy, and add abuse controls before enabling mainnet sponsorship. <br>
Risk: Insufficient SmoothSend credits can cause transaction submission failures for users. <br>
Mitigation: Handle 402 insufficient-credit responses with a user-friendly fallback and monitor credit balance before production use. <br>


## Reference(s): <br>
- [SmoothSend Docs](https://docs.smoothsend.xyz) <br>
- [SmoothSend Pricing](https://docs.smoothsend.xyz/pricing) <br>
- [SmoothSend Dashboard](https://dashboard.smoothsend.xyz) <br>
- [@smoothsend/sdk on npm](https://www.npmjs.com/package/@smoothsend/sdk) <br>
- [ClawHub Skill Page](https://clawhub.ai/iskysun96/smoothsend-gasless) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, TSX, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; it does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
