---
name: xui-node-manager
description: >-
  Install 3x-ui panels on servers via SSH, create VLESS+Reality+TCP nodes
  with SOCKS5 outbound binding. Triggers on giving SOCKS5 ip:port:user:pass
  with a server name, or requests like install panel, create node, 3x-ui.
---

# 3x-ui Node Manager

## Workflows

### 0. Install 3x-ui panel (one-time per server)

User provides SSH login info. Run:

```bash
bash scripts/xui_install.sh <ip> <ssh_port> <username> <password>
```

What the script does:
1. SSH 登录到服务器
2. 运行 `bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)`
3. 全程自动按默认选项安装（自动回车确认）
4. 等待安装完成
5. 提取面板信息（URL、用户名、密码、端口、WebBasePath、API Token）

**Install done. Now you MUST:**

1. Add the new panel to `scripts/servers.yaml` in the `servers:` list  
   - 脚本自动检测 SSL 是否成功，失败则 URL 用 `http://` 而非 `https://`
2. Display the installation result to the user (URL, username, password, etc.)

### 1. Server registration (one-time)

Edit `scripts/servers.yaml` using `scripts/servers.yaml.example` as template. Can also be done manually or automatically after install.

```yaml
proxy: socks5://127.0.0.1:10808

defaults:
  dest: 1.1.1.1:443
  server_names: [www.microsoft.com]
  port: random
  port_range: [10000, 60000]

servers:
  - name: server-1
    url: http://<ip>:<port>/<path>
    username: <user>
    password: <pass>
```

### 2. Create nodes (per-request)

User gives SOCKS5 exit + target server. Run:

```bash
pip install -r scripts/requirements.txt
python3 scripts/xui_batch.py --server <name|all> --socks5 <ip:port:user:pass>
```

### 3. Display results (MANDATORY)

After the script finishes, you MUST:

1. **Read the QR PNG file** whose path is printed in the output (look for `QR_PNG:` line)
2. **Display it inline** using the `read` tool — this renders the QR image directly in chat
3. **Print the vless:// URI** alongside it

Never just report the file path. Always show the QR image.

## Safety Rules

**NEVER delete existing inbounds without explicit user approval.**
The script creates new nodes on random ports — it does not need to delete anything.
If the user explicitly asks to delete a node, confirm which one before proceeding.
If port conflicts occur, ask the user before removing any inbound.

## Auto-generated settings

- Remark: today's date (YYYY-MM-DD)
- Port: random in [10000, 60000]
- Client tag: last 2 octets of SOCKS5 IP + date suffix
- Outbound tag: socks5-<ip>
- Reality keys: from panel API
