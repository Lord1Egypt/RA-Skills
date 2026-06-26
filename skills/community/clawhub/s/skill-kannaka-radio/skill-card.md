## Description: <br>
Kannaka Radio is an operator skill for checking and operating a modular Icecast ghost-DJ station, including status, schedule, listeners, perception, voice DJ, broadcast controls, and social announcement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickflach](https://clawhub.ai/user/nickflach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and authorized service maintainers use this skill to inspect Kannaka Radio status, listener data, schedules, perception output, and voice or broadcast workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live broadcast actions, voice DJ toggles, service restarts, and public social posting workflows. <br>
Mitigation: Use it only as an authorized operator and require explicit confirmation before actions that restart services, broadcast generated audio, toggle voice DJ, or post publicly. <br>
Risk: The skill references sensitive credentials for Flux, voice, and AI music integrations. <br>
Mitigation: Use least-privilege tokens, keep credentials out of prompts and logs, and rotate or revoke tokens if exposure is suspected. <br>
Risk: External CLI, server, and script behavior is not verified by the card evidence. <br>
Mitigation: Inspect the external CLI, server, and scripts before use and review proposed commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickflach/skill-kannaka-radio) <br>
- [Kannaka Radio stream](https://radio.ninja-portal.com/stream) <br>
- [Kannaka Radio API state endpoint](https://radio.ninja-portal.com/api/state) <br>
- [Kannaka Radio listeners endpoint](https://radio.ninja-portal.com/api/listeners) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference live service endpoints, external CLI behavior, sensitive credential requirements, and operator confirmations.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
