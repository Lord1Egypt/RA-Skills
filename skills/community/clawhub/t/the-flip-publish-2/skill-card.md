## Description: <br>
$1 USDC entry. Pick 20 predictions. All 20 coins flip at once each round. Match the first 14 to win the entire jackpot. Live on Solana devnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bedesta5050](https://clawhub.ai/user/bedesta5050) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use The Flip to inspect and interact with a Solana devnet jackpot game: check game state, enter 20 H/T predictions, review ticket status, trigger round flips, and claim eligible winnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a local Solana keypair file and sign devnet transactions. <br>
Mitigation: Use a dedicated devnet wallet with no real assets, review commands before running them, and avoid sharing private key material. <br>
Risk: Some commands can move funds or perform operator actions, including entry, claim, withdraw-fees, and close-game-v1. <br>
Mitigation: Run only commands whose effects you understand, and avoid withdraw-fees or close-game-v1 unless you control and intend the operator action. <br>
Risk: The setup instructions include a curl-piped installer for Solana tooling. <br>
Mitigation: Prefer verified installation steps or inspect the installer before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bedesta5050/the-flip-publish-2) <br>
- [Source Repository](https://github.com/maurodelazeri/the-flip-publish) <br>
- [Live Dashboard](https://the-flip.vercel.app) <br>
- [Solana Devnet Program Explorer](https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read a local Solana keypair and submit Solana devnet transactions when the user runs game commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
