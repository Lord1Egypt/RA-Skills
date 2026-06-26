## Description: <br>
Rewrites text into one of 10 supported tones while preserving the original meaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Daisuke134](https://clawhub.ai/user/Daisuke134) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to rewrite user-provided text for tone adjustment in messages, drafts, and other short-form content through a paid x402 service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text to an external tone-rewriting endpoint. <br>
Mitigation: Avoid sending confidential, regulated, proprietary, or credential-like text unless the external service and its data handling are trusted. <br>
Risk: Using the skill requires a paid x402 flow that can spend USDC. <br>
Mitigation: Install only if the awal CLI and payment flow are trusted, and monitor usage and spend. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Daisuke134/tone-rewriter) <br>
- [Tone rewriter x402 endpoint](https://anicca-proxy-production.up.railway.app/api/x402/tone-rewriter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response with rewritten text and tone metadata, plus Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Input text is capped at 2000 characters; requests are paid at $0.01 USDC via x402.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
