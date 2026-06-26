---
name: vagrant
description: >-
  Disposable VMs for safe testing — full sudo, Docker, Go, nested KVM, destroy
  and recreate. Use when you need a sandbox to build, test, or break things
  without affecting the host. Use when the user says "spin up a VM", "test in
  isolation", "run with sudo", "try something dangerous", "set up a dev
  environment", "I need Docker", "test firewall rules", "clean environment",
  or needs root access, network testing, or safe experimentation.
license: Apache-2.0
compatibility: >-
  Requires vagrant binary and at least one provider: Parallels (Mac Apple
  Silicon), libvirt (Linux), or VirtualBox (cross-platform). Designed for
  terminal-based AI agents and interactive developer use.
allowed-tools: "Bash(vagrant:*) Bash(bats:*) Read Write"
metadata:
  author: jpoley
  version: "0.1.0"
  category: infrastructure
  tags: [vm, sandbox, testing, docker, devops, isolation, kvm]
  openclaw:
    requires:
      bins:
        - vagrant
      anyBins:
        - VBoxManage
        - virsh
        - prlctl
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This skill provides a **disposable VM sandbox** for safe development and testing. All privileged operations (sudo, iptables, Docker, systemd, KVM) happen inside the VM — the host is never modified.

**You (the agent) should NEVER need host-level sudo.** Instead, use this Vagrant workflow to get a fully provisioned, disposable VM where you have unrestricted root access.

### Prerequisites

Before using this workflow, verify a provider is available:

```bash
# Check Vagrant is installed
command -v vagrant

# Check for a provider (any one is sufficient)
command -v prlctl        # Parallels (Mac Apple Silicon — recommended)
vagrant plugin list | grep libvirt  # libvirt (Linux — nested KVM)
command -v VBoxManage    # VirtualBox (fallback)
```

See [references/platform-setup.md](references/platform-setup.md) for detailed provider installation.

---

## Core Workflow

### Step 1: Create a Vagrantfile in the User's Project

If the user's project does not already have a `Vagrantfile`, you MUST create a real, working one in their project directory. This is not a template or example — it must work end-to-end with `vagrant up`.

**Requirements for the Vagrantfile you create:**
- Base box: `bento/ubuntu-24.04`
- Sync the project root into the VM: `config.vm.synced_folder ".", "/project", type: "rsync"`
- Include all three providers (Parallels, libvirt, VirtualBox) so it works on any platform
- Provision with the actual tools the project needs (inspect the project first — look for `go.mod`, `package.json`, `requirements.txt`, `Makefile`, `Dockerfile`, etc.)
- Use `set -euo pipefail` in provisioning scripts
- Make provisioning idempotent

Here is the **base Vagrantfile** — you MUST customize the provisioning section based on what the project actually uses:

```ruby
# -*- mode: ruby -*-
# Vagrantfile — disposable dev/test VM

VM_CPUS   = Integer(ENV["VM_CPUS"]   || 4)
VM_MEMORY = Integer(ENV["VM_MEMORY"] || 4096)

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.box_check_update = false
  config.vm.hostname = "dev"
  config.vm.boot_timeout = 300
  config.ssh.forward_agent = true

  # ─── Sync project into VM at /project ─────────────────────────────────────
  config.vm.synced_folder ".", "/project", type: "rsync",
    rsync__exclude: [
      ".git/", "node_modules/", "vendor/", ".vagrant/",
      "bin/", "dist/", "build/", ".next/",
    ]

  # ─── Provider: Parallels (Mac Apple Silicon — recommended) ────────────────
  config.vm.provider "parallels" do |prl|
    prl.cpus   = VM_CPUS
    prl.memory = VM_MEMORY
    prl.update_guest_tools = true
  end

  # ─── Provider: libvirt (Linux — preferred, nested KVM) ────────────────────
  config.vm.provider "libvirt" do |lv|
    lv.cpus   = VM_CPUS
    lv.memory = VM_MEMORY
    lv.cpu_mode = "host-passthrough"
    lv.nested = true
  end

  # ─── Provider: VirtualBox (cross-platform fallback) ───────────────────────
  config.vm.provider "virtualbox" do |vb|
    vb.cpus   = VM_CPUS
    vb.memory = VM_MEMORY
    vb.customize ["modifyvm", :id, "--nested-hw-virt", "on"]
  end

  # ─── Provision: install project dependencies ──────────────────────────────
  # CUSTOMIZE THIS for the project. Inspect go.mod, package.json,
  # requirements.txt, Dockerfile, Makefile, etc. and install what's needed.
  config.vm.provision "shell", privileged: true, inline: <<-SHELL
    set -euo pipefail
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq build-essential curl git jq ca-certificates gnupg

    # ── Docker ────────────────────────────────────────────────────────────
    if ! command -v docker &>/dev/null; then
      install -m 0755 -d /etc/apt/keyrings
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
        -o /etc/apt/keyrings/docker.asc
      chmod a+r /etc/apt/keyrings/docker.asc
      echo "deb [arch=$(dpkg --print-architecture) \
        signed-by=/etc/apt/keyrings/docker.asc] \
        https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
        | tee /etc/apt/sources.list.d/docker.list > /dev/null
      apt-get update -qq
      apt-get install -y -qq docker-ce docker-ce-cli containerd.io
    fi
    systemctl enable --now docker
    usermod -aG docker vagrant

    # ── Add project-specific tooling below ────────────────────────────────
    # Examples (uncomment / add what the project needs):
    #
    # Go:
    #   GO_VERSION="1.24.3"
    #   curl -fsSL "https://go.dev/dl/go${GO_VERSION}.linux-$(dpkg --print-architecture).tar.gz" \
    #     | tar -C /usr/local -xz
    #   echo 'export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"' > /etc/profile.d/go.sh
    #
    # Node.js:
    #   curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
    #   apt-get install -y -qq nodejs
    #
    # Python:
    #   apt-get install -y -qq python3 python3-pip python3-venv

    echo "VM ready — project synced at /project"
  SHELL
end
```

