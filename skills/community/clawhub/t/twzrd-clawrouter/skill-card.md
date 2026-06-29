## Description: <br>
TWZRD Preflight for ClawRouter is a pre-spend gate that helps agents check ClawRouter or BlockRun payment readiness before routing x402 USDC spend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twzrd-sol](https://clawhub.ai/user/twzrd-sol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a TWZRD readiness check before ClawRouter or BlockRun spend flows, then continue, warn, or abort based on the returned decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The preflight gate can fail open when unavailable, so it should not be treated as a fail-closed payment-control system. <br>
Mitigation: Use it as an advisory pre-spend check, keep explicit logs for skipped preflight calls, and require separate controls for high-value or policy-bound spend. <br>
Risk: Wallet-enabled payment flows can sign transactions or spend funds through ClawRouter or BlockRun integrations. <br>
Mitigation: Use a dedicated low-balance wallet, keep spend limits small, and avoid shared or high-value production wallets. <br>
Risk: Coarse preflight calls without the real seller wallet provide weaker scoring. <br>
Mitigation: Pass the server-observed seller wallet or payTo value whenever available before routing spend. <br>
Risk: The included receipt helper is not proof that a user's own paid receipt was validated. <br>
Mitigation: Verify real paid receipts with the TWZRD verifier or MCP receipt-verification tool and persist receipt evidence for audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twzrd-sol/twzrd-clawrouter) <br>
- [TWZRD homepage](https://intel.twzrd.xyz) <br>
- [TWZRD x402 descriptor and receipt spec](https://intel.twzrd.xyz/.well-known/x402) <br>
- [TWZRD MCP endpoint](https://intel.twzrd.xyz/mcp) <br>
- [ClawRouter](https://github.com/BlockRunAI/ClawRouter) <br>
- [BlockRun](https://blockrun.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with bash, curl, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces preflight integration instructions, decision-handling guidance, and receipt-verification examples for agent payment flows.] <br>

## Skill Version(s): <br>
0.1.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
