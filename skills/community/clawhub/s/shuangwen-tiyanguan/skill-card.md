## Description: <br>
爽文体验馆 is a Chinese text-game launcher that gives agents a menu for entering cultivation, wuxia, Republican-era, and campus story worlds with separate save paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heaven-ll](https://clawhub.ai/user/heaven-ll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and interactive-fiction agents use this skill to present a unified game hub, check or install named child game skills, and route a selected world into a text adventure with independent saves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The launcher may prompt users to add other game skills, and each child skill is a separate trust decision. <br>
Mitigation: Review the requested child skill, publisher, license, and security evidence before installing or running it. <br>
Risk: The release description mentions four game worlds while the included launcher files mostly cover two. <br>
Mitigation: Treat the two-world launcher behavior as the implemented baseline and verify four-world support before relying on the full public description. <br>
Risk: Game saves may contain personal or sensitive roleplay details. <br>
Mitigation: Avoid entering sensitive personal information into game saves and review saved files before sharing a workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heaven-ll/shuangwen-tiyanguan) <br>
- [SKILL.md](SKILL.md) <br>
- [Core logic](references/core_logic.md) <br>
- [Save system](references/save_system.md) <br>
- [UI templates](references/ui_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text prompts with occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces interactive menu text and launcher guidance for separate child game skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
