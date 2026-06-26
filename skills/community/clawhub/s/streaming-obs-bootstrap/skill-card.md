## Description: <br>
Rebuild and validate a reusable OBS streaming scene pack via agentic-obs and mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowcrab-dev](https://clawhub.ai/user/snowcrab-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and streaming operators use this skill to rebuild, configure, and validate reusable OBS scene packs for local or remote streaming setups. It helps wire browser overlays over LAN HTTP, apply transition and audio defaults, run recording walkthroughs, and troubleshoot browser-source rendering issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The overlay server can briefly expose workspace files on the LAN. <br>
Mitigation: Run it only on a trusted network, restrict served files to safe workspace content, and stop the background server when finished. <br>
Risk: The skill can change OBS scenes, sources, transitions, and audio settings. <br>
Mitigation: Back up the OBS scene collection first and verify the target OBS host and profile before running setup scripts. <br>
Risk: The stream dry-run helper can start OBS streaming if the configured account is connected to a live destination. <br>
Mitigation: Run stream_dry_run.sh only when the configured OBS account is safe to go live or has been pointed at a non-public test destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snowcrab-dev/streaming-obs-bootstrap) <br>
- [Networking Notes](references/networking.md) <br>
- [Scene Map](references/scene-map.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [v0.2.0 Feature Notes](references/v0.2-features.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands and OBS configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scene setup steps, overlay hosting instructions, validation commands, and troubleshooting notes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server evidence release version and PUBLISH.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
