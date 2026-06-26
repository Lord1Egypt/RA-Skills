## Description: <br>
Design, compare, research, and plan SDR projects for OpenClaw, including hardware and software selection, architecture choices, and implementation planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadud](https://clawhub.ai/user/dadud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to choose SDR project stacks and translate them into OpenClaw-friendly designs with separated hardware, ingest, decoding, storage, API, and UI layers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SDR hardware or network receiver services may be exposed more broadly than intended. <br>
Mitigation: Use least-privilege USB or device mappings, bind services to localhost or trusted interfaces, and require firewall, VPN, or authentication controls for remote access. <br>
Risk: Radio traffic may be recorded, archived, rebroadcast, or published in ways that create legal, privacy, or policy issues. <br>
Mitigation: Verify local law and privacy obligations before capturing, storing, sharing, or publishing radio traffic. <br>
Risk: Example setup snippets may be followed without enough review for the user's host, hardware, or deployment model. <br>
Mitigation: Review skill guidance before installing packages, changing device access, or applying runtime configuration. <br>


## Reference(s): <br>
- [SDR Project Design](SKILL.md) <br>
- [Architecture Patterns](references/architecture-patterns.md) <br>
- [Browser Receiver](references/browser-receiver.md) <br>
- [Common Failure Modes](references/common-failure-modes.md) <br>
- [Dashboard UI Patterns](references/dashboard-ui-patterns.md) <br>
- [Example Builds](references/example-builds.md) <br>
- [General Desktop and Utility](references/general-desktop-and-utility.md) <br>
- [Hardware Driver Integration](references/hardware-driver-integration.md) <br>
- [Implementation Recipes](references/implementation-recipes.md) <br>
- [OpenClaw Build Patterns](references/openclaw-build-patterns.md) <br>
- [Platform Deployment](references/platform-deployment.md) <br>
- [Project Intake](references/project-intake.md) <br>
- [Project Landscape](references/project-landscape.md) <br>
- [Reverse Engineering](references/reverse-engineering.md) <br>
- [Satellite Weather](references/satellite-weather.md) <br>
- [Scanner Public Safety](references/scanner-public-safety.md) <br>
- [SDR Research Deep Dive](references/sdr-research-deep-dive.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with optional inline code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include architecture recommendations, implementation order, risk notes, and platform-specific setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
