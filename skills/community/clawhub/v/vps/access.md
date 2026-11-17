# Access — SSH, Keys, and Getting Back In

Read when SSH fails, before any change to sshd or the firewall, and when setting up access for a second person. The single rule that prevents most of this file: **never change the way in from the only session you have** (SKILL.md Rule 1).

**Before touching access on a specific host**, read its row in `## Hosts` in `memory.md` and check `## Boxes` for a recovery runbook naming that host — a previous lockout usually left the answer written down.

**Contents:** [Classify the Failure First](#classify-the-failure-first) · [Refused](#refused) · [Timed Out](#timed-out) · [Permission Denied](#permission-denied) · [Locked Out Completely](#locked-out-completely) · [Rescue Mode](#rescue-mode) · [Keys](#keys) · [Hardening sshd](#hardening-sshd) · [More Than One Person](#more-than-one-person) · [Jump Hosts and Bastions](#jump-hosts-and-bastions) · [When Fail2ban Bans You](#when-fail2ban-bans-you)

## Classify the Failure First

Three failure shapes, three different subsystems. Guessing wastes the time you have.

| What you see | What it means | Look at |
|---|---|---|
| `Connection refused` | A packet reached the host and nothing was listening on that port | sshd running? bound to which port and address? |
| `Connection timed out` / hangs | Nothing answered at all | Provider firewall, host firewall, network, or the box is down |
| `Permission denied (publickey)` | You reached the right daemon; it rejected the credential | Key, username, file permissions, sshd config |
| `Host key verification failed` | The host key changed | A rebuild, a restore, an address reused for a different machine — or, rarely, interception |
| Connects then hangs before the prompt | Usually reverse-DNS lookup or a slow login script, not the network | sshd DNS setting, then the shell profile |

## Refused

- sshd is not running, or it is listening on a different port than you are dialing. Get in through the console and check both.
- If sshd is bound only to a private address or to IPv6, the public IPv4 dial refuses. This is a common outcome of a copy-pasted hardening guide.
- On a box that just rebooted, sshd may have failed to start because of a syntax error in the configuration — the daemon validates on start and refuses to come up. The console shows the reason immediately.
- If the disk is full, sshd can fail to start or fail to accept sessions. Check filesystem usage before assuming a network problem (`operations.md`).

## Timed Out

Walk the layers outward, in this order, because each one is invisible from the layer below:

1. **Provider firewall.** Invisible from inside the box. Check it in the console first — a rule added weeks ago for a different purpose is a common cause.
2. **Host firewall.** A default-deny policy enabled before the SSH allow rule locks you out instantly.
3. **The machine.** Is it running? Does the console respond?
4. **The network path.** Provider status page, then whether the address responds to anything at all.
5. **Your side.** A corporate network or a hotel blocking a nonstandard SSH port is a real cause and looks exactly like a server problem. Test from a second network before changing anything on the server.

## Permission Denied

- **Username.** `root` is disabled on many images by default and should be disabled on all of them; the admin user is the one with the key.
- **Which key.** If several keys are loaded, the daemon may try the wrong ones and hit the attempt limit before reaching yours. Specify the identity explicitly to test.
- **Permissions on disk.** The daemon refuses keys in a home directory or `.ssh` directory that is group- or world-writable, and says almost nothing about it in the client output. Home not writable by group or others, `.ssh` at 700, `authorized_keys` at 600, all owned by the user.
- **Verbose client output names the failing step**, and the daemon's log names the reason. Read the server side: the client only ever says "denied".
- **The key was added to the wrong user.** Copying to root's `authorized_keys` and logging in as the admin user is the classic version.
- **SELinux** on RHEL-family images blocks reads of `authorized_keys` after a manual file copy that lost its context. Symptom: perfect-looking permissions and a denial anyway.

## Locked Out Completely

Order matters, and the irreversible option is last:

1. **Web console.** A keyboard on the running machine. Fixes sshd, firewall rules, and a wrong port. Requires that the machine is running and that you know a local password — which is why the admin user should have one set even in a key-only setup, stored as a pointer (`1password:Infra/<host>-local`), never in `~/Clawic/data/`.
2. **Rescue mode.** Fixes anything that stops the machine from booting or that requires the disk to be unmounted.
3. **Attach the disk to another server**, where the provider supports it. Same effect as rescue mode with more steps.
4. **Restore a snapshot to a new machine.** Loses everything since the snapshot. Fine when the box is cattle, expensive when it is a pet.
5. **Rebuild.** Irreversible, and the button sits next to the one you actually want.

If none of the first four are available, the real finding is that Rule 1 was never satisfied on this host — record that in `## Hosts` and fix it before the next change.

## Rescue Mode

The rescue system boots a temporary OS with your disk present but not in use. The workflow is always the same, whatever the provider calls it:

1. Enable rescue mode in the console, then reboot into it. Some providers give a one-time root password at this point — that password is a secret and is stored as a pointer, never written into a file under `~/Clawic/data/`.
2. Identify the disk and its partitions, mount the root filesystem, and — if you need working package tools, network resolution, or a bootloader repair — bind the system directories and chroot into it.
3. Make the fix. The four that account for most rescue sessions: a bad `/etc/fstab` entry stopping boot (add `nofail` to non-root mounts), a full root filesystem, a broken sshd configuration, a mistaken firewall policy.
4. Exit, unmount cleanly, disable rescue mode, reboot into the normal system.

The trap: disabling rescue mode and rebooting are two separate actions on most providers, and forgetting the first means the box boots back into rescue and looks broken again.

## Keys

- **Ed25519** by default: short, fast, and universally supported by anything current. RSA at 4096 bits only where an old system requires it.
- **Passphrase on every private key**, held by an agent. A key file without a passphrase is a password lying in a file.
- **One key per human, not one key per server.** Revoking a person's access must be one action, and shared keys make it impossible to know who did what.
- **Never copy a private key to a server.** If a server needs to reach another server, that is a purpose-scoped key generated on that server, or agent forwarding limited to the session that needs it — and agent forwarding to a host you do not fully trust exposes your agent to whoever has root there.
- **Rotation** matters less than revocation. Removing a key from `authorized_keys` on every host is the operation to keep cheap — which is an argument for configuration management, not for a spreadsheet.
- **Certificates instead of keys** are the right answer above roughly ten people or fifty hosts: short-lived, centrally issued, expire on their own. Below that scale the operational cost exceeds the benefit.
- Keys live in the user's own store. This skill records only a pointer (`file:~/.ssh/id_ed25519`) in `servers.md`.

## Hardening sshd

The list is short and the order is what matters. Each change is proven from a second session before the first is closed.

| Setting | Why | Note |
|---|---|---|
| Password authentication off | Ends every brute-force attempt at once | The single highest-value change |
| Root login off | Forces named accounts and an audit trail | Set the admin user up first |
| Key-only, published algorithms current | Removes legacy ciphers | Distribution defaults are already reasonable; do not paste a cipher list from an old article |
| Login grace and max auth tries reduced | Cheap reduction of resource consumption from bots | Cosmetic for security, useful for logs |
| Allow-list of users or a group | Prevents a service account becoming an SSH account by accident | Especially on boxes with many system users |
| Port change | Removes untargeted noise from the logs | Not a security control; see the trap in SKILL.md. If you do it, update `ssh_port`, both firewall layers, and any monitoring |

## More Than One Person

- Each person gets their own account and their own key, with sudo. Shared logins destroy the audit trail and make offboarding guesswork.
- Offboarding is a checklist: their key removed from every host, their provider-console access removed, any API token they created rotated, and shared secrets they knew rotated. The last item is the one everyone skips and it is the one that matters (Rule 2).
- Session recording and command logging are worth it only where an audit requires them; otherwise per-person accounts plus a sensible shell history retention is proportionate.

## Jump Hosts and Bastions

- One small hardened host with the SSH port exposed, and every other box reachable only over the private network, is the standard shape for a fleet above two or three machines. It reduces the exposed surface to one address.
- Client-side jump configuration keeps this ergonomic: connecting through the bastion should be one command, or people will find a way around it.
- The bastion is a single point of failure for access. It needs the same fallback path as everything else, and it must not be the only place the recovery documentation lives.
- A modern alternative is an identity-aware access layer or a mesh VPN with no public SSH port at all (`networking.md`). Both are legitimate; both add a dependency whose own outage locks you out, so keep the provider console as the floor.

## When Fail2ban Bans You

The most common self-inflicted access failure after a hardening session, and it looks exactly like a network problem:

- Symptom: worked yesterday, times out today, nothing changed, and it works from a phone hotspot.
- Cause: repeated failed attempts (a stale key in an agent, a script with the wrong port, a monitoring check) tripped the ban, or the office address changed.
- Fix from the console: inspect the ban list, unban the address, then fix the cause. Re-banning within a minute means something is still retrying.
- Prevention: allow-list the office and home addresses, and keep the ban duration finite. A permanent ban on a dynamic address eventually locks out someone innocent.

---

**Write it down.** After any lockout — resolved or not — save the recovery path that worked to `~/Clawic/data/vps/artifacts/runbook-lockout-<host>.md`: the fallback that was available, the console path by name, the cause, and what would have made it faster. Add its `## Boxes` line to `memory.md` in the same turn with the read condition "SSH to `<host>` refuses or times out". Update the host's row in `## Hosts` if the fallback situation changed, put the SSH port and its source restriction in `## Exposure`, and record the access reference pointer in `servers.md`. Never write a key, passphrase, or console password into any of them.
