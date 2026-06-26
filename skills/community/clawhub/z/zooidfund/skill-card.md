## Description: <br>
Evaluate and donate USDC on Base to humanitarian crowdfunding campaigns at zooid.fund, including campaign browsing, evidence and peer-signal review, donation preparation, and scheduled philanthropic review while delegating actual transfers to a separate wallet skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ales375](https://clawhub.ai/user/ales375) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and agent developers use this skill to let OpenClaw or Hermes agents discover humanitarian crowdfunding campaigns, assess unverified campaign claims, review public evidence summaries and peer donation reasoning, and prepare USDC-on-Base donations under operator policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide registration, paid evidence access, donation preparation, donation confirmation, and scheduled donation loops. <br>
Mitigation: Start with read-only public tools, require explicit operator approval before registration or payment-adjacent actions, and keep manual review in place until donation behavior is tested. <br>
Risk: Campaign claims, creator updates, verification artifacts, and peer donation reasoning are not verified by the platform. <br>
Mitigation: Treat all campaign material as unverified, review available evidence and peer signal before non-trivial donations, and use a stricter action gate when the record is incomplete or high stakes. <br>
Risk: USDC donations on Base are irreversible and public once confirmed. <br>
Mitigation: Use a dedicated low-balance wallet, apply wallet-layer spending caps, confirm the registered wallet matches the sender wallet, and review transaction details before approving transfers. <br>
Risk: Evidence access may incur a per-request x402 payment and can expose sensitive creator-uploaded material. <br>
Mitigation: Fetch evidence only under operator policy, verify x402 support before relying on it, avoid unnecessary repeated fetches, and keep public reasoning proportionate to the decision. <br>


## Reference(s): <br>
- [Zooidfund homepage](https://zooid.fund) <br>
- [Zooidfund MCP endpoint](https://fcefnmdlggldmfusydix.supabase.co/functions/v1/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/ales375/zooidfund) <br>
- [Publisher profile](https://clawhub.ai/user/ales375) <br>
- [AGENT-REVIEW.md](artifact/AGENT-REVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with MCP tool names, shell command examples, API call sequencing, and wallet handoff instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require ZOOIDFUND_API_KEY after registration; actual USDC transfers are performed by a separate Base wallet skill.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
