## Description: <br>
Seisoai is a unified media generation gateway for agents that discovers tools dynamically, chooses API key or x402 authentication, invokes image, video, audio, music, 3D, and training tools, and handles queued jobs reliably. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Legendarylibr](https://clawhub.ai/user/Legendarylibr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover Seisoai media tools, price and authenticate requests, invoke image, video, audio, music, 3D, and training workflows, and handle queued job results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize paid x402 requests or spend API-key credits. <br>
Mitigation: Require explicit user approval before paid calls, check pricing before invocation, and keep payment authority scoped to the current task. <br>
Risk: Media prompts, URLs, or payloads may expose secrets or sensitive personal media. <br>
Mitigation: Avoid sending secrets or sensitive media in prompts or URLs, and review payloads before submitting them to Seisoai endpoints. <br>
Risk: Face-swap and voice-clone workflows can affect a person's identity or likeness. <br>
Mitigation: Use identity-affecting workflows only with clear authorization from the person involved. <br>
Risk: Agent-scoped routes can broaden authority beyond normal media generation. <br>
Mitigation: Use agent-scoped routes only when explicitly required, bind to one verified agent ID, enforce that agent's tool allowlist, and stop on ownership or scope ambiguity. <br>


## Reference(s): <br>
- [Seisoai homepage](https://seisoai.com) <br>
- [ClawHub skill page](https://clawhub.ai/Legendarylibr/seiso) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint selection, authentication posture, queue polling guidance, and safety controls for agent-scoped routes.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
