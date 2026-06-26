# OpenClaw VM Setup Guide

This guide walks through setting up a secure, isolated VirtualBox VM to run OpenClaw and Claude Code with the thetaedge-skill thetix skill.

## Overview

- **VM OS:** Ubuntu 25.10
- **VM User:** `openclaw`
- **Purpose:** Run OpenClaw/Claude Code in isolation from the host machine
- **Repo access:** Via SSH agent forwarding (no keys stored on VM)

---

## 1. Host-Side VirtualBox Settings

These settings are applied on your **host machine** before running the setup script inside the VM. They ensure the VM is isolated from the host.

### Create the VM

Create an Ubuntu 25.10 VM with at least:
- 2 CPU cores
- 4 GB RAM
- 25 GB disk
- Username: `openclaw`

### Disable Shared Folders

Remove any shared folders in the VM settings under **Shared Folders**. Alternatively:

```bash
VBoxManage sharedfolder remove "VM-NAME" --name "shared-folder-name"
```

### Disable Clipboard Sharing

```bash
VBoxManage modifyvm "VM-NAME" --clipboard-mode disabled
```

### Disable Drag and Drop

```bash
VBoxManage modifyvm "VM-NAME" --drag-and-drop disabled
```

### Use NAT Networking

The default NAT adapter is correct — the VM can reach the internet, but the host cannot initiate connections to the VM (except through port forwards).

### Add SSH Port Forward

Forward host port 2222 to VM port 22 for SSH access with agent forwarding:

```bash
VBoxManage modifyvm "VM-NAME" --natpf1 "ssh,tcp,,2222,,22"
```

### Do Not Install Guest Additions

VirtualBox Guest Additions enable shared folders, clipboard integration, and other host-VM bridges. Leave them uninstalled for isolation.

### Take a Snapshot

Before running the setup script, take a snapshot so you can roll back if needed:

```bash
VBoxManage snapshot "VM-NAME" take "pre-setup" --description "Clean Ubuntu before OpenClaw setup"
```

> Replace `"VM-NAME"` with your actual VM name in all commands above.

---

## 2. Transfer the Setup Script

From your host machine, copy the script to the VM:

```bash
scp -P 2222 scripts/setup-openclaw-vm.sh openclaw@localhost:~/setup-openclaw-vm.sh
```

---

## 3. SSH into the VM with Agent Forwarding

SSH agent forwarding lets the VM use your host's SSH keys without copying them:

```bash
# Make sure your SSH key is loaded on the host
ssh-add -l

# Connect with agent forwarding
ssh -A -p 2222 openclaw@localhost
```

### Verify Agent Forwarding

Once inside the VM:

```bash
ssh-add -l          # Should show your key
ssh -T git@github.com  # Should authenticate successfully
```

If `ssh-add -l` says "Could not open a connection to your authentication agent", agent forwarding is not working. Check:
- Your host SSH agent is running (`eval $(ssh-agent)` then `ssh-add`)
- You used the `-A` flag when connecting
- The VM's `/etc/ssh/sshd_config` has `AllowAgentForwarding yes` (default)

---

## 4. Run the Setup Script

```bash
chmod +x ~/setup-openclaw-vm.sh
bash ~/setup-openclaw-vm.sh
```

The script will:
1. Update system packages
2. Install and enable SSH server
3. Configure the firewall (deny incoming, allow SSH and local OpenClaw dashboard)
4. Install Node.js 22 via nvm
5. Install OpenClaw
6. Install Claude Code
7. Prompt you for your Anthropic API key (stored securely in `~/.openclaw/.env`)
8. Clone `thetaedge-skill` from GitHub via SSH
9. Install the thetix skill into `~/.openclaw/skills/` and configure credentials in `~/.openclaw/openclaw.json`

---

## 5. Post-Setup

### Verify Installations

```bash
node --version        # v22.x.x
claude --version      # Claude Code version
openclaw --version    # OpenClaw version
```

### Verify the Thetix Skill

```bash
# Symlink should resolve to the repo
ls -la ~/.openclaw/skills/thetix/SKILL.md

# Config should contain thetix credentials
cat ~/.openclaw/openclaw.json

# Test in Claude Code
claude
# Inside Claude Code, type: /thetix
```

### Update the Anthropic API Key

If you need to change your Anthropic API key:

```bash
echo 'ANTHROPIC_API_KEY=sk-your-new-key' > ~/.openclaw/.env
chmod 600 ~/.openclaw/.env
```

### Update ThetaEdge Credentials

ThetaEdge credentials are stored in `~/.openclaw/openclaw.json`. To update them, either re-run the installer or edit the file directly:

```bash
# Re-run the installer (will prompt for new credentials)
bash ~/projects/thetaedge-skill/scripts/install-thetix-skill.sh

# Or edit directly
nano ~/.openclaw/openclaw.json
```

### Manual Skill Install (Without VM Setup)

If you're not using the VM setup script, you can install the thetix skill directly:

```bash
# Clone the repo
git clone git@github.com:thetaedge/thetaedge-skill.git ~/projects/thetaedge-skill

# Run the installer
bash ~/projects/thetaedge-skill/scripts/install-thetix-skill.sh
```

The installer symlinks into `~/.openclaw/skills/thetix` and writes credentials to `~/.openclaw/openclaw.json`.

---

## 6. Security Summary

| Layer | Protection |
|-------|-----------|
| **Network** | NAT networking — VM can reach the internet, host cannot reach VM except via SSH port forward |
| **Firewall** | ufw denies all incoming except SSH (port 22); OpenClaw dashboard (port 18789) bound to localhost only |
| **Clipboard** | Disabled — no data leaks via copy/paste |
| **Shared folders** | None configured — no filesystem bridge to host |
| **Drag and drop** | Disabled |
| **Guest Additions** | Not installed — no host integration drivers |
| **SSH keys** | Agent forwarding only — private keys never leave the host |
| **API key** | Stored in `~/.openclaw/.env` with mode 600, entered interactively (not in shell history) |
| **ThetaEdge key** | Stored in `~/.openclaw/openclaw.json` with mode 600, entered interactively |

---

## 7. Snapshots and Rollback

### Take a Snapshot After Setup

From the host:

```bash
VBoxManage snapshot "VM-NAME" take "post-setup" --description "OpenClaw setup complete"
```

### Restore a Snapshot

```bash
VBoxManage snapshot "VM-NAME" restore "pre-setup"
```

### List Snapshots

```bash
VBoxManage snapshot "VM-NAME" list
```

---

## 8. Day-to-Day Usage

```bash
# From host: connect to the VM
ssh -A -p 2222 openclaw@localhost

# Inside the VM: start working
cd ~/projects/thetaedge-skill
claude
```

The SSH agent forwarding session allows git operations against private GitHub repos without storing keys on the VM. If you close the SSH session and reconnect, agent forwarding will be active again as long as your host SSH agent is running.
