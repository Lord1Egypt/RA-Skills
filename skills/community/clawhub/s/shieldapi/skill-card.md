## Description: <br>
ShieldAPI provides x402-paid security intelligence endpoints for AI agents, including password breach checks, email and domain reputation, IP and URL safety, prompt-injection checks, package checks, and full security scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alberthild](https://clawhub.ai/user/alberthild) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use ShieldAPI to request security intelligence about passwords, emails, domains, IPs, URLs, prompts, packages, MCP servers, and skill artifacts before taking action or integrating external resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 endpoints can spend USDC and require payment signing. <br>
Mitigation: Use demo mode first, set wallet or payment limits before paid calls, and delegate signing to a secure wallet or signer instead of exposing raw private keys. <br>
Risk: Selected indicators are sent to an external API, and scanned domains, URLs, and IPs may be logged by the service. <br>
Mitigation: Avoid submitting secrets, confidential internal URLs, sensitive prompts, private emails, or internal infrastructure indicators unless external processing and logging are acceptable. <br>
Risk: The full password-hash endpoint is deprecated and increases privacy exposure. <br>
Mitigation: Use the k-anonymity password range endpoint and compare hash suffixes locally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alberthild/shieldapi) <br>
- [ShieldAPI Privacy Policy](https://shield.vainplex.dev/privacy.html) <br>
- [ShieldAPI Health and Discovery Endpoint](https://shield.vainplex.dev/api/health) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for API calls; paid endpoints use x402 payment unless demo mode is used.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
