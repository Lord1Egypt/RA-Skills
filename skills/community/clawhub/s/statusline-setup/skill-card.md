## Description: <br>
Use when the user wants to configure Claude Code statusline UI by inspecting shell prompt configuration and updating the relevant settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to inspect shell prompt context, read current Claude settings, and make minimal statusline-related configuration updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect shell prompt configuration and edit Claude Code settings, which could expose unrelated secrets or alter unrelated preferences. <br>
Mitigation: Tell the agent which shell prompt file or prompt text to inspect, ask it to show the Claude settings change before applying it, and avoid broad scanning of dotfiles. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wimi321/statusline-setup) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance] <br>
**Output Format:** [Markdown guidance with proposed settings changes and refinement notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include shell commands or settings snippets when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
