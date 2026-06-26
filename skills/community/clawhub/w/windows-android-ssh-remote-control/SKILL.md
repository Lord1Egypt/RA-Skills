---
name: windows-android-ssh-remote
description: "Setup and guide for full remote control of a Windows PC from an Android device over the internet via SSH tunneling. Use for: remote desktop access, secure RDP over SSH, Windows-Android remote control."
---

# Windows-Android SSH Remote Control

This skill provides a secure workflow for setting up and using full remote control of a Windows PC from an Android device using SSH tunneling. This method is more secure than exposing RDP directly to the internet.

## Prerequisites

- **Windows PC**: Windows 10/11 Pro or Enterprise (Home edition does not support RDP server).
- **Android Device**: With internet access.
- **Apps**: ConnectBot (or Termux) and Microsoft Remote Desktop on Android.

## Workflow Overview

1.  **Windows Setup**: Enable RDP and OpenSSH Server.
2.  **Network Configuration**: Port forward SSH (Port 22) or use a VPN/Tailscale.
3.  **Android Setup**: Configure an SSH tunnel in ConnectBot.
4.  **Remote Connection**: Connect via Microsoft Remote Desktop to `localhost`.

## Detailed Instructions

### 1. Windows PC Configuration
Read the detailed Windows setup guide for enabling RDP and OpenSSH:
- `/home/ubuntu/skills/windows-android-ssh-remote/references/windows_setup.md`

### 2. Android Device Configuration
Read the detailed Android setup guide for configuring the SSH tunnel and RDP client:
- `/home/ubuntu/skills/windows-android-ssh-remote/references/android_setup.md`

## Security Best Practices

- **Use SSH Keys**: Disable password authentication in `sshd_config` and use public/private key pairs for maximum security.
- **Change Default Port**: Consider changing the SSH port from 22 to a non-standard port (e.g., 2222) to reduce automated bot attacks.
- **Use a VPN**: For the highest security, use a mesh VPN like **Tailscale** or **ZeroTier** instead of port forwarding. This eliminates the need to expose any ports to the public internet.

## Troubleshooting

- **Connection Refused**: Ensure the `sshd` service is running on Windows and the firewall allows Port 22.
- **RDP Fails**: Verify that the SSH tunnel is active in ConnectBot and that you are connecting to `127.0.0.1` in the RDP app.
- **NLA Error**: If you get a Network Level Authentication error, ensure your Windows user account has a password and is part of the "Remote Desktop Users" group.
