## Description: <br>
Register and control reCamera Pro devices from an agent, including onboarding, AI detection models, rule-based triggers, event polling with snapshots, JPG/RAW/MP4 capture, recorded-clip browsing, storage management, and GPIO control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichizer0](https://clawhub.ai/user/ichizer0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect agents to owned reCamera Pro devices for camera setup, AI event detection, media capture, recording management, storage operations, and GPIO control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad control over cameras, storage, media retrieval, recording rules, and GPIO. <br>
Mitigation: Install only for agents that are intended to operate owned reCamera devices, and require explicit user confirmation before destructive or physical-world actions such as formatting storage, deleting files, clearing events, changing GPIO, or modifying recording rules. <br>
Risk: Device tokens, returned images, videos, and relay URLs can expose sensitive credentials or media. <br>
Mitigation: Treat credentials and media outputs as sensitive, avoid logging tokens or returned media unnecessarily, and keep the device registry file private. <br>
Risk: Unsecured transport settings can expose device traffic on untrusted networks. <br>
Mitigation: Use HTTPS with certificate validation when possible and avoid allow_unsecured except on a trusted LAN. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ichizer0/recamera-intellisense) <br>
- [reCamera documentation](https://wiki.seeedstudio.com/recamera/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command examples and shell commands; runtime command results are JSON, text, base64 media payloads, or relay URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use a single JSON object argument and can return sensitive device, credential-adjacent, image, video, storage, or GPIO state.] <br>

## Skill Version(s): <br>
2.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
