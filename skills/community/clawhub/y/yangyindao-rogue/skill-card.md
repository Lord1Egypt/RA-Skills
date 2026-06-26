## Description: <br>
阴阳岛肉鸽 is a pixel-art cultivation roguelike game where players choose a class, evolve weapons, advance realms, survive tribulations, and remove curses on Yin Yang Island. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[121212165](https://clawhub.ai/user/121212165) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and agents use this skill to launch and interact with a browser-based Chinese cultivation roguelike. The included interface supports direct play, game-state inspection, action execution, and simple AI decision workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger phrases may invoke the skill unintentionally. <br>
Mitigation: Use explicit invocation by skill name or a specific trigger phrase when launching the game. <br>
Risk: Game progress and achievements are stored in browser localStorage. <br>
Mitigation: Use a trusted browser profile and clear site data when local persistence is not desired. <br>
Risk: Opening the page may contact Google Fonts for styling. <br>
Mitigation: Review or restrict external font requests in environments that require offline or controlled network behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/121212165/yangyindao-rogue) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SPEC.md](artifact/SPEC.md) <br>
- [AI_INTERFACE_SPEC.md](artifact/AI_INTERFACE_SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with a local HTML game artifact and JavaScript interface examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The game runs in the browser, stores progress locally, and may request Google Fonts for styling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
