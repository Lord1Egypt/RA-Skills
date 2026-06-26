## Description: <br>
Interact with QR Coin auctions on Base by checking auction status, viewing bids, creating new bids, or contributing to existing bids. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktaesthetix](https://clawhub.ai/user/ktaesthetix) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to participate in QR Coin auctions on Base, including reading auction data and preparing wallet or Bankr transaction prompts for USDC bids. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bankr or wallet prompts can authorize real USDC transactions on Base. <br>
Mitigation: Before signing, verify the QR Coin site, Base network, auction contract, active token ID, URL/name, amount, gas fee, and allowance. <br>
Risk: Broad USDC approvals can leave unused allowance after bidding. <br>
Mitigation: Use limited approvals where possible and revoke unused allowance after participation. <br>


## Reference(s): <br>
- [QR Coin](https://qrcoin.fun) <br>
- [QR Auction Contract on BaseScan](https://basescan.org/address/0x7309779122069EFa06ef71a45AE0DB55A259A176) <br>
- [USDC on Base](https://basescan.org/token/0x833589fCD6eDb6E08f4c7c32D4f71b54bdA02913) <br>
- [ClawHub Skill Page](https://clawhub.ai/ktaesthetix/qrcoin) <br>
- [Publisher Profile](https://clawhub.ai/user/ktaesthetix) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and transaction prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Base contract addresses, function selectors, status-query commands, and wallet transaction guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
