## Description: <br>
Cross-pane messaging for tmux using `tmux-bridge` to send messages between panes labeled p1, p2, and p3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkuiwu](https://clawhub.ai/user/mkuiwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple AI agent panes inside tmux, including launching workspaces, listing panes, sending tasks, tracking pending replies, and configuring pane labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a local `tmux-bridge` executable that is not included in the artifact. <br>
Mitigation: Verify the executable source and resolved path before installing or using the skill. <br>
Risk: Other tmux panes may send tasks or receive final results, which can expose sensitive information or misdirect output. <br>
Mitigation: Avoid sharing secrets through pane messages and check `tmux-bridge pending` before replying. <br>
Risk: The documented workflow can kill tmux sessions and append configuration to `~/.tmux.conf`. <br>
Mitigation: Confirm session names before kill commands and review configuration changes before applying them. <br>


## Reference(s): <br>
- [Smux ClawHub release](https://clawhub.ai/mkuiwu/smux) <br>
- [mkuiwu publisher profile](https://clawhub.ai/user/mkuiwu) <br>
- [tmux-bridge reference](references/tmux-bridge.md) <br>
- [tmux reference](references/tmux.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on macOS or Linux and a trusted local tmux-bridge executable.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