**You MUST customize the provisioning section.** Read the project to determine what it needs:
- `go.mod` → install Go
- `package.json` → install Node.js
- `requirements.txt` / `pyproject.toml` → install Python
- `Dockerfile` → Docker is already included above
- Network testing → add `iptables dnsmasq dnsutils iproute2 net-tools`
- KVM/microVM testing → add `qemu-kvm libvirt-daemon-system`

Uncomment the relevant blocks and add any other tooling. Do NOT leave placeholder comments in the final Vagrantfile — produce a clean, working file.

Then **add `.vagrant/` to the user's `.gitignore`** if not already present:

```bash
grep -qxF '.vagrant/' .gitignore 2>/dev/null || echo '.vagrant/' >> .gitignore
```

The Vagrantfile itself **should be committed** — it's reusable project infrastructure.

If the user already has a `Vagrantfile`, use it as-is unless they ask to modify it.

### Step 2: Start the VM

```bash
vagrant up
```

This boots the VM with the user's project synced at `/project` inside the VM.

### Step 3: Run Commands Inside the VM

**All commands use `vagrant ssh -c` from the host.** No interactive SSH needed.

```bash
# Run any command with sudo
vagrant ssh -c "sudo apt-get install -y some-package"

# Build the project
vagrant ssh -c "cd /project && make build"
vagrant ssh -c "cd /project && go test ./..."

# Docker operations
vagrant ssh -c "docker build -t myimage ."
vagrant ssh -c "docker run --rm myimage"

# Network/firewall testing
vagrant ssh -c "sudo iptables -L -n"
```

### Step 4: Iterate on Code Changes

When you modify source on the host:

```bash
vagrant rsync                                    # sync changes to VM
vagrant ssh -c "cd /project && make build"       # rebuild
vagrant ssh -c "cd /project && make test"        # test
```

### Step 5: Tear Down

```bash
vagrant destroy -f    # destroys VM completely, clean slate
```

---

## Testing Patterns

### Pattern: Build-Test-Fix Loop

```bash
vagrant rsync && vagrant ssh -c "cd /project && make build"
vagrant ssh -c "cd /project && make test"
# If tests fail, fix code on host, repeat
```

### Pattern: Docker-in-VM

```bash
vagrant ssh -c "cd /project && docker build -t test ."
vagrant ssh -c "docker run --rm test"
```

### Pattern: Network/Firewall Testing

```bash
vagrant ssh -c "sudo iptables -A FORWARD -s 172.16.0.0/24 -j DROP"
vagrant ssh -c "sudo iptables -L -n -v"
```

### Pattern: bats End-to-End Tests

