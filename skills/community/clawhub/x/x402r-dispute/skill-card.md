## Description: <br>
Pay merchants and file payment disputes on the x402r refundable payments protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vraspar](https://clawhub.ai/user/vraspar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and agent operators use this CLI skill to make x402r escrow payments, file refund disputes, check dispute status, view evidence, and verify arbiter rulings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for wallet authority and can initiate payment and dispute transactions. <br>
Mitigation: Use a dedicated low-balance test wallet and verify the configured npm package, network, RPC, operator, and arbiter before running payment or dispute commands. <br>
Risk: Evidence and payment details may be sent to configured services and may become public or difficult to remove. <br>
Mitigation: Review evidence content before submission and avoid submitting private or sensitive material unless disclosure is acceptable. <br>
Risk: Production evidence pinning depends on a configured Pinata JWT; without it, the artifact falls back to a placeholder CID. <br>
Mitigation: Configure a real Pinata JWT or another supported evidence storage path before relying on dispute evidence in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vraspar/x402r-dispute) <br>
- [Publisher profile](https://clawhub.ai/user/vraspar) <br>
- [x402r homepage](https://x402r.org) <br>
- [Support issues](https://github.com/x402r/x402r-arbiter-eigencloud/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [CLI text output with optional JSON files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can write local state under ~/.x402r and optional response files.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
