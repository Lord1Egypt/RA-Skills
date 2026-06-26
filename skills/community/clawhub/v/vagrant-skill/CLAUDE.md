# CLAUDE.md — vagrant-skill

## What This Is

A general-purpose disposable VM skill for AI agents and developers. Provides Ubuntu 24.04 VMs with full sudo, Docker, Go, mage, and optional nested KVM.

Works as both a Claude Code skill (`/vagrant`) and an OpenClaw skill.

## Key Commands

```bash
# Start VM
vagrant up
PROJECT_SRC=~/myproject vagrant up

# Run commands inside
vagrant ssh -c "command here"

# Sync changes
vagrant rsync

# Destroy
vagrant destroy -f

# Re-provision
vagrant provision
```

## File Layout

- `Vagrantfile` — VM config, multi-provider (libvirt + VirtualBox)
- `SKILL.md` — Agent Skills standard skill definition
- `scripts/setup.sh` — Provisioner (system deps, Docker, Go, mage, KVM)
- `scripts/verify.sh` — Validation suite
- `test/` — Tests (bats-core)
- `docs/` — Reference docs

## Testing

```bash
# Run all tests
make test

# Shellcheck
make lint

# Full integration (requires Vagrant + provider)
make test-integration
```

## Rules

- No project-specific tooling in setup.sh (this is general-purpose)
- Consumer projects add their own provisioning on top
- All scripts must be idempotent
- All scripts must pass shellcheck
