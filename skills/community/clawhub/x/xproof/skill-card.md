## Description: <br>
xProof helps agents anchor hashed proof and audit records on MultiversX/Base through REST, MCP, and x402 payment flows before significant actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonxkensei](https://clawhub.ai/user/jasonxkensei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add proof-before-action logging, public verification, and audit trails to agents that take financial, compliance, publishing, or other high-accountability actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proof and audit workflows can externally record sensitive reasoning, prompts, session content, filenames, hashes, or metadata. <br>
Mitigation: Record only hashes, opaque identifiers, and redacted summaries; do not upload raw prompts, chain-of-thought, secrets, personal data, proprietary logic, or detailed trading/security rationale. <br>
Risk: API keys and x402 payment payloads are credentials that can authorize paid proof actions. <br>
Mitigation: Treat pm_ keys and X-Payment payloads as secrets, store them outside source control, rotate on exposure, and set spending caps or human approval thresholds for autonomous payments. <br>
Risk: Proof URLs, hashes, filenames, and metadata may be public or durable. <br>
Mitigation: Assume records are long-lived and public before submitting them; use neutral filenames and metadata that do not reveal sensitive business, user, or operational details. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/jasonxkensei/xproof) <br>
- [xProof Platform](https://xproof.app) <br>
- [Agent Context Documentation](https://xproof.app/agent-context) <br>
- [MCP Endpoint](https://xproof.app/mcp) <br>
- [Source Repository](https://github.com/jasonxkensei/xproof-openclaw-skill) <br>
- [Support Issues](https://github.com/jasonxkensei/xproof-openclaw-skill/issues) <br>
- [xProof API Reference](references/api-reference.md) <br>
- [Certification API](references/certification.md) <br>
- [MCP Server](references/mcp.md) <br>
- [x402 Payments](references/x402.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, JSON payloads, and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may cause agents to create external proof or audit records and may initiate paid x402 or API-key authenticated proof calls when configured.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence and ClawHub metadata; artifact/xproof/SKILL.md frontmatter reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
