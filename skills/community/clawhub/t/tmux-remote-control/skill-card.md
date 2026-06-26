## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill when they need an interactive TTY workflow for CLI tools. It helps create named tmux sessions, send commands safely, capture pane output, poll for completion, and clean up managed sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended tmux-controlled agents may run with permission-bypass or full-auto flags and make broad changes without review. <br>
Mitigation: Use those modes only in disposable worktrees or sandboxes, inspect pane output before relying on results, and require human review before applying or shipping changes. <br>
Risk: Commands sent to the wrong tmux target can affect unrelated sessions or processes. <br>
Mitigation: Use the documented oc- session naming convention, inspect sessions and panes before sending input, and attach to or list managed sessions before cleanup. <br>
Risk: Captured pane output can be stale, incomplete, or misleading when used as the only completion signal. <br>
Mitigation: Poll for explicit prompts or expected text, use stale or hard timeouts, and verify the final state in the shell or repository before trusting completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/tmux-remote-control) <br>
- [Publisher profile](https://clawhub.ai/user/BrennerSpear) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [wait-for-text.sh](artifact/scripts/wait-for-text.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and a shell helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on darwin or linux; the helper script polls tmux pane output for regex or fixed-text matches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
