---
name: rockd-remote-control
description: 'Control a remote computer with the RockDesk command line `rds`, by its 9-digit ID: shell, files (copy / sync / mount), screenshots, mouse and keyboard, clipboard, port / serial / USB forwarding, 内网穿透 (VPN). Needs the RockDesk app on both machines: if `rds` is missing, send the user to https://rockdesk.io/#download first. Triggers: "RockDesk", "rds" with a 9-digit ID, "剪贴板历史", "内网穿透", "挂目录", "screenshot the remote", a 9-digit ID plus an action, or any request to operate another machine.'
---

# RockDesk CLI (`rds`) & Agent Skill

> **Needs the RockDesk app on both machines.** Download it at
> https://rockdesk.io/#download (in China: https://rockdesk.cn/#download).

RockDesk is a cross-platform remote-access tool. Its engine, rockd, comes as a
background daemon (`rockd`, also running inside the app), the app, and a
scriptable command line, `rds`, which lets an AI agent drive another machine
headlessly. Every machine has a 9-digit **ID** (shown in the app and by
`rds status`).

`rds` itself never touches the network. It hands each command to the local
rockd daemon. The daemon keeps one encrypted QUIC connection per peer and
reuses it for every later command. That connection goes direct when it can
punch through, and through the server's relay otherwise. The first command to
a peer takes a moment (connect, maybe authorize); the rest are near-instant.
No GUI window opens. Output and error messages are in Chinese.

## First: is RockDesk installed?

**Before your first `rds` command, check that RockDesk is installed and running
on this machine** (`rds status`, see the next section). This skill only teaches
the commands. The work is done by the RockDesk app, which must be installed and
running on **both** machines: this one (where `rds` runs) and every machine you
want to control.

- **Not installed here** (`rds` isn't found and there is no RockDesk app, or
  `rds status` can't reach the background service after starting the app):
  stop and tell the user, in their language, that this needs the RockDesk app
  on this computer and on the one they want to control, and give them the
  download page: **https://rockdesk.io/#download** (in China:
  **https://rockdesk.cn/#download**). There are a Windows installer, Linux
  .deb packages (x86_64: Ubuntu 20.04+, Debian 12+; arm64: Ubuntu 22.04+,
  Debian 12+), macOS .dmg (Apple silicon or Intel) and an Android .apk.
  Direct links that always point to the newest release (in China, use
  rockdesk.cn instead of rockdesk.io in them):
  - Windows: https://rockdesk.io/download/latest/windows (an .exe installer). It
    is not code-signed yet. To install it for the user, download it with
    PowerShell (`Invoke-WebRequest <link> -OutFile $env:TEMP\rockdesk-setup.exe`)
    or curl.exe and run it silently: `(Start-Process $env:TEMP\rockdesk-setup.exe
    -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-'
    -PassThru).WaitForExit()` (not `-Wait`: that also waits for the RockDesk app
    the installer opens at the end, so it never returns). A file downloaded that
    way has no download mark, so SmartScreen does not stop it. It needs
    administrator rights, so the user may have to approve a UAC prompt. If the
    user downloaded it in a browser and Windows says "Windows protected your PC",
    they click "More info", then "Run anyway".
  - macOS, Apple silicon: https://rockdesk.io/download/latest/macos; Intel:
    https://rockdesk.io/download/latest/macos-x86_64 (a .dmg). To install it for
    the user: with Homebrew, `brew tap rockdesk-io/tap && brew install --cask
    rockdesk`; without Homebrew (or in China, where the rockdesk.cn link is
    faster), download the .dmg for this Mac's chip (`uname -m`: arm64 or x86_64)
    as `rockdesk.dmg`, then `hdiutil attach -nobrowse -readonly -mountpoint
    /tmp/rockdesk-dmg rockdesk.dmg && ditto /tmp/rockdesk-dmg/rockd.app
    /Applications/rockd.app && hdiutil detach /tmp/rockdesk-dmg && open
    /Applications/rockd.app`. macOS then asks the user to allow Screen Recording
    and Accessibility for it. By hand: open the .dmg, drag the app into
    Applications and open it once.
  - Linux x86_64: https://rockdesk.io/download/latest/linux-amd64; arm64:
    https://rockdesk.io/download/latest/linux-arm64 (a .deb:
    `curl -fL -o rockdesk.deb https://rockdesk.io/download/latest/linux-amd64 && sudo apt install ./rockdesk.deb`)
  - Android: https://rockdesk.io/download/latest/android (an .apk)

  You may offer to download and install it for them, but ask first. The version
  and release notes are in https://rockdesk.io/rockd-latest.json. New devices
  start with a free trial. The web version at https://rockdesk.io/web/ is for
  people and has no `rds`.
