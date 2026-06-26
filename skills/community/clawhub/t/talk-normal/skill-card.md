## Description: <br>
talk-normal installs an always-on AGENTS.md prompt that makes agent replies more concise and direct in English and Chinese while preserving useful information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexiecs](https://clawhub.ai/user/hexiecs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install a writing-style prompt into AGENTS.md so future agent responses are shorter, more direct, and less padded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer changes AGENTS.md with an always-on writing-style prompt, which can affect later agent responses in the workspace. <br>
Mitigation: Inspect the resolved AGENTS.md target before installing, and run bash install.sh --uninstall from the skill directory to remove the marked block. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/hexiecs/talk-normal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Installs or removes a marked prompt block in AGENTS.md.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
