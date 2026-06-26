# SSH handoff examples

## Example 1: SSH login handoff

Goal: let the human perform an SSH login manually, then let the agent continue in the same remote shell.

Suggested flow:

1. create session `handoff-session`
2. ask the human to attach: `tmux attach -t handoff-session`
3. let the human run the SSH login inside `tmux`
4. capture the pane and confirm the remote prompt is visible
5. continue with the next task through `tmux`

## Example 2: Temporary sudo handoff

Goal: let the human enter a sudo password once, then let the agent perform a few administrative checks in the same shell.

Suggested flow:

1. create session `admin-session`
2. let the human attach
3. let the human run `sudo -s` or a single `sudo` command
4. capture the pane and verify the shell state
5. continue carefully, capturing output after important commands

## Example 3: LAN browser handoff

Goal: let the human open a temporary browser terminal from a trusted machine on the same LAN.

Suggested flow:

1. create or reuse session `handoff-session`
2. launch `start-url-token-web-terminal.sh` with placeholder values replaced by the real server IP and trusted client IP
3. send the printed one-shot URL to the human
4. let the human authenticate inside the browser terminal
5. capture the pane and continue through `tmux`
6. run the cleanup command when done

## Example 4: Recovery when session state is unclear

If the pane suggests nested SSH, `vim`, `less`, `sudo`, a password prompt, or a hung command:

1. capture the pane first
2. avoid sending blind commands
3. if needed send `Ctrl-C`
4. capture again
5. only continue when the state is clear
