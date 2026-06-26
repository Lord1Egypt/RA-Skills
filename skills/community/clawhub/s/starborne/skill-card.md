## Description: <br>
Starborne runs a sci-fi equipment looter game with rolls, ten-rolls, cargo inventory, sacrifice, energy, and item art generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skb2026](https://clawhub.ai/user/skb2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and entertainment-focused agent users use Starborne to run a persistent sci-fi loot-roll game with equipment collection, upgrades, inventory management, and optional generated item art. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create local image files and a JSON file for saved game state. <br>
Mitigation: Use it in a workspace where those artifacts are acceptable, and delete the saved Starborne files to reset or remove retained gameplay state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skb2026/starborne) <br>
- [Starborne README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown chat responses with optional generated image files and JSON game state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save warehouse state and generated item images under ~/.openclaw/workspace/starborne/.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
