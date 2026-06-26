## Description: <br>
Generate images and videos through the renderful.ai API with API-key authentication and optional crypto payment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luv005](https://clawhub.ai/user/luv005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call Renderful for AI image and video generation, configure authentication, and check generation status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call Renderful's paid generation API and may trigger crypto payments through x402. <br>
Mitigation: Use a dedicated API key, keep x402 disabled unless needed, and require explicit approval before each paid request. <br>
Risk: Wallet-based payments can spend funds without defined safeguards. <br>
Mitigation: Use a dedicated low-balance wallet and revoke or rotate credentials after use. <br>


## Reference(s): <br>
- [Renderful API](https://api.renderful.ai/v1) <br>
- [Renderful Dashboard](https://renderful.ai/dashboard) <br>
- [Renderful Pricing](https://renderful.ai/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/luv005/renderful-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with curl examples and JSON request/response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RENDERFUL_API_KEY; x402 wallet settings should be used only with explicit approval and spending limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
