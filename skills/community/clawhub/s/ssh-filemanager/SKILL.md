---
name: tailnet_ssh_file_manager
description: Manage files on remote machines over Tailscale SSH (Tailnet). Use this skill when the user needs to list, read, write, delete, move, copy, search, chmod, push, or pull files on a remote OpenClaw node via a Tailscale SSH connection. Always prefer scp for files larger than 3KB to avoid the OpenClaw invoke payload limit.
---

# Tailnet SSH File Manager

## Overview
This skill enables file management between the OpenClaw Gateway and remote OpenClaw Nodes through **Tailscale SSH** (Tailnet). It wraps system `ssh`, `scp`, and `sftp` commands via the helper script `scripts/ssh_file_manager.py`.

## Pre-requisites
1. The local machine (Gateway) must be connected to the same **Tailnet** as the target node.
2. **Tailscale SSH** must be enabled on the target node and allowed by Tailscale ACLs.
3. The target node must be reachable via its **Tailscale IP** or **MagicDNS hostname** (e.g. `node-name.tailXXXX.ts.net`).

## Workflow
1. Determine the remote node's Tailscale identifier (`host`). Ask the user if it is ambiguous.
2. Determine the requested operation (`action`) and the relevant `path`(s).
3. **File size check**:
   - If reading/writing text content and the estimated size is **< 3KB**, you may use `read` or `write` with inline content.
   - If the file is **>= 3KB**, or if transferring binary files, **always** use `push` (local -> remote) or `pull` (remote -> local) via `scp`.
4. Run the helper script:
   ```bash
   python3 {baseDir}/scripts/ssh_file_manager.py <action> --host <host> [args...]
   ```
5. Parse the JSON output and present results to the user. If `success` is `false`, surface the `error` message.

## Supported Actions
| Action | Description | Command Example |
|---|---|---|
| `list` | List directory entries with size, mode, and mtime. | `python3 {baseDir}/scripts/ssh_file_manager.py list --host node.tailXXXX.ts.net --path /home/user` |
| `read` | Read a remote file as text or base64. | `python3 {baseDir}/scripts/ssh_file_manager.py read --host node.tailXXXX.ts.net --path /home/user/file.txt` |
| `write` | Write text or base64 content to a remote file. | `python3 {baseDir}/scripts/ssh_file_manager.py write --host node.tailXXXX.ts.net --path /home/user/file.txt --content "Hello"` |
| `delete` | Delete a remote file or directory recursively. | `python3 {baseDir}/scripts/ssh_file_manager.py delete --host node.tailXXXX.ts.net --path /home/user/old.txt` |
| `move` | Move/rename a remote file or directory. | `python3 {baseDir}/scripts/ssh_file_manager.py move --host node.tailXXXX.ts.net --src /tmp/a --dst /tmp/b` |
| `copy` | Copy a remote file or directory recursively. | `python3 {baseDir}/scripts/ssh_file_manager.py copy --host node.tailXXXX.ts.net --src /tmp/a --dst /tmp/b` |
| `stat` | Get file metadata (size, mode, uid, gid, mtime, is_dir). | `python3 {baseDir}/scripts/ssh_file_manager.py stat --host node.tailXXXX.ts.net --path /home/user/file.txt` |
| `find` | Search for files by name pattern under a path. | `python3 {baseDir}/scripts/ssh_file_manager.py find --host node.tailXXXX.ts.net --path /home/user --name "*.log"` |
| `chmod` | Change file permissions. | `python3 {baseDir}/scripts/ssh_file_manager.py chmod --host node.tailXXXX.ts.net --path /home/user/script.sh --mode 755` |
| `push` | Copy a local file to the remote node via scp. | `python3 {baseDir}/scripts/ssh_file_manager.py push --host node.tailXXXX.ts.net --local /tmp/local.bin --remote /tmp/remote.bin` |
| `pull` | Copy a remote file to the local machine via scp. | `python3 {baseDir}/scripts/ssh_file_manager.py pull --host node.tailXXXX.ts.net --remote /tmp/remote.bin --local /tmp/local.bin` |

## Safety Rules
- **Destructive operations** (`write`, `delete`, `move`, `chmod`): Always ask the user for explicit confirmation before invoking the script.
- **Payload limit**: Do not attempt to inline base64-encode files larger than 3KB through OpenClaw's `node.invoke`. Use `push`/`pull` (scp) instead.
- **Path sanitization**: Do not traverse above `/` unless explicitly requested. Verify absolute paths when provided by the user.
- **Connection check**: If a command fails with a connection error, you may first run `python3 {baseDir}/scripts/ssh_tunnel.py check --host <host>` to verify Tailscale SSH reachability.

## Edge Cases
- **Target host offline or not in the tailnet** -> connection timeout. Run `ssh_tunnel.py check` to diagnose.
- **Permission denied** -> user lacks SSH/ACL access or file permissions on the remote node.
- **Remote path does not exist** -> script returns `success: false` with details.
- **Binary file read** -> use `read` with `--format base64`.
- **Remote node missing Python 3** -> `list` and `stat` may fail; fallback to raw `ssh` commands if needed.
