## Description: <br>
Interact with TruCheq P2P commerce protocol - browse verified marketplace listings, chat with sellers via XMTP, pay via x402 on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vduda](https://clawhub.ai/user/vduda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to browse verified peer-to-peer marketplace listings, inspect seller trust indicators, create listings, message sellers through XMTP, and initiate x402 payments through the TruCheq API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide payment actions through x402 marketplace endpoints. <br>
Mitigation: Require explicit user confirmation before any payment request or payment proof is sent, and use only a trusted TRUCHEQ_API_URL. <br>
Risk: The skill can guide uploads, World ID proof verification, and XMTP seller messaging. <br>
Mitigation: Require explicit confirmation before uploads, proof verification, or XMTP messages, and do not provide private keys or secrets to the skill. <br>


## Reference(s): <br>
- [TruCheq Protocol ClawHub listing](https://clawhub.ai/vduda/trucheq-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with HTTP endpoints, JSON payloads, and curl-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, TRUCHEQ_API_URL, and XMTP_ENV configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
