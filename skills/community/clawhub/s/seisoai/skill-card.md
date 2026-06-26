## Description: <br>
Unified media generation gateway for agents. Discover tools dynamically, choose API key or x402 auth, invoke image/video/audio/music/3D/training tools, and handle queue jobs reliably. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Legendarylibr](https://clawhub.ai/user/Legendarylibr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover Seisoai media tools, price and invoke image, video, audio, music, 3D, training, and agent-scoped jobs, and handle queued results reliably. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use paid API keys or x402 payments. <br>
Mitigation: Use a dedicated Seisoai key or wallet with strict spending limits, check pricing first, and require explicit confirmation before paid jobs. <br>
Risk: Face-swap and voice-cloning tools can involve identity-sensitive media. <br>
Mitigation: Use these tools only with clear authorization from the people involved. <br>
Risk: Agent-scoped routes can operate privileged workflows if the target agent or tool scope is ambiguous. <br>
Mitigation: Deny agent-scoped calls by default, bind an exact agent ID, enforce the declared tool allowlist, and record agent ID, route, tool ID, and reason in run notes. <br>


## Reference(s): <br>
- [Seisoai homepage](https://seisoai.com) <br>
- [ClawHub skill listing](https://clawhub.ai/Legendarylibr/seisoai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live discovery, pricing checks, authentication choices, queue polling, and agent-scoped safety guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
