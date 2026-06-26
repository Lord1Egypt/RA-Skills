# Android Setup for SSH Tunneling and RDP

## 1. Install Required Apps
1. **ConnectBot** (or **Termux**): For creating the SSH tunnel.
2. **Microsoft Remote Desktop**: For the actual remote control.

## 2. Configure SSH Tunnel in ConnectBot
1. Open **ConnectBot**.
2. Tap the **+** button to add a new host.
3. Enter `username@your-public-ip` (or `username@tailscale-ip`).
4. Save and connect.
5. Once connected, tap the **three dots** (menu) > **Port Forwards**.
6. Tap **Add port forward**:
   *   **Nickname**: `RDP Tunnel`
   *   **Type**: `Local`
   *   **Source port**: `3389` (or any free port like `13389`)
   *   **Destination**: `localhost:3389`
7. Tap **Create port forward**.
8. **Important**: Keep ConnectBot running in the background.

## 3. Configure Microsoft Remote Desktop
1. Open **Microsoft Remote Desktop**.
2. Tap **+** > **Add PC**.
3. **PC Name**: `127.0.0.1:3389` (or the source port you chose).
4. **User Account**: Enter your Windows username and password.
5. Tap **Save**.
6. Tap the PC icon to connect.
