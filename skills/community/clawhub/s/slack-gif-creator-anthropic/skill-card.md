## Description: <br>
Knowledge and utilities for creating animated GIFs optimized for Slack, including constraints, validation tools, animation concepts, and local GIF-building helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to create Slack-ready animated GIFs, validate dimensions and timing, and optimize generated frames for emoji or message use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source images and writes GIF output paths on the local filesystem. <br>
Mitigation: Use only image paths intended for processing and output paths intended for GIF creation or replacement. <br>
Risk: Dependency behavior can vary over time because requirements specify version ranges. <br>
Mitigation: Pin dependencies or use a lock file when reproducible builds matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pupuking723/slack-gif-creator-anthropic) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [Runtime dependencies](artifact/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with Python code blocks and generated GIF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated GIFs are local file outputs; validation returns text summaries and dictionaries with GIF properties.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
