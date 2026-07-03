## Description: <br>
Screenclaw helps an agent operate Windows desktop software by using coordinate-grid screenshots to locate targets and then issue mouse, keyboard, screenshot, and batch automation commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginsing1226](https://clawhub.ai/user/ginsing1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use Screenclaw to automate visible Windows desktop applications when application APIs, CLI tools, browser automation, or specialized skills are not available. It is suited for screenshot-guided clicking, typing, keypresses, window discovery, desktop-level actions, and reusable scenario templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad desktop control through screenshots, mouse actions, keyboard input, remote transfer behavior, installation steps, and credential-handling workflows. <br>
Mitigation: Install and use it only when intentional, keep the service bound to localhost where possible, use a unique token, and review actions before operating sensitive applications. <br>
Risk: Screenshots and session data may expose passwords, financial information, private chats, regulated data, or other sensitive screen contents. <br>
Mitigation: Avoid using the skill on sensitive screens, minimize captured data, and delete persisted screenshots and session data when finished. <br>
Risk: The release workflow may require downloading a ScreenClaw binary before operation. <br>
Mitigation: Verify any downloaded ScreenClaw binary yourself before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ginsing1226/skills/screenclaw) <br>
- [ScreenClaw releases](https://github.com/GinSing1226/ScreenClaw/releases) <br>
- [ScreenClaw repository](https://github.com/GinSing1226/ScreenClaw) <br>
- [ScreenClaw configuration](references/config.md) <br>
- [ScreenClaw script usage](scripts/README.md) <br>
- [ScreenClaw self-check checklist](references/self_check.md) <br>
- [Scenario template workflow](references/scenarios/README.md) <br>
- [Recording-to-scenario workflow](references/scenarios/recording_to_scenario.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, script outputs, JSON API summaries, and reusable scenario-template Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local screenshot paths, session data paths, coordinate-adaptation results, and scenario templates; desktop actions require screenshot verification after execution.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
