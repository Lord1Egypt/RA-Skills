## Description: <br>
Translates rigid scene triggers into rich 6-element spatial intents for smart home control with manual override and personalized mode roaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home automation designers use this skill to translate legacy scene-button events into six-element spatial intents and demonstrate how avatar preferences can override default smart-space modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local demo can create S2 data folders, mock files, and a SQLite database wherever it is run. <br>
Mitigation: Run it in a dedicated workspace and review or remove generated local data after testing. <br>
Risk: Hotel roaming, surveillance, and physical-control behavior is conceptual unless integrated with real automation systems. <br>
Mitigation: Before connecting to real devices, add explicit authorization, consent, device allowlists, safety limits, and cleanup or retention controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-classic-scene-parser) <br>
- [Project homepage](https://space2.world) <br>
- [S2-SP-OS Ultimate Whitepaper](artifact/S2-SP-OS-Ultimate-Whitepaper.md) <br>
- [S2-SP-OS Classic Scene Parser Whitepaper](artifact/S2-SP-OS经典场景语义降维解析白皮书.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python execution instructions, console text, JSON files, and a local SQLite log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local demo may create S2 data folders, mock JSON files, rendered timeline tracks, and an s2_chronos.db SQLite database in the directory where it is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
