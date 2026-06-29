## Description: <br>
Installs agent skills from ClawHub, skillhub.cn, skills.sh, Anthropic's skills repository, or a configured self-hosted hub, with source routing, conflict handling, license prompts, and safe archive extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install skills from the hub they name or from a private hub, while preserving clear choices for conflicts, restricted licenses, and custom-hub setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing skills from public, GitHub-backed, or self-hosted hubs can introduce untrusted prompts or code into an agent environment. <br>
Mitigation: Install only from trusted sources, review downloaded skills before relying on them, and scan artifacts before deployment. <br>
Risk: Installer actions can replace local skill directories when the user chooses overwrite, which may discard local modifications. <br>
Mitigation: Read overwrite prompts carefully and back up locally modified skills before replacing them. <br>


## Reference(s): <br>
- [Skill Hub United on ClawHub](https://clawhub.ai/songhonglei/skill-hub-united) <br>
- [ClawHub](https://clawhub.ai) <br>
- [SkillHub](https://skillhub.cn) <br>
- [skills.sh](https://skills.sh) <br>
- [Anthropic Skills documentation](https://docs.claude.com/en/docs/build-with-claude/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and structured status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke installer commands that download and extract skill archives when the user requests an installation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact SKILL.md Version field agrees) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
