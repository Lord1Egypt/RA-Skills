# Domestic Mirror Configuration

Quick reference for configuring domestic mirrors for common package managers and tools.

## System Package Managers

### Ubuntu / Debian (apt)

**Default**: `mirrors.aliyun.com`

Edit `/etc/apt/sources.list`:
```bash
# Ubuntu 24.04 (noble)
deb http://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse

# Ubuntu 22.04 (jammy)
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse

# Debian 12 (bookworm)
deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware
deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware
deb http://mirrors.aliyun.com/debian-security/ bookworm-security main contrib non-free non-free-firmware
```

**Alternatives**:
- Tsinghua: `mirrors.tuna.tsinghua.edu.cn`
- USTC: `mirrors.ustc.edu.cn`

After edit:
```bash
apt-get update
```

### CentOS / RHEL / Rocky (yum/dnf)

**Default**: `mirrors.aliyun.com`

Edit `/etc/yum.repos.d/CentOS-Base.repo`:
```ini
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/
gpgcheck=1
enabled=1

[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
gpgcheck=1
enabled=1

[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/
gpgcheck=1
enabled=1
```

```bash
# CentOS 7
yum makecache

# CentOS 8+/Rocky
dnf makecache
```

**Note**: For RHEL, use `vault.centos.org` for EOL versions or configure Red Hat's CDN.

### Alpine (apk)

**Default**: `mirrors.aliyun.com`

Edit `/etc/apk/repositories`:
```bash
http://mirrors.aliyun.com/alpine/v3.18/main
http://mirrors.aliyun.com/alpine/v3.18/community
```

Replace `v3.18` with your Alpine version (`cat /etc/alpine-release`).

```bash
apk update
```

---

## Language Package Managers

### Python (pip)

```bash
# Aliyun
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

# Tsinghua (alternative)
# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Verify
pip config list
```

**Per-user**: `~/.pip/pip.conf`
**System-wide**: `/etc/pip.conf`

### Node.js (npm)

```bash
# Taobao (recommended)
npm config set registry https://registry.npmmirror.com

# Verify
npm config get registry

# Reset to official
# npm config set registry https://registry.npmjs.org/
```

**Global config**: `/etc/npmrc` or `~/.npmrc`

### Yarn

```bash
yarn config set registry https://registry.npmmirror.com
yarn config get registry
```

**Config file**: `~/.yarnrc` or `~/.yarnrc.yml`

### Go Modules

```bash
# Add to ~/.bashrc or ~/.profile
echo 'export GOPROXY=https://goproxy.cn,direct' >> ~/.bashrc
source ~/.bashrc

# Verify
go env GOPROXY
# Should output: https://goproxy.cn,direct
```

### Rust (rustup)

```bash
# In ~/.cargo/config.toml
[source.crates-io]
replace-with = 'tuna'

[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

### Java Maven

Edit `~/.m2/settings.xml`:
```xml
<settings>
  <mirrors>
    <mirror>
      <id>aliyunmaven</id>
      <mirrorOf>*</mirrorOf>
      <name>Aliyun Maven Mirror</name>
      <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
  </mirrors>
</settings>
```

---

## Container & Tool Mirrors

### Docker

Edit `/etc/docker/daemon.json`:
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```

```bash
systemctl restart docker
# Verify
docker info | grep -A 5 "Registry Mirrors"
```

### Homebrew (Linux)

```bash
# Tsinghua mirror
echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"' >> ~/.bashrc
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"' >> ~/.bashrc
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"' >> ~/.bashrc
source ~/.bashrc
```

---

## Mirror Speed Comparison (China, 2024)

| Mirror | Latency | Reliability | Notes |
|--------|---------|-------------|-------|
| Aliyun | ~30ms | ⭐⭐⭐⭐⭐ | Best all-around, comprehensive |
| Tsinghua | ~40ms | ⭐⭐⭐⭐⭐ | Academic, stable |
| USTC | ~50ms | ⭐⭐⭐⭐ | Hefei-based, good speed |
| Huawei Cloud | ~60ms | ⭐⭐⭐⭐ | Enterprise-grade |

**Recommendation**: Start with Aliyun, fallback to Tsinghua if issues.

---

## Automatic Configuration

The `base_setup.sh` template configures system mirrors automatically:

```bash
cat templates/base_setup.sh | python3 scripts/deploy.py exec group:all "bash -s"
```

This script:
- Detects OS (Ubuntu/Debian/CentOS/Alpine)
- Configures appropriate mirrors
- Updates package cache
- Installs `curl`, `wget`, `ca-certificates`
- Configures npm/pip mirrors

---

## Troubleshooting

### Mirror unreachable

```bash
# Test connectivity
ping mirrors.aliyun.com
curl -I http://mirrors.aliyun.com/ubuntu/

# Switch to alternative
# Replace 'mirrors.aliyun.com' with 'mirrors.tuna.tsinghua.edu.cn'
```

### Stale package cache

```bash
# Debian/Ubuntu
apt-get clean
rm -rf /var/lib/apt/lists/*
apt-get update

# CentOS/RHEL
yum clean all
rm -rf /var/cache/yum
yum makecache
```

### SSL certificate errors

```bash
# Update CA certificates
apt-get install ca-certificates  # Debian/Ubuntu
yum install ca-certificates      # CentOS/RHEL
update-ca-certificates
```

### Mixed mirror sources

Ensure all sources use the same mirror to avoid version mismatch:

```bash
# Bad: mix of official and mirror
# Good: all from same mirror
deb http://mirrors.aliyun.com/ubuntu/ focal main
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main
```

---

## Manual vs Template

**Manual configuration**: Use `docs/mirrors.md` for detailed steps, custom needs.

**Template-based**: Use `base_setup.sh` for quick, automated setup across multiple servers.

---

## More Resources

- [Aliyun Mirror Station](https://mirrors.aliyun.com/)
- [Tsinghua Mirror Station](https://mirrors.tuna.tsinghua.edu.cn/)
- [USTC Mirror Station](https://mirrors.ustc.edu.cn/)
- [USTC Mirror Help](https://mirrors.ustc.edu.cn/help/)

---

*This guide covers common tools. For additional package managers, consult their documentation for mirror configuration.*
