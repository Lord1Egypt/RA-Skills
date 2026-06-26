## Description: <br>
S2-SP-OS Vision Cast helps agents check LAN display compatibility for AirPlay, Chromecast, Miracast, and DLNA-style casting before using an S2 snapshot push fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to inspect private-network display endpoints and choose a compatible projection route for media URLs or visual snapshots. It is intended for controlled displays and networks where the user has explicit permission to scan and push visual content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can probe LAN display ports and route visual content using credentials. <br>
Mitigation: Limit execution to networks and displays the user controls, require explicit confirmation before each scan or visual push, and provide S2_VISION_TOKEN only when snapshot push is needed. <br>
Risk: The claimed encrypted or ephemeral fallback is not verified by the provided implementation evidence. <br>
Mitigation: Review and test the fallback implementation before relying on it for sensitive visual content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SpaceSQ/s2-vision-projection) <br>
- [S2-SP-OS homepage](https://space2.world/s2-sp-os) <br>
- [S2 Vision Edge Hardware Setup Guide](artifact/setup-guide.md) <br>
- [S2 Vision Projection Memzero Protocol](artifact/S2-MEMZERO-PROTOCOL.md) <br>
- [Agent Reasoning Examples](artifact/AGENT-EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, S2_PRIVACY_CONSENT, and S2_VISION_TOKEN for runtime use.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