- **On the machine to control:** RockDesk has to be installed there too. The
  user reads its 9-digit ID in the app and decides how you may get in (see
  Authorization below). A Linux machine without a screen:
  `sudo systemctl enable --now rockd`, then `sudo rds otp` prints a one-time
  password.

## Find `rds` and check that it works

`rds` is installed with RockDesk:

- Linux .deb: `/usr/bin/rds`
- Windows: `C:\Program Files\rockd\rds.exe`
- macOS app (1.0.3 and later): `/Applications/rockd.app/Contents/MacOS/rds`
- Source build: `target/release/rds`

- **Check:** `rds status` prints `本机 <name>（…）  ID <ID>  服务器 已连`
  followed by the live connections. If it says `连不上本机的 rockd（…）：后台没起来？`,
  the daemon is not running: start the RockDesk app, or with the .deb run
  `systemctl --user start rockd`. On Windows it is the `rockd` system service.
- Put its path in a variable and always use it: `RDS=/path/to/rds`.
  Everything below is written as `$RDS`.
- **Config dir** (identity, permissions, clipboard history): `~/.config/rockd/`.
  On Windows it is `%APPDATA%\rockd`, or `C:\ProgramData\rockd` for the system
  service; for the Linux system service it is `/var/lib/rockd` (root's `rds`
  finds it, so run `sudo rds …` there). `--dir <dir>` or `$ROCKD_DIR` overrides it.

## For agents (read first)

- **Shell first, GUI second.** Anything doable in a shell, do with
  `$RDS <id> shell -c "…"`: it is faster, deterministic and needs no
  coordinates. Use mouse and keyboard only for GUI-only things.
- **Interactive `$RDS <id> shell` is for humans.** Agents always pass `-c`.
- **One command, one round trip.** Chain logic inside one `shell -c`
  (`cd … && grep … | head`) rather than many calls.
- **GUI work: observe → act → verify.** Take a screenshot to a file, read the
  image, find the pixel, act, then take another screenshot. Never click blind.
- **Permissions come from the peer.** If a command is refused, don't retry in a
  loop. Tell the user what the peer has to allow (see Authorization).
- **Safety.**
  - Only operate machines the user owns or is authorized to control.
  - Before anything destructive or irreversible, say what you will run and get
    confirmation. That includes deleting, overwriting, restarting services,
    sending messages, `sync --delete`, and `clip history rm/clear`.
  - Read-only inspection needs no confirmation.
  - Never type the user's passwords or secrets into remote fields.
  - Clipboard history can hold secrets (passwords, codes, tokens). Don't send
    it to third-party services unless the user asked.

---

## Machine & connection (本机、连接)

```
$RDS status [--json]           This machine's name, ID and server state; LAN peers; every
                               live connection with its paths (direct / LAN / relay, RTT, loss).
$RDS <id> ping                 Connect if needed and measure:
                               "<id>（name）：建连 N ms，往返 N ms，走 <direct|lan|relay> <addr>".
$RDS log [n] [--json]          Connection log: who connected to me, whom I connected to, which
                               services, how long, direct or relayed.
$RDS wake <id|MAC> [--port 9]  Wake-on-LAN magic packet (needs a MAC this machine saw on the LAN).
$RDS login <email> | logout | devices [--json] | account
                               Account (email-code login); devices on the same account; license.
```

`<id>` may also be `IP:port`, `[IPv6]:port` or `host:port` to connect directly
without the server. The peer asks for confirmation or a password the first
time.

## Authorization (谁能连我)

The **peer** decides. There is no per-ID allow list (an ID alone is not proof).
A host offers up to three ways, any combination:

1. **Allow when someone connects.** Someone at the peer clicks "allow"; it
   covers that one connection. `rds` keeps retrying every 2 s while it waits.
2. **One-time password.** Shown on the peer's home page (or `$RDS otp` run on
   the peer); it changes after each use.
