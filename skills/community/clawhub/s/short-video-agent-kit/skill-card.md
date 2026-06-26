## Description: <br>
Use one dry-run-first interface for agent-generated vertical video payloads across Sora/OpenAI, Gemini Veo, xAI/Grok, and Seedance-style providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidmosiah](https://clawhub.ai/user/davidmosiah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install, configure, verify, and troubleshoot Short Video Agent Kit for MCP-compatible clients while keeping video-generation provider credentials and live calls explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve OAuth tokens, API keys, service-account JSON, local token files, or private user data. <br>
Mitigation: Avoid printing secrets, run doctor, manifest, privacy_audit, connection_status, or dry-run flows first, and only enable live mode with credentials the user intends to use and can revoke. <br>
Risk: Live provider calls may use paid video-generation services or user-owned prompts and assets. <br>
Mitigation: Keep live mode opt-in, confirm user consent and asset ownership before provider calls, and prefer dry-run validation before writes or external requests. <br>
Risk: The npm package and GitHub repository are external third-party dependencies. <br>
Mitigation: Verify the package and repository before installation and consider pinning a known package version. <br>


## Reference(s): <br>
- [Short Video Agent Kit repository](https://github.com/davidmosiah/short-video-agent-kit) <br>
- [short-video-agent-kit npm package](https://www.npmjs.com/package/short-video-agent-kit) <br>
- [ClawHub skill page](https://clawhub.ai/davidmosiah/short-video-agent-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run-first guidance for MCP setup, provider readiness checks, privacy audits, and credential handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
