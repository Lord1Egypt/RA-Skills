## Description: <br>
Manage tmux sessions using the tmux-manager.py script. Use when asked to create, kill, restart, list, or inspect tmux sessions, send commands to sessions, tail session output, or validate the sessions config file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdeangel](https://clawhub.ai/user/rdeangel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage local tmux-based development environments from YAML configuration, including creating, listing, restarting, killing, inspecting, and validating sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad local shell control through tmux session commands, hooks, panes, environment variables, and AI CLI flags. <br>
Mitigation: Review tmux-sessions.yaml before use, especially pre_hook, post_hook, command, panes, env, and AI CLI flags; use --validate and --dry-run before creating or restarting sessions. <br>
Risk: Destructive tmux actions can terminate managed sessions or, through native tmux commands, all tmux sessions. <br>
Mitigation: Prefer --list or --dry-run before kill or restart actions, scope selectors narrowly, and avoid tmux kill-server unless all tmux sessions should be terminated. <br>
Risk: Tailing panes can expose secrets or untrusted terminal output. <br>
Mitigation: Do not tail panes that may contain secrets or untrusted output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rdeangel/tmux-manager) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local uv and tmux; commands and hooks may execute on the host shell through tmux-manager.py.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
