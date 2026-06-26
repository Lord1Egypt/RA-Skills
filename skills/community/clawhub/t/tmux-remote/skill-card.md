## Description: <br>
Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[164149043](https://clawhub.ai/user/164149043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect tmux sessions, send keystrokes to interactive command-line tools, and capture pane output during terminal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can read tmux pane contents, including command output, prompts, and any secrets visible in terminal history. <br>
Mitigation: Use a dedicated low-risk tmux session or socket and avoid running the skill against panes that expose credentials, production access, or sensitive data. <br>
Risk: An agent can send keystrokes to live tmux panes and may execute unintended commands if the wrong target is selected. <br>
Mitigation: Confirm the session, window, and pane target before sending Enter or destructive commands. <br>
Risk: Capturing large pane histories can reveal more context than intended. <br>
Mitigation: Limit captured history to the minimum needed for the workflow and clear panes that contain sensitive output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/164149043/tmux-remote) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux on Linux or macOS; shell helpers can list tmux sessions and poll pane text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
