# SSH Server Skill

Remotely connect to and operate Linux/Unix servers via SSH.

## Features

- 🔐 Password/SSH key authentication
- 📡 Remote command execution
- 📊 System status monitoring
- 🐳 Docker container management
- 📝 Log viewing
- ⚙️ Service management

## Quick Start

### 1. Add Server Configuration

```bash
python D:\openClaw\openclaw\config\ssh_config.py add
```

Enter when prompted:
- Server name (e.g., vps, ubuntu)
- Server IP address
- Port (default 22)
- Username (root, ubuntu, etc.)
- Password

### 2. Connect to Server

```bash
python D:\openClaw\openclaw\config\ssh_config.py connect <server-name>
```

### 3. SSH Key Login (More Secure)

```bash
# Generate local SSH key
ssh-keygen -t ed25519

# Copy public key to server
ssh-copy-id user@server-ip
```

## Common Commands

### System Status
```bash
uptime
free -h
df -h
```

### Process Management
```bash
ps aux
ps aux | grep nginx
```

### Service Management
```bash
systemctl status nginx
sudo systemctl restart nginx
```

### Docker Operations
```bash
docker ps
docker logs container_name
docker exec -it container_name bash
```

### Log Viewing
```bash
sudo journalctl -n 100
sudo journalctl -u nginx
```

## Management Commands

```bash
# Add server
python config/ssh_config.py add

# List servers
python config/ssh_config.py list

# Connect to server
python config/ssh_config.py connect <name>

# Delete server
python config/ssh_config.py delete <name>
```

## Security Notes

- 🔐 Passwords are encrypted locally, never transmitted via chat
- 🔑 SSH key authentication recommended
- ⚠️ Confirmation before dangerous operations
