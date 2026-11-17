# Multi-Machine T3 Code Setup

Use this reference when one controller desktop or mobile client should manage projects on two or more machines.

## Prerequisites

Before this workflow starts:

- Install T3 from a trusted source on the controller and every remote host.
- Install and authenticate Tailscale on hosts that use Tailnet transport.
- Prepare one repository checkout per machine. Git synchronization and concurrent-edit policy stay outside this skill.
- Confirm the controller has the T3 desktop or mobile environment interface used by the installed build.
- Confirm an authorized, noninteractive SSH route exists before choosing the SSH tunnel fallback.

## 1. Draw the topology

Record these roles before installing services:

- Controller: the desktop or mobile client where environments are selected.
- Local workspace: projects that run on the controller itself.
- Remote host: each machine that runs `t3 serve` near its own repositories and tools.
- Transport: direct Tailnet HTTP, Tailscale Serve HTTPS, or a local-only SSH forward.

Give each environment a distinct label such as `Build host (Server A)`. Assign a unique controller-side port to every SSH tunnel.

## 2. Align the installations

On the controller and every remote host:

```bash
command -v t3
t3 --version
t3 serve --help
```

Use compatible T3 versions when possible. Record the desktop build separately from the CLI and headless server versions.

## 3. Prepare each remote host

For every remote:

1. Confirm T3 can open the intended repositories locally.
2. Confirm Tailscale is connected when Tailnet transport is planned.
3. Choose one transport from the next section.
4. Run `t3 serve` interactively once and inspect its pairing details and logs.
5. Convert the working command into the target operating system's user service or scheduled task.
6. Test the exact URL from the controller before saving the environment.

Repeat the full loop for one host at a time. Do not configure several remotes with the same label, port, or copied state directory.

On Linux, use a user service and verify whether it must survive logout:

```bash
loginctl show-user "$USER" -p Linger
```

If the result is `Linger=no` and the service must survive logout, get explicit operator approval before running:

```bash
sudo loginctl enable-linger "$USER"
loginctl show-user "$USER" -p Linger
```

Run the command on each Linux machine whose user services need logout persistence, including the controller when it owns a tunnel service.

For Windows remotes, follow `windows-remote.md`. It covers the PowerShell launcher, current-user Scheduled Task, Tailscale and firewall checks, SSH fallback prerequisites, restart verification, and safe cleanup of an orphaned T3 child process.

## 4. Choose the transport per host

### Direct Tailnet binding

Use this when the controller can reach the remote T3 TCP port over the Tailnet. Follow `remote-tailscale.md` and bind the remote server to `tailscale ip -4`.

A successful `tailscale ping` is not enough. Test the T3 URL from the controller.

### Tailscale Serve

Use this when the user wants a Tailnet HTTPS URL and the installed T3 build supports `--tailscale-serve`. Bind T3 to loopback and verify the published route with `tailscale serve status`.

### Local-only SSH forward

Use this when direct T3 TCP is blocked but an authorized SSH route to the remote host works. Run T3 on remote loopback:

```bash
t3 serve --no-browser --host 127.0.0.1 --port 3773 --base-dir "$HOME/.t3"
```

### Remote loopback service

After the interactive command works, pin the absolute T3 executable reported by `readlink -f "$(command -v t3)"` in a remote user service:

```ini
[Unit]
Description=T3 Code loopback server
After=network-online.target

[Service]
Type=simple
ExecStart=/absolute/path/to/t3 serve --no-browser --host 127.0.0.1 --port 3773 --base-dir=%h/.t3
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Enable it and verify the remote listener before opening the controller tunnel:

```bash
systemctl --user daemon-reload
systemctl --user enable --now t3-code.service
systemctl --user status t3-code.service --no-pager
ss -ltn 'sport = :3773'
```

On the controller, verify noninteractive SSH and choose a free local port:

```bash
ssh -o BatchMode=yes remote-host true
ss -ltn 'sport = :3775'
```

If the SSH check fails, stop and fix the authorized SSH route or choose another transport. The port check should return no listener before the tunnel starts. Do not disable SSH host-key checking to make a service start.

Start the tunnel in the foreground first:

```bash
ssh -NT \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -L 127.0.0.1:3775:127.0.0.1:3773 \
  remote-host
```

The controller then connects to `http://127.0.0.1:3775`. Choose another local port for a second remote. The SSH route may itself use Tailscale or another approved private path.

A tunnel is a fallback, not proof that the Tailnet policy is correct. Diagnose ACL, firewall, VPN, and routing behavior separately.

## 5. Persist the SSH tunnel

After the foreground tunnel and T3 URL work, create a controller-side user service. Example:

```ini
[Unit]
Description=T3 Code tunnel to remote host
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/ssh -NT -o BatchMode=yes -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -L 127.0.0.1:3775:127.0.0.1:3773 remote-host
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Then:

```bash
systemctl --user daemon-reload
systemctl --user enable --now t3-code-tunnel-remote.service
systemctl --user status t3-code-tunnel-remote.service --no-pager
journalctl --user -u t3-code-tunnel-remote.service -n 100 --no-pager
```

Use one service name and local port per remote. Verify the service after logout or reboot when persistence is required.

## 6. Save and pair each environment

For each working remote URL:

1. Start the remote server and obtain the current pairing details from the installed T3 build.
2. In the controller, add the backend URL and pairing value in their separate fields.
3. Use a host-qualified environment name.
4. Confirm the environment opens a project from the intended remote filesystem.
5. Confirm one-time pairing material is consumed or revoked according to the installed build's behavior.

Do not paste full URLs into fields that expect only a host. Do not reuse pairing values across hosts.
Treat terminal output, screenshots, and journal entries that contain pairing material as sensitive until the value is consumed or revoked.

## 7. Register projects on the correct host

Run `t3 project add` on the machine that owns the workspace path. Use host-qualified titles when the same Git repository exists on several hosts:

```bash
t3 project add --base-dir "$HOME/.t3" --title "Example (Server A)" /path/to/repository
```

The workspace root must be valid on that host. A controller-side path does not identify a remote workspace.

## 8. Verify the matrix

Check every row, not only the first remote:

- Controller label maps to the intended host.
- T3 version and executable are the intended ones.
- Headless service or scheduled task survives logout and restart as designed.
- Bind address is loopback or Tailnet-only unless public exposure was explicitly approved.
- The controller can reach the exact saved URL.
- The selected project title and workspace root belong to that host.
- Local tunnel ports are unique and listen only on `127.0.0.1`.
- Logs contain no repeated pairing or connection failures.

Direct Tailnet mode uses an HTTP application URL over Tailscale's encrypted transport. Tailscale Serve is the option when the user needs a Tailnet HTTPS URL.

## Boundaries

- This workflow does not install T3, clone or synchronize repositories, write Tailnet ACL policy, or configure SSH keys.
- Exact desktop UI labels and pairing lifetimes depend on the installed T3 build. Use the fields and output shown by that build.
- A working Tailnet route does not replace T3 authentication or pairing.
- A working SSH tunnel does not prove that direct Tailnet policy is correct.

## Failure patterns

- Tailnet ping works, T3 URL fails: test the TCP port, then inspect Tailnet policy, host firewall, VPN, and the server bind address.
- URL works in a shell, desktop opens the wrong host: inspect the saved backend and logical project key.
- Tunnel starts but T3 is unreachable: confirm remote T3 is listening on the address and port named on the right side of `-L`.
- Tunnel service loops on restart: run the same SSH command with `BatchMode=yes` in a terminal and fix host-key, key, or forwarding errors before restarting the service.
- One remote replaces another: give each saved environment a unique name and each tunnel a unique local port.