3. **Fixed password and / or key pair (either or both):**
   - *Fixed password:* anyone who knows it can connect. Give it with
     `$RDS <id> auth` (prompts once) or `RDS_PASSWORD=… $RDS <id> …`; it is
     remembered (`keys.json`, not plaintext) until the peer changes it.
   - *Key pair (like ssh):* every device holding the same key connects to the
     others without a password. On one device `$RDS key gen`; then
     `$RDS key export` there and `$RDS key import "<that line>"` on each of
     your other devices. A device holding the key signs a challenge bound to
     the connection automatically when refused. (Extra keys or single devices
     can also be listed in the peer's `authorized_keys`, see
     `$RDS authorize`.)

What you can use: everything with the key pair, or when your device is on the
same RockDesk account and proved a password. Otherwise only the features the peer
enabled (`$RDS config` there shows them).

**Machines without a screen** (servers, robots, dev boards; Linux .deb 1.0.10+):

```
sudo systemctl enable --now rockd     # system service: starts at boot, config in /var/lib/rockd
sudo rds status                       # this machine's ID
sudo rds otp                          # its current one-time password (sudo rds otp new: a fresh one)
```

- There, people who come in with the one-time password may also use the
  terminal and port forwarding (file transfer was already on), and "allow when
  someone connects" is off (nobody is there to click).
- Fixed password: `sudo rds passwd` (prompts twice; `--clear` removes it).
- Key pair, like ssh: on your own computer `$RDS key gen` once (later `$RDS key`
  prints the same public line); on the headless machine
  `sudo rds authorize "<that line>"`. Your computer then gets in with no
  password and can use everything.
- What others may use: `sudo rds config` lists it;
  `sudo rds config feature <shell|file|fwd|mount|vpn|serial|usb|…> on|off`
  changes it; `sudo rds config otp off` / `ask on` switch the one-time password
  / the allow dialog.
- With a one-time password, prove it once (`RDS_PASSWORD=… $RDS <id> shell -c …`
  or `$RDS <id> auth`); later commands on the same connection don't need it again.

Setting up a host from the command line (no GUI needed): on a machine without
a screen use the system service above. On a desktop you can also run the
per-user daemon without the app: `systemctl --user enable --now rockd` (plus
`sudo loginctl enable-linger $USER`, so it keeps running after you log out).
The first start writes a default config: the official server, one-time
password on. `$RDS status` shows the ID; `$RDS otp` prints the current
one-time password (`$RDS otp new` makes another). For lasting access:
`$RDS passwd` (fixed password) and / or `$RDS key gen | import | export | clear`
(key pair); both work immediately. `$RDS config` shows / changes the rest
(`ask on|off`, `otp on|off`, `feature <name> on|off`, `name`, `port`,
`term-keep`); `$RDS login <email>`.

A refusal says what is missing (password, a click, a feature that is off).
Don't guess passwords. If you're refused, report which of these is missing.

## Terminal (终端)

```
$RDS <id> shell -c "<command>"
    Run one command in the peer's login shell. Prints stdout+stderr and exits with the remote
    command's exit code, so `&&`, `||` and `if` work like ssh. Piped local stdin is forwarded:
      cat data.csv | $RDS <id> shell -c "wc -l"
    No timeout: a long build runs to the end (wrap with a local `timeout` if you need one).
    Unix peers run it with `$SHELL -lc` (profile sourced: PATH, conda …). Windows peers run it with
    `powershell -NoProfile -NonInteractive -Command`, so use PowerShell syntax there; the exit code
    of a failing external program still comes back.
$RDS <id> spawn "<command>"
    Start a detached process on the peer that outlives the call (servers, long jobs):
      → spawned pid 12345  ·  log: <path of its log file>
$RDS <id> shell                          Interactive TTY for a human (ConPTY on Windows).
$RDS <id> shell --list [--json]          Sessions the peer keeps after a disconnect (30 min by default).
$RDS <id> shell --attach <n>             Reattach to a session (replays what you missed).
$RDS <id> shell --close <n>              Close a session.
```

