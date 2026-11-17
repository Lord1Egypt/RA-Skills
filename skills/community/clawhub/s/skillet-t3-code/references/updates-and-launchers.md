# Updates, Launchers, and Local Automation

Use this reference when T3 shows an update banner, a wrapper launches the wrong build, or desktop and headless components drift apart.

## Official sources and release channels

Use these upstream locations:

- Product website: <https://t3.codes>
- Official desktop download and release landing page: <https://t3.codes/download>
- Source repository: <https://github.com/pingdotgg/t3code>
- Latest stable GitHub release: <https://github.com/pingdotgg/t3code/releases/latest>
- Stable and nightly desktop releases: <https://github.com/pingdotgg/t3code/releases>
- Published CLI package: <https://www.npmjs.com/package/t3>

The official download page links the current Windows, macOS, and Linux desktop installers. If it sends the user to GitHub Releases, select the newest non-pre-release asset for the operating system and architecture. The GitHub releases page also contains development builds. Nightly release titles begin with `T3 Code Nightly` and are marked `Pre-release`.

Do not hardcode a nightly tag in a reusable launcher or runbook. Inspect the current npm channels at runtime:

```bash
npm view t3 dist-tags --json
```

Use the stable CLI without installing it globally:

```bash
npx t3@latest --version
npx t3@latest
```

For an unattended stable headless server, make the server subcommand explicit:

```bash
npx --yes t3@latest serve --host 127.0.0.1
```

Replace loopback only after choosing and reviewing the direct Tailnet or Tailscale Serve transport in `remote-tailscale.md`.

Use the current nightly only when the user explicitly chooses the development channel:

```bash
npx t3@nightly --version
npx t3@nightly
```

The development-channel equivalent for a headless server is:

```bash
npx --yes t3@nightly serve --host 127.0.0.1
```

Do not put the nightly command into an existing stable service until the user accepts the development-channel risk and a rollback path exists.

With GitHub CLI installed, print the newest GitHub pre-release without relying on a hardcoded nightly tag:

```bash
gh api repos/pingdotgg/t3code/releases \
  --jq 'map(select(.prerelease))[0] | {name, tag_name, html_url}'
```

For a specific client and server version match, use the exact version shown by the client:

```bash
npx "t3@<client-version>" --version
```

On the GitHub releases page, verify the release title, tag, pre-release status, operating system, and architecture before downloading an asset. Nightly builds can break compatibility or state. Keep the controller and remote servers on matching versions and retain the previous working artifact when rollback matters.

### Official desktop package commands

The upstream repository documents these package-manager commands:

```powershell
winget install T3Tools.T3Code
```

```bash
brew install --cask t3-code
yay -S t3code-bin
```

The website download page remains the source for the Windows installer, macOS disk images, and Linux AppImage when a package manager is not used.

## Identify the install source

Before updating, record:

```bash
command -v t3
t3 --version
readlink -f "$(command -v t3)"
```

For the desktop application, inspect the launcher or desktop entry to determine whether it runs an AppImage, package-manager installation, source checkout, or another channel.

Do not run an npm, package-manager, or AppImage update command until the current source and channel are known. Two installations can coexist and make an update appear ineffective.

## Separate components

Check these independently:

- Desktop application build.
- T3 CLI used in the shell.
- Headless server executable used by a service.
- Wrapper or symlink that selects a version.

An update banner may refer to one component while another is already current.

## Durable local layout

Keep local integration outside release artifacts:

- Versioned application files: `~/.local/opt/t3-code/` or another user-owned application directory.
- Stable launcher or symlink: `~/.local/bin/`.
- Local assets: `~/.local/share/t3-code/`.
- User services and timers: `~/.config/systemd/user/`.

A launcher should select one explicit installation and fail clearly when it is missing. Avoid scanning arbitrary downloads on every launch.

## Update sequence

1. Record the current version and executable target.
2. Download or install through the same trusted channel.
3. Verify the new artifact before changing the stable launcher.
4. Switch the wrapper or symlink atomically.
5. Relaunch the desktop application or restart the user service.
6. Confirm the reported version and the executable path after restart.
7. Keep or remove the previous artifact according to the user's rollback policy.

Do not modify a generated bundle to make a durable fix. Put compatibility flags, environment variables, and path selection in the local wrapper.

## User timer pattern

Automated updates are optional. If the user asks for them, use a user service and timer that call a reviewed local updater. Do not embed credentials in the unit. Use randomized delay and retain logs for diagnosis.

After changing units:

```bash
systemctl --user daemon-reload
systemctl --user enable --now t3-update.timer
systemctl --user list-timers --all | grep t3
journalctl --user -u t3-update.service -n 100 --no-pager
```

## Verification

- `command -v t3` and `readlink -f` point to the intended installation.
- `t3 --version` reports the expected build.
- The desktop launcher starts the intended desktop artifact.
- The headless service uses the intended executable.
- Project state remains under the intended base directory.
- A failed update leaves the previous working version available when rollback was requested.