Run a [bats-core](https://github.com/bats-core/bats-core) test suite against a live VM as proof that the system under test works. The VM must be up before running bats.

```bash
vagrant up
bats test/e2e.bats      # run tests, output is the proof
vagrant destroy -f      # tear down after
```

Capture output to show the user:

```bash
vagrant up
bats test/e2e.bats 2>&1 | tee /tmp/bats-results.txt
vagrant destroy -f
cat /tmp/bats-results.txt
```

bats exits non-zero on any failure — treat that as a test run failure.

### Pattern: Full Reprovision (Nuclear Option)

```bash
vagrant destroy -f && vagrant up
```

---

## Configuration

Environment variables to customize the VM (set before `vagrant up`):

| Variable | Default | Purpose |
|----------|---------|---------|
| `VM_CPUS` | 4 | Number of vCPUs |
| `VM_MEMORY` | 4096 | RAM in MB |

Example:
```bash
VM_CPUS=8 VM_MEMORY=8192 vagrant up
```

See [references/vm-contents.md](references/vm-contents.md) for full details on VM filesystem layout and installed software.

## Safety Guarantees

- **No host sudo required** — all privileged operations are inside the VM
- **Fully disposable** — `vagrant destroy -f` removes everything
- **Idempotent provisioning** — `vagrant provision` is safe to re-run
- **Isolated networking** — VM has its own network stack
- **Source is rsynced** — VM gets a copy; your host repo is never modified by the VM
- **No persistent state** — destroying the VM removes all data
- **Vagrantfile is committed** — reusable across sessions; `.vagrant/` is gitignored

## Examples

### Example 1: Test iptables firewall rules without touching host network

User says: "I need to test some firewall rules before deploying to production"

Actions:
1. Create Vagrantfile with `iptables dnsmasq dnsutils iproute2 net-tools` provisioned
2. `vagrant up`
3. `vagrant ssh -c "sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT"`
4. `vagrant ssh -c "sudo iptables -A INPUT -p tcp --dport 0:442 -j DROP"`
5. `vagrant ssh -c "sudo iptables -L -n -v"` — verify rules look right
6. `vagrant ssh -c "sudo iptables-save > /project/firewall.rules"` — export if good
7. `vagrant rsync` to get rules file back, or `vagrant destroy -f` to scrap

Result: Firewall rules iterated safely. Host network never touched. Rules exportable.

### Example 2: Test systemd service configuration

User says: "I need to test this systemd unit file before deploying"

Actions:
1. Create Vagrantfile with the project synced
2. `vagrant up`
3. `vagrant ssh -c "sudo cp /project/myservice.service /etc/systemd/system/"`
4. `vagrant ssh -c "sudo systemctl daemon-reload && sudo systemctl start myservice"`
5. `vagrant ssh -c "systemctl status myservice"` — check it works
6. `vagrant ssh -c "sudo journalctl -u myservice --no-pager"` — check logs
7. `vagrant destroy -f` — clean slate

Result: Service tested with real systemd, real journald. No risk to host init system.

### Example 3: Docker daemon configuration and privileged port binding

User says: "I need to test a Docker compose setup that binds port 80"

Actions:
1. Create Vagrantfile with Docker CE provisioned
2. `vagrant up`
3. `vagrant ssh -c "cd /project && docker compose up -d"`
4. `vagrant ssh -c "curl -sf http://localhost"` — test from inside VM
5. `vagrant ssh -c "docker compose logs"` — check output
6. `vagrant ssh -c "docker compose down"` — cleanup
7. `vagrant destroy -f`

Result: Full Docker compose stack running with privileged ports — impossible without sudo on the host.

### Example 4: Run the built-in e2e examples

Three working examples live under `examples/` in this skill's directory. All follow the same pattern — boot, test, tear down:

```bash
cd examples/<name>
vagrant up [--provider=<provider>]
bats test/e2e.bats 2>&1 | tee /tmp/e2e-results.txt
cat /tmp/e2e-results.txt
vagrant destroy -f
```

#### `examples/nginx-hardened/` — Linux / libvirt (16 tests)

Deploys nginx + hardened iptables (INPUT DROP, allow SSH + HTTP only).
**Why VM:** `iptables -F INPUT; iptables -P INPUT DROP` on the host locks you out.

```bash
cd examples/nginx-hardened
vagrant up
bats test/e2e.bats 2>&1 | tee /tmp/e2e-results.txt
vagrant destroy -f
```

#### `examples/mac-docker-compose/` — Mac Apple Silicon / Parallels (14 tests)

Runs a Docker Compose stack: nginx on port 80 proxying a Python JSON API.
**Why VM:** Docker Desktop requires a commercial license; Docker CE in a VM has none of its restrictions.

```bash
cd examples/mac-docker-compose
vagrant up --provider=parallels
bats test/e2e.bats 2>&1 | tee /tmp/e2e-results.txt
vagrant destroy -f
```

#### `examples/windows-systemd-service/` — Windows WSL2 / VirtualBox (20 tests)

Deploys a Python HTTP server as a real systemd unit, running as a dedicated system user.
**Why VM:** WSL2 does not run real systemd — unit files cannot be tested without a real Linux init.

WSL2 pre-flight:
```bash
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"
```

```bash
cd examples/windows-systemd-service
vagrant up --provider=virtualbox
bats test/e2e.bats 2>&1 | tee /tmp/e2e-results.txt
vagrant destroy -f
```

## Troubleshooting

### VM Won't Boot

**Error:** `vagrant up` hangs or times out
**Cause:** Provider not installed or configured correctly
**Solution:**
1. Check provider is installed: `vagrant plugin list`
2. Debug boot: `vagrant up --debug 2>&1 | tail -50`
3. Try explicit provider: `vagrant up --provider=virtualbox`

### Source Not Synced

**Error:** `/project` directory is empty or missing inside VM
**Cause:** rsync failed or synced_folder misconfigured
**Solution:**
1. Re-sync: `vagrant rsync`
2. Check Vagrantfile has `synced_folder ".", "/project", type: "rsync"`

### Provider Mismatch

**Error:** `vagrant up` uses wrong provider
**Cause:** Multiple providers installed, Vagrant auto-selects
**Solution:**
1. Check what's running: `vagrant status`
2. Force provider: `vagrant up --provider=parallels`

### KVM Not Available Inside VM

**Error:** `/dev/kvm` missing inside the VM
**Cause:** Host doesn't support nested virtualization or provider not configured
**Solution:**
1. Ensure host has KVM: `test -e /dev/kvm` on host
2. Use libvirt provider with `cpu_mode = "host-passthrough"`
3. Mac: nested KVM is not available — use a Linux host for KVM workloads
