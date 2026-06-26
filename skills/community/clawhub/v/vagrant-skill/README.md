# vagrant-skill

**Disposable VMs for safe testing — an [Agent Skills](https://agentskills.io) standard skill**

| | |
|---|---|
| **Repo** | [daax-dev/vagrant-skill](https://github.com/daax-dev/vagrant-skill) |
| **Stack** | Vagrant, Shell, Ubuntu 24.04 |
| **Skill** | [Agent Skills](https://agentskills.io) standard |
| **Compatible** | Claude Code, Claude.ai, OpenClaw, Cursor, Gemini CLI, and [30+ agents](https://agentskills.io) |
| **License** | Apache 2.0 |

## What It Does

Provides disposable, fully-provisioned Ubuntu 24.04 VMs for safe experimentation:

- **Full sudo access** — agents and humans can do anything without risk to the host
- **Pre-installed tooling** — Go 1.24, Docker, mage, build-essential, network tools
- **Nested KVM** — hardware virtualization passthrough (Linux with libvirt)
- **Configurable** — sync any project, adjust CPU/RAM/Go version via env vars
- **Destroy and recreate** — VMs are ephemeral, nothing persists unless you want it
- **Cross-platform** — tested on Mac (Parallels), Linux (libvirt), with VirtualBox as fallback

---

## Quick Start

```bash
# Start VM (no project sync)
vagrant up

# Start VM with your project synced into /project
PROJECT_SRC=~/myproject vagrant up

# Run commands inside (agent workflow — no interactive SSH needed)
vagrant ssh -c "sudo apt-get install -y something"
vagrant ssh -c "cd /project && make test"

# Sync code changes from host
vagrant rsync

# Destroy and start fresh
vagrant destroy -f
```

## Examples

Three self-contained examples, one per platform. Each has a `Vagrantfile`, a `scripts/provision.sh`, and a `test/e2e.bats` suite. Run them the same way:

```bash
vagrant up
bats test/e2e.bats
vagrant destroy -f
```

---

### Linux — nginx-hardened (`examples/nginx-hardened/`)

Deploys nginx with a hardened iptables firewall (INPUT DROP by default, allow SSH + HTTP only). **16 bats tests.**

**Why it needs a VM:** `iptables -F INPUT` + `-P INPUT DROP` on the host locks you out of your own SSH session. Provider: **libvirt**.

```bash
cd examples/nginx-hardened
vagrant up
bats test/e2e.bats
vagrant destroy -f
```

**Ask the LLM:**
> `/vagrant` Run the nginx-hardened example in `examples/nginx-hardened/`, show me the full bats output, then destroy the VM.

---

### Mac — docker-compose (`examples/mac-docker-compose/`)

Runs a Docker Compose stack: nginx on port 80 proxying a Python JSON API on port 8000 (internal only). **14 bats tests.**

**Why it needs a VM:** Docker Desktop requires a commercial license and proxies port bindings through a hyperkit shim. Docker CE in a Parallels VM has no restrictions. Provider: **Parallels** (Apple Silicon).

```bash
cd examples/mac-docker-compose
vagrant up --provider=parallels
bats test/e2e.bats
vagrant destroy -f
```

**Ask the LLM:**
> `/vagrant` Run the mac-docker-compose example in `examples/mac-docker-compose/`, show me the bats results proving the stack is up, then tear it down.

---

### Windows — systemd-service (`examples/windows-systemd-service/`)

Deploys a Python HTTP server as a real systemd unit file, running as a dedicated `demo` system user. **20 bats tests** including service restart after SIGKILL.

**Why it needs a VM:** WSL2 does not run real systemd — you can't test unit files without a proper Linux VM. Provider: **VirtualBox**.

WSL2 setup before `vagrant up`:
```bash
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"
```

```bash
cd examples/windows-systemd-service
vagrant up --provider=virtualbox
bats test/e2e.bats
vagrant destroy -f
```

**Ask the LLM:**
> `/vagrant` Run the windows-systemd-service example in `examples/windows-systemd-service/`, show me the bats output and journald logs, then destroy the VM.

---

## Configuration

| Variable | Default | Purpose |
|----------|---------|---------|
| `PROJECT_SRC` | auto-detect | Host directory to sync into VM at `/project` |
| `VM_CPUS` | 4 | Number of vCPUs |
| `VM_MEMORY` | 4096 | RAM in MB |
| `VM_NAME` | vagrant-skill-dev | VM hostname |
| `GO_VERSION` | 1.24.3 | Go version to install |

```bash
PROJECT_SRC=~/myapp VM_CPUS=8 VM_MEMORY=8192 vagrant up
```

---

## Install as a Skill

> **Note:** The skill name is `vagrant`. When installing, clone into a directory
> named `vagrant` (not `vagrant-skill`) so the directory name matches the skill
> name per the [Agent Skills spec](https://agentskills.io/specification).

### Claude Code

```bash
# Global (available in all projects)
git clone git@github.com:daax-dev/vagrant-skill.git ~/.claude/skills/vagrant

# Per-project
git clone git@github.com:daax-dev/vagrant-skill.git .claude/skills/vagrant
```

Then use `/vagrant` in Claude Code.

### ClawHub

```bash
npx clawhub@latest install vagrant
```

### Other Agent Skills-Compatible Agents

Any agent that supports the [Agent Skills standard](https://agentskills.io) can use this skill. Install into the agent's skill directory with the name `vagrant`:

```bash
git clone git@github.com:daax-dev/vagrant-skill.git <agent-skills-dir>/vagrant
```

---

## Platform Setup

### Mac (Apple Silicon — M1/M2/M3/M4) — Recommended: Parallels

VirtualBox on Apple Silicon is experimental and unreliable. **Use Parallels.**

```bash
# 1. Install Parallels Desktop (requires license)
#    Download from https://www.parallels.com/products/desktop/

# 2. Install Vagrant
brew install --cask vagrant

# 3. Install the Parallels provider plugin
vagrant plugin install vagrant-parallels

# 4. Clone and start
git clone git@github.com:daax-dev/vagrant-skill.git vagrant
cd vagrant
vagrant up --provider=parallels
```

**Verified working:** macOS 26.3, Apple Silicon (arm64), Parallels Desktop, Vagrant 2.4.9, bento/ubuntu-24.04 arm64 box. Setup provisions Go 1.24.3 (arm64), Docker, mage. 11/11 checks pass.

**KVM note:** Nested KVM is not available on Mac (no `/dev/kvm`). The VM still provides Docker, Go, mage, and full sudo. If you need nested KVM (e.g., for Firecracker microVM testing), use a Linux host.

### Mac (Intel) — VirtualBox

```bash
brew install --cask virtualbox
brew install --cask vagrant
git clone git@github.com:daax-dev/vagrant-skill.git vagrant
cd vagrant
vagrant up --provider=virtualbox
```

### Linux — Recommended: libvirt/KVM

This is the most capable setup — includes nested KVM for microVM testing.

```bash
sudo apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo apt-get install -y vagrant
vagrant plugin install vagrant-libvirt
git clone git@github.com:daax-dev/vagrant-skill.git vagrant
cd vagrant
vagrant up --provider=libvirt
```

**Nested KVM** is automatically enabled (`cpu_mode: host-passthrough`). Verify:
```bash
test -e /dev/kvm && echo "KVM OK"
vagrant ssh -c "test -e /dev/kvm && echo 'Nested KVM OK'"
```

### Windows (WSL2) — VirtualBox

```bash
# Install VirtualBox on Windows (not inside WSL2)
# Inside WSL2:
sudo apt-get install -y vagrant
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"
git clone git@github.com:daax-dev/vagrant-skill.git vagrant
cd vagrant
vagrant up --provider=virtualbox
```

---

## Using as a Consumer

Projects that depend on vagrant-skill for dev environments:

```bash
# From vagrant-skill directory, point to your project
PROJECT_SRC=~/path/to/your-project vagrant up

# Then run project-specific setup inside the VM
vagrant ssh -c "sudo /project/scripts/my-setup.sh"
```

---

## What's In The VM

| Tool | Version | Notes |
|------|---------|-------|
| Ubuntu | 24.04 LTS | bento/ubuntu-24.04 box |
| Go | 1.24.3 | arm64 or amd64 auto-detected |
| Docker | Latest CE | Daemon running, vagrant user in docker group |
| mage | Latest | Go build tool |
| build-essential | System | gcc, make, etc. |
| Network tools | System | iptables, dnsmasq, iproute2, dig, net-tools |
| KVM tools | System | Only on Linux with nested KVM |
| sqlite3 | System | With libsqlite3-dev |
| jq, curl, git | System | Standard utilities |

---

## Testing

```bash
# Lint (shellcheck + ruby syntax)
make lint

# Unit tests (58 bats tests)
make test

# Full integration (spins up VM, provisions, verifies, destroys)
make test-integration

# All
make test-all
```

## Project Structure

```
vagrant-skill/
├── Vagrantfile                    # Multi-provider (Parallels, libvirt, VirtualBox)
├── SKILL.md                       # Agent Skills standard skill definition
├── scripts/
│   ├── setup.sh                   # Provisioner: system deps, Docker, Go, mage, KVM
│   └── verify.sh                  # Validation suite (11 checks)
├── examples/
│   ├── nginx-hardened/            # Linux/libvirt:    nginx + iptables firewall (16 tests)
│   ├── mac-docker-compose/        # Mac/Parallels:    Docker Compose stack (14 tests)
│   └── windows-systemd-service/   # Windows/VirtualBox: systemd unit file (20 tests)
│       (each has Vagrantfile, scripts/provision.sh, test/e2e.bats)
├── references/                    # Progressive disclosure
│   ├── platform-setup.md          # Detailed provider installation
│   └── vm-contents.md             # VM filesystem and software reference
├── docs/                          # Project documentation
├── test/                          # bats-core tests (unit + integration)
├── Makefile                       # lint, test, test-integration, up, destroy
├── README.md
├── CLAUDE.md
└── LICENSE                        # Apache 2.0
```

## License

Apache 2.0
