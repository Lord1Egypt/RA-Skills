## Description: <br>
The trust layer for AI agents: encrypted channels, identity, audit, attestations, trust circles, key rotation, and federation using the MLS protocol (RFC 9420). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicholasraimbault](https://clawhub.ai/user/nicholasraimbault) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and use Skytale MCP tools for encrypted multi-agent messaging, shared context, identity, audit logging, attestations, trust circles, key rotation, and federation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive credentials or key-exchange material could be exposed if API keys, key packages, or Welcome messages are logged, displayed, or sent through channels. <br>
Mitigation: Treat SKYTALE_API_KEY, key packages, and Welcome messages as opaque secrets; pass them only through intended setup or tool paths and keep them out of user-visible output. <br>
Risk: Misconfigured access can prevent Skytale channels from being created, joined, or used reliably. <br>
Mitigation: Confirm Python, the Skytale MCP package, the openclaw.json server entry, and SKYTALE_API_KEY are configured before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicholasraimbault/skytale) <br>
- [Skytale OpenClaw integration documentation](https://skytale.sh/docs/integrations/openclaw) <br>
- [Skytale application](https://app.skytale.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and SKYTALE_API_KEY for Skytale MCP setup.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release evidence; artifact frontmatter: 0.5.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
