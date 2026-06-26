# VM Contents Reference

Detailed reference of what's installed inside the VM and where to find it.

## Installed Software

| Tool | Version | Install Method | Notes |
|------|---------|---------------|-------|
| Ubuntu | 24.04 LTS | Base box (bento/ubuntu-24.04) | arm64 or amd64 |
| Go | 1.24.3 (configurable) | Binary download from go.dev | SHA256 verified |
| Docker | Latest CE | Official Docker repo | Daemon running, vagrant user in docker group |
| mage | Latest | `go install` | Go build tool |
| build-essential | System | apt-get | gcc, make, etc. |
| iptables | System | apt-get | Firewall management |
| dnsmasq | System | apt-get | DNS filtering (disabled by default) |
| iproute2 | System | apt-get | `ip` command |
| dnsutils | System | apt-get | `dig` command |
| net-tools | System | apt-get | `ifconfig`, `netstat` |
| sqlite3 | System | apt-get | With libsqlite3-dev |
| jq | System | apt-get | JSON processing |
| curl | System | apt-get | HTTP client |
| git | System | apt-get | Version control |
| strace | System | apt-get | System call tracing |
| KVM tools | System | apt-get (conditional) | Only if `/dev/kvm` exists |

## Filesystem Layout

| Path | Contents |
|------|----------|
| `/project` | Source code (rsynced from host, if PROJECT_SRC set) |
| `/vagrant-scripts` | Setup and verify scripts |
| `/usr/local/go/bin/go` | Go toolchain |
| `/usr/local/bin/mage` | Mage build tool |
| `/etc/profile.d/go.sh` | Go PATH configuration (loaded in all shells) |

## Environment Variables (set in VM)

```bash
PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"
GOPATH="$HOME/go"
```

## Users and Groups

| User | Groups | Purpose |
|------|--------|---------|
| vagrant | vagrant, docker, (libvirt, kvm if KVM available) | Default SSH user, full sudo |

## rsync Excludes

When syncing with `PROJECT_SRC`, these paths are excluded:
- `.git/`
- `node_modules/`
- `vendor/`
- `bin/`
- `dist/`
- `build/`
- `.next/`
- `coverage.out`
- `coverage.html`
