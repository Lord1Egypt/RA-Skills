# Windows PC Setup for SSH and RDP

## 1. Enable Remote Desktop (RDP)
1. Open **Settings** > **System** > **Remote Desktop**.
2. Toggle **Enable Remote Desktop** to **On**.
3. Note the PC name (though we will use `localhost` via the tunnel).
4. Ensure "Require computers to use Network Level Authentication (NLA) to connect" is checked for security.

## 2. Install and Start OpenSSH Server
1. Open **PowerShell** as Administrator.
2. Check if OpenSSH is installed:
   ```powershell
   Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
   ```
3. If not installed, run:
   ```powershell
   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
   ```
4. Start the service and set to automatic:
   ```powershell
   Start-Service sshd
   Set-Service -Name sshd -StartupType 'Automatic'
   ```
5. Verify firewall rule:
   ```powershell
   Get-NetFirewallRule -Name *OpenSSH-Server* | select Name, DisplayName, Enabled
   ```

## 3. Configure Port Forwarding (If not using a VPN/Tailscale)
If the PC is behind a router, you must forward **Port 22 (TCP)** to the PC's local IP address in the router settings.
*   **Warning**: Exposing Port 22 to the internet is a security risk. Use strong passwords or, preferably, SSH keys.
*   **Alternative**: Use **Tailscale** or **ZeroTier** to create a private network, avoiding port forwarding entirely.
