# SSH Config Guide

Complete guide for configuring SSH client (`~/.ssh/config`) for easier remote access.

## Basic Structure

```
Host <alias>
    HostName <hostname-or-ip>
    User <username>
    Port <port>
    IdentityFile <path-to-key>
```

## Common Examples

### Simple Host

```
Host production
    HostName 192.168.1.100
    User admin
```

### With Custom Port

```
Host server1
    HostName server1.example.com
    User deploy
    Port 2222
```

### With SSH Key

```
Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_key
```

### Jump Host (Bastion)

```
Host bastion
    HostName bastion.example.com
    User admin

Host internal-server
    HostName 10.0.0.5
    User admin
    ProxyJump bastion
```

### Multiple Identity Files

```
Host *
    IdentityFile ~/.ssh/id_ed25519
    IdentityFile ~/.ssh/id_rsa
```

## Useful Options

### Connection Settings

```
Host slow-server
    HostName slow.example.com
    ConnectTimeout 30
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Keep Connection Alive

```
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### Disable Host Key Checking (Not Recommended for Production)

```
Host temp-server
    HostName 192.168.1.50
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```

### Multiplexing (Faster Connections)

```
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

Create socket directory:

```bash
mkdir -p ~/.ssh/sockets
```

## Wildcards

### Apply to All Hosts

```
Host *
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
```

### Pattern Matching

```
Host *.example.com
    User admin

Host 192.168.*
    User root
```

## Advanced Patterns

### AWS EC2 Instances

```
Host aws-*
    User ec2-user
    IdentityFile ~/.ssh/aws-key.pem
    StrictHostKeyChecking no
```

### Different Keys for Different Services

```
Host github.com
    IdentityFile ~/.ssh/github_key

Host gitlab.com
    IdentityFile ~/.ssh/gitlab_key

Host bitbucket.org
    IdentityFile ~/.ssh/bitbucket_key
```

### Tunnels

```
# Local port forwarding
Host tunnel-db
    HostName server.example.com
    User admin
    LocalForward 3306 localhost:3306

# Remote port forwarding
Host tunnel-web
    HostName server.example.com
    User admin
    RemoteForward 8080 localhost:80
```

### SOCKS Proxy

```
Host proxy
    HostName proxy.example.com
    User admin
    DynamicForward 1080
```

## Security Best Practices

### Use Ed25519 Keys

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

### Limit Key Usage

```
Host restricted
    HostName sensitive.example.com
    User admin
    IdentityFile ~/.ssh/restricted_key
    PermitLocalCommand no
    AllowAgentForwarding no
```

### Use Certificate-Based Authentication

```
Host with-cert
    HostName server.example.com
    User admin
    CertificateFile ~/.ssh/user-cert.pub
```

## Debugging

### Verbose Connection

```bash
ssh -vvv user@host
```

### Test Config

```bash
ssh -G <alias> | grep -i hostname
```

### Show Effective Config

```bash
ssh -G production
```

## Config File Permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

## Sample Complete Config

```
# Global defaults
Host *
    AddKeysToAgent yes
    UseKeychain yes
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Production servers
Host prod-web1
    HostName 192.168.1.10
    User admin

Host prod-web2
    HostName 192.168.1.11
    User admin

Host prod-db
    HostName 192.168.1.20
    User postgres
    IdentityFile ~/.ssh/db_key

# Staging servers
Host staging-*
    HostName %h.staging.example.com
    User deploy

# Bastion host
Host bastion
    HostName bastion.example.com
    User admin

# Internal servers via bastion
Host internal-*
    User admin
    ProxyJump bastion

# GitHub
Host github.com
    User git
    IdentityFile ~/.ssh/github_key

# GitLab
Host gitlab.com
    User git
    IdentityFile ~/.ssh/gitlab_key
```
