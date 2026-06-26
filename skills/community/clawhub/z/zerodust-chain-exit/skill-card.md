## Description: <br>
Helps agents sweep 100% of native gas tokens from supported EIP-7702 chains to leave the source balance at zero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerodustxyz](https://clawhub.ai/user/zerodustxyz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill when an agent needs to help quote, authorize, and submit native-token sweeps from supported EIP-7702 chains to a destination chain or address. It is intended for complete chain exits, dust consolidation, and multi-chain balance cleanup after the user reviews and signs the required wallet messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps an agent move all native crypto balance off a chain, which can leave the source chain with no gas for later recovery actions. <br>
Mitigation: Install and invoke it only when complete balance removal is intended, and confirm the source chain, destination chain, destination address, exact amount semantics, fees, and estimated receive amount before requesting signatures. <br>
Risk: EIP-7702 delegation and sweep signatures can authorize high-impact wallet actions. <br>
Mitigation: Require the user to inspect the ZeroDust endpoint/provider, typed data, delegation details, revocation authorization, and sweep intent before signing. <br>
Risk: Batch sweeps can obscure per-chain mistakes or unsupported-chain assumptions. <br>
Mitigation: Avoid batch sweeps unless every chain, balance, fee, and destination is reviewed individually. <br>


## Reference(s): <br>
- [ZeroDust Chain Exit on ClawHub](https://clawhub.ai/zerodustxyz/zerodust-chain-exit) <br>
- [ZeroDust API documentation](https://zerodust-backend-production.up.railway.app/docs) <br>
- [ZeroDust backend issues](https://github.com/zerodustxyz/zerodust-backend/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZERODUST_API_KEY for agent endpoints; users must review the quote, source and destination chains, destination address, fees, receive amount, signatures, EIP-7702 delegation details, and revocation status before signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README publish command) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
