## Description: <br>
Generate 3D avatars (VRM/GLB/MML) from text prompts or images via Sideload.gg. Pay-per-use with any x402 wallet (USDC on Base). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DirectiveCreator](https://clawhub.ai/user/DirectiveCreator) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creators use this skill to generate 3D avatar assets from text prompts or image references, then download or use GLB, VRM, MML, and processed PNG outputs in games, virtual worlds, social apps, VTubing, and Three.js experiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local image generation can upload any user-specified local file to Sideload.gg. <br>
Mitigation: Use only non-sensitive image files and prompts that are intended to be sent to Sideload.gg. <br>
Risk: The unchecked --output option can write downloads outside the intended output folder. <br>
Mitigation: Avoid path-like output names such as ../name until filename confinement is fixed. <br>
Risk: Generation requires a payment authorization token. <br>
Mitigation: Probe the price first and pass only a one-time scoped x402 payment token, not wallet private keys. <br>


## Reference(s): <br>
- [Sideload.gg](https://sideload.gg) <br>
- [Sideload API Documentation](https://sideload.gg/agents/raw) <br>
- [x402 Protocol](https://x402.org) <br>
- [Coinbase x402 SDK](https://github.com/coinbase/x402) <br>
- [@pixiv/three-vrm](https://github.com/pixiv/three-vrm) <br>
- [VRM Specification](https://vrm.dev/en/) <br>
- [MML](https://mml.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, API calls] <br>
**Output Format:** [Markdown guidance with Node.js command examples, JSON API/status responses, result URLs, and downloaded GLB, VRM, and PNG files when downloads are enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation requires a one-time scoped x402 payment token; each completed generation returns GLB, VRM, MML, and processed PNG outputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
