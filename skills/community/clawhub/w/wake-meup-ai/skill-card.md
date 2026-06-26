## Description: <br>
Schedule personalized AI wake-up phone calls via wake.meup.ai for one-time or recurring wake-up calls, including phone verification, call scheduling, voice selection, and x402 USDC payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianium](https://clawhub.ai/user/brianium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to verify a phone number, schedule paid AI wake-up calls, choose a voice, and manage the required wake.meup.ai payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends phone details, schedule, voice choice, and optional personalization hints to a paid third-party phone-call service. <br>
Mitigation: Confirm the user intends to use wake.meup.ai, keep optional hints minimal, and avoid sharing unnecessary personal context. <br>
Risk: Paid endpoints use a Solana keypair to sign x402 USDC payments. <br>
Mitigation: Use a dedicated low-balance Solana keypair and confirm the exact cost before each verification or scheduled call. <br>


## Reference(s): <br>
- [Wake Up homepage](https://wake.meup.ai) <br>
- [Wake Up OpenClaw documentation](https://wake.meup.ai/openclaw) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [x402 documentation](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON API payloads and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solana keypair path for paid x402 USDC calls; optional personalization hints should remain concise and are truncated to 200 characters.] <br>

## Skill Version(s): <br>
1.3.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
