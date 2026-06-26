## Description: <br>
Use Renderful from OpenClaw for image/video/audio/3D creation with model discovery, quote-before-generate workflow, deterministic polling, and insufficient-funds/x402 fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luv005](https://clawhub.ai/user/luv005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to coordinate Renderful media generation through OpenClaw tools, including model discovery, quote review, generation polling, balance checks, and payment fallback handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media generation can trigger external-service actions and costs if generation is approved without reviewing the quote. <br>
Mitigation: Use the skill's quote-before-generate flow and review the selected model, prompt, and quoted cost before approving side effects. <br>
Risk: Payment fallback and insufficient-funds flows may require funding steps or x402 payment details. <br>
Mitigation: Surface payment requirements, deposit addresses, shortfall, and x_payment requirements to the user before retrying generation. <br>
Risk: Webhook configuration can expose generation events to untrusted endpoints. <br>
Mitigation: Only configure webhooks for endpoints the user owns and trusts. <br>


## Reference(s): <br>
- [Renderful homepage](https://renderful.ai) <br>
- [ClawHub skill page](https://clawhub.ai/luv005/renderful-generation) <br>
- [Publisher profile](https://clawhub.ai/user/luv005) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with structured tool-call sequencing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides quote-before-generate, deterministic polling, insufficient-funds handling, x402 payment fallback, and webhook setup review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
