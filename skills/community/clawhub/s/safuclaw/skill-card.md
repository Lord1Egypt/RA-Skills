## Description: <br>
Security audit gate - scans agent skills for malware, prompt injection, and data exfiltration before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alikayhan](https://clawhub.ai/user/alikayhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Safuclaw before installing third-party skills to request a paid security audit, review trust-score findings, and decide whether installation should proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill contents may be sent to a third-party paid audit service. <br>
Mitigation: Avoid submitting private or proprietary skill files unless sharing them with Safuclaw is acceptable. <br>
Risk: Audit requests can spend wallet funds through the x402 payment flow. <br>
Mitigation: Use a dedicated low-balance Base wallet and require explicit approval for each 0.99 USDC audit. <br>
Risk: If Safuclaw is unavailable, security verification cannot be completed. <br>
Mitigation: Do not install the target skill automatically; wait for an explicit user decision before proceeding without verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alikayhan/safuclaw) <br>
- [Safuclaw homepage](https://safuclaw.com) <br>
- [Safuclaw audit API](https://api.safuclaw.com/v1/audit) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with HTTP request examples and structured audit-result descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require x402 payment flow and a funded Base wallet with USDC before the audit API returns results.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