- **Windows peers running the rockd service** (the installer's default): `shell` and `spawn`
  run inside the service, as SYSTEM in session 0, not in the signed-in user's desktop session.
  A GUI program started there never appears on screen, and `~`, Desktop and `%APPDATA%` are
  SYSTEM's, so use full paths such as `C:\Users\<name>\Desktop`. To open a program or a URL on
  the user's desktop, use the keyboard: `$RDS <id> key win+r`, then
  `$RDS <id> type "msedge https://example.com"`, `$RDS <id> key Return`, and take a screenshot.

## Files (文件)

```
$RDS <id> cp <src> <dst>
    Exactly one side is the peer's, prefixed with ':'.
      upload:   $RDS <id> cp ./a.tgz :/home/u/a.tgz
      download: $RDS <id> cp :/etc/hosts ./hosts
    Folders are copied recursively (scp rules). Re-running an interrupted copy of a file of 8 MB or
    more resumes where it stopped.
$RDS <id> sync [--delete] [--dry-run] <src> <dst>
    One-way folder sync (one side ':'-prefixed). Only missing or changed files go over (size +
    mtime); a second run transfers nothing. --delete removes destination files the source lacks.
$RDS <id> ls [path] [--json]     List a peer directory (default ~).
$RDS <id> send <file>...         Drop files into the peer's Downloads AND put them on its clipboard,
                                 so the person there just pastes. Prints the remote paths; same
                                 names are renamed, not overwritten.
```

`cp` is for one-shot transfers (faster for big files). `mount` is for working
inside the remote tree.

## Mount a remote folder (挂目录)

```
$RDS <id> mount :/remote/dir <local_dir>
    Mount the peer's directory at <local_dir>, read-write. Tools, editors and builds see an
    ordinary folder.
    On Windows <local_dir> may be a drive letter: `Z:`, or `*:` for any free one.
$RDS [<id>] umount <local_dir>    Unmount (only what you mounted — the user may be using theirs).
$RDS mount [--json]               What this machine has mounted.
```

- Clients: Linux kernel FUSE (the mount point can't be on NTFS); macOS needs
  nothing (rockd serves the folder to the system's NFS client on 127.0.0.1);
  Windows uses Dokany, which the RockDesk installer includes.
- The peer must allow `mount`.
- All mounts to one peer share its single connection.

## Clipboard (剪贴板)

```
$RDS <id> clip                       Print the peer's clipboard text. If it holds an image, the image
                                     is saved as rockd-clip-<time>.png (RDS_CLIP_OUT=<file> to choose).
$RDS <id> clip set "<text>"          Put text on the peer's clipboard (no text: read it from stdin).
$RDS <id> clip set --image a.png     Put an image on it.
$RDS <id> clip sync                  Keep both clipboards in sync until Ctrl-C (for humans).
```

Alternative spellings also work: `clipboard get | set <text> |
get-image [file] | set-image <file>`.

## Clipboard history (剪贴板历史)

What the daemon records:

- **What counts as an entry.** Each copy is one entry, text or image, newest
  first. Copying the same content again moves it to the top instead of adding
  a new entry.
- **Where it came from.** Every entry notes whether it was received from a peer
  and which peers it was sent to.
- **Limits.** Up to 300 entries; images 200 MB in total; text 1 MB per entry.
- **Storage.** It stays on that machine, in `clip_history/` under the config
  dir.
- **Phones** don't record their own clipboard.
- **Recording can be off.** Then nothing new is recorded, and what was copied
  while it was off isn't added later.

Without `<id>` a command works on **this machine's** history. With `<id>` it
works on the **peer's** history; the peer must allow `clip`. An older peer
answers that it has no history yet.

```
$RDS [<id>] clip history [-n N]        List the newest N (default 100):
                                       "#<n>  time  文字/图片 size  从 X 收到 / 发给过 Y",
                                       then the first 100 characters.
$RDS [<id>] clip history --json [-n N] Same, as JSON, with the full text of every entry
                                       (agents: prefer this). Fields: id, t (Unix ms), kind
                                       (text|image), text, truncated, w, h, bytes, from, from_name,
                                       sent_to, sent_to_names, thumb (base64 PNG, images only).
$RDS [<id>] clip history --md          Export everything as Markdown for an LLM.
$RDS [<id>] clip history list <n>... --md
                                       Export just those entries.
$RDS [<id>] clip history show <n> [-o file]
                                       One entry in full: text to stdout (or into a file); an
                                       image needs -o file.png.
$RDS [<id>] clip history rm <n>...     Delete entries.          (confirm first)
$RDS [<id>] clip history clear         Delete all.              (confirm first)
$RDS clip history copy <n>             Put this machine's entry back on this machine's clipboard.
$RDS clip history on | off             Start / stop recording on this machine.
$RDS <id> clip history send <n>        Put entry <n> of THIS machine's history on the peer's clipboard.
$RDS <id> clip history take <n>        Put the peer's entry <n> on this machine's clipboard.
$RDS <id> clip history restore <n>     Put the peer's entry <n> back on the peer's own clipboard.
```

What the `--md` export contains:

- A short instruction block at the top, asking the model to drop duplicates and
  noise, group entries by topic, format them, and end with a summary of what
  the user was doing and what needs follow-up.
- Every entry in order: time, source, and the text in a fenced block. Images
  appear as a size line only.
- At most 2 MB.

When the user asks you to "整理 / 总结剪贴板", export, read the file, and do
what the header says. Write the result for the user and don't paste raw
secrets back.

## Screen, mouse, keyboard (屏幕、鼠标、键盘)

```
$RDS <id> info                                     Displays: index, W×H, position, name, primary/default.
$RDS <id> screenshot [-o f.png] [-d n] [-R x,y,w,h] Save a PNG (default rds-shot-<time>.png); prints
                                                   the path and size. Then read the image.
$RDS <id> click X Y [--right] [--double] [-d n]    Click at pixel X,Y from the display's top-left.
$RDS <id> move X Y [-d n]
$RDS <id> type "<text>"                            Type into the focused field (click it first). Any Unicode.
$RDS <id> key <combo>                              A key or chord, e.g. Return, Escape, ctrl+c, cmd+s, alt+F4.
$RDS <id> scroll DX DY                             Wheel notches; DY > 0 scrolls down.
$RDS <id> desktop [--view-only] [--display :0] [--no-open]
                                                   Open the peer's desktop in a local browser page (prints
                                                   its URL). This is for humans.
```

- **`-d`** picks a display by its `info` index or name. Coordinates are then
  counted from that display's top-left.
- **`key` names:**
  - Return/Enter, Tab, Escape, Backspace, Delete, Space.
  - Up, Down, Left, Right, Home, End, PageUp, PageDown, Insert.
  - F1–F24, and single letters and digits.
  - Modifiers: `ctrl+`, `shift+`, `alt+`/`option+`, and `cmd+`/`win+`/`super+`
    (⌘ on macOS, the Windows key on Windows).
- **Android peers:**
  - The RockDesk app must have its accessibility service ("被远程点屏幕") turned
    on. `info` says whether it is.
  - A right click is a long press.
  - `type` fills the focused input box.
  - `key` also takes back / home / recents.

## Port forwarding (端口转发)

```
$RDS <id> forward <local>:[<host>:]<port>
    Listen on 127.0.0.1:<local> and tunnel each connection to <host>:<port> as seen from the peer.
    <host> defaults to the peer itself and is resolved there, so peer-only hostnames work.
      $RDS <id> forward 15432:db.internal:5432
    Returns immediately: the daemon holds the listener until `unforward` or until rockd stops.
$RDS <id> forward              List running forwards.
$RDS <id> unforward <local>    Stop one.
```

The peer must allow `fwd`.

## VPN / 内网穿透

```
$RDS <id> vpn up [--route <cidr>]...   A virtual NIC on each side: this machine 10.77.0.2, the peer
                                       10.77.0.1. --route also sends those subnets (e.g. the peer's
                                       LAN) through it.
$RDS <id> vpn up --exit [--bypass <cidr>]...
                                       Use the peer as the internet exit: this machine's traffic
                                       goes out through the peer (the peer must allow `exit`).
                                       Linux: the LAN, connections coming into this machine (ssh)
                                       and --bypass networks stay off the tunnel; DNS goes to the
                                       peer when systemd-resolved is running.
$RDS <id> vpn down
```

- The peer must allow `vpn`.
- Without root, Linux and macOS need the rockd helper to create the NIC. It is
  installed from the app's settings. `--exit` on Linux needs the current helper
  (protocol 3); an older one is reported as old, with how to update it.
- In the Chinese UI this feature is called 内网穿透.

## Serial ports & USB (串口、USB)

```
$RDS <id> serial list [--json]                 The peer's serial ports.
$RDS <id> serial <port> [baud] [--local <path>] A local virtual serial port wired to the peer's
                                               port (default 115200 8N1); prints the local path.
                                               Baud changes made by the local program follow over.
$RDS serial | serial list | unserial <local path>
                                               Running forwards / this machine's ports / stop one.
$RDS <id> usb list [--json]                    The peer's USB devices (with busid).
$RDS <id> usb attach <busid>                   Attach one here (USB/IP).
$RDS <id> usb install                          Windows peer: install its USB share driver (usbipd-win)
                                               so its devices can be attached elsewhere.
$RDS usb | usb list | usb detach <n|busid> | usb install
                                               Attached devices / this machine's devices / detach /
                                               install this machine's USB drivers (Windows).
```

- The local end of a serial forward must be Linux or macOS.
- USB works between Linux and Windows, in both directions (e.g. a dongle on a Linux box used
  by Windows-only software). Linux needs the rockd helper (or the rockd system service).
  Windows installs the open-source usbip-win2 driver the first time it attaches a device; to
  share a Windows machine's own devices, run `usb install` on it first (or `$RDS <id> usb
  install` remotely). macOS is not supported (the OS does not allow it).
- The peer must allow `serial` or `usb`.

## Recipes

- **Is the peer reachable, and on which path?** `$RDS <id> ping`
- **Inspect a server:** `$RDS <id> shell -c "uname -a; uptime; df -h /; free -h"`
- **Fetch a log:** `$RDS <id> cp :/var/log/syslog ./syslog`
- **Run something long:** `$RDS <id> spawn "cd ~/proj && make -j8"`, then
  `$RDS <id> shell -c "tail -20 <log>"`.
- **Summarize what the user copied on another machine:**
  `$RDS <id> clip history --md > clip.md`, then read `clip.md` and summarize.
- **Re-send an older clipboard item:** run `$RDS clip history`, find `#n`, then
  `$RDS <id> clip history send n`.
- **Get a screenshot of the peer:** `$RDS <id> screenshot -o shot.png`, then
  read `shot.png`.

## Installing this skill, or using MCP instead

**Install this skill:** save this file unchanged as `SKILL.md` in a folder named
`rockd-remote-control` inside your agent's skills folder:

- Claude Code: `~/.claude/skills/rockd-remote-control/SKILL.md`
- Gemini CLI: `~/.gemini/skills/rockd-remote-control/SKILL.md`
- DeepSeek Harness (`dsh`), Codex and other agents that read the shared folder:
  `~/.agents/skills/rockd-remote-control/SKILL.md` (Windows:
  `%USERPROFILE%\.agents\skills\rockd-remote-control\SKILL.md`). dsh does not
  read `~/.claude/skills`.

**Right after installing the skill, check RockDesk itself** (see "First: is RockDesk
installed?" at the top): if `rds` is not there yet, tell the user the skill needs the
RockDesk app on both machines and give them https://rockdesk.io/#download (in China:
https://rockdesk.cn/#download). Without RockDesk the skill can do nothing.

**Or connect it as an MCP server:** `rds mcp` (1.0.3 and later) is an MCP server over
stdio with the same abilities as tools: `status`, `devices`, `ping`, `shell`, `spawn`,
`ls`, `copy`, `info`, `screenshot`, `click`, `move`, `scroll`, `type_text`, `key`,
`clipboard_get`, `clipboard_set`, `forward`, `unforward`. Screenshots come back as
images (long edge ≤ 1280 px) and click coordinates are read off the latest
screenshot. When the MCP tools are available, use them; this document still
explains what each one does.

- Claude Code: `claude mcp add -s user rockdesk -- rds mcp`
- Codex: `codex mcp add rockdesk -- rds mcp`
- Gemini CLI, Cursor, Claude Desktop and other MCP clients: an stdio server whose
  command is `rds` and args `["mcp"]`, e.g.
  `{"mcpServers": {"rockdesk": {"command": "rds", "args": ["mcp"]}}}`
- `rds` is not on the PATH on macOS and Windows: use
  `/Applications/rockd.app/Contents/MacOS/rds` or `C:\Program Files\rockd\rds.exe`.
- `npx -y rockdesk-mcp` (npm) or `uvx rockdesk-mcp` (PyPI) start the same server and find
  `rds` on every system by themselves. If RockDesk is not installed yet, they serve an
  `install_rockdesk` tool instead: once the user agrees, it installs RockDesk and loads
  the RockDesk tools.
