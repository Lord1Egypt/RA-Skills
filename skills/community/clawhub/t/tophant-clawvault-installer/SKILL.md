---
name: tophant-clawvault-installer
version: 0.2.13
description: Install, configure, test, and uninstall ClawVault AI security proxy
homepage: https://github.com/tophant-ai/ClawVault
user-invocable: true
disable-model-invocation: false
---

# ClawVault Installer

Install, configure, test, and uninstall ClawVault — the AI security proxy that protects agents from prompt injection, data leakage, and dangerous commands.

**Protection Against:**
- Prompt injection attacks
- Data leakage (PII, credentials, API keys)
- Dangerous command execution
- Jailbreak attempts

## What This Skill Does

Installs ClawVault into a dedicated venv at `~/.clawvault-env/` and writes config under `~/.ClawVault/`. See `SECURITY.md` for the full capability, risk, and design-intent disclosure.

## How to Run

**IMPORTANT: All commands MUST be executed using the Python script bundled with this skill.**

Do NOT run `pip install`, `clawvault`, or any other command directly. Always use:

```bash
python3 SKILL_DIR/clawvault_manager.py <command> [options]
```

Where `SKILL_DIR` is the directory containing this SKILL.md file (typically `~/.openclaw/workspace/skills/tophant-clawvault-installer/` or `~/.openclaw/skills/tophant-clawvault-installer/`).

Add `--json` to any command for machine-readable JSON output.

## Commands

### /tophant-clawvault-installer install

Install ClawVault. The script creates a Python virtual environment, temporarily installs the latest GitHub repository code from `main` instead of PyPI or a fixed tag, generates config, writes OpenClaw gateway proxy config when the gateway service exists, and starts ClawVault services. By default it does **not** restart `openclaw-gateway`, because recent OpenClaw versions may disconnect or hang after a gateway restart. **No pip or system package manager needed.**

```bash
# Default: write OpenClaw gateway proxy config and start ClawVault web dashboard,
# but do not restart openclaw-gateway.
# ClawVault web dashboard starts at http://localhost:8766.
# To activate OpenClaw proxy later, manually run:
#   systemctl --user restart openclaw-gateway
python3 SKILL_DIR/clawvault_manager.py install --mode quick --install-plugin --json

# Interactive setup
python3 SKILL_DIR/clawvault_manager.py install --mode standard --json

# Full control (strict mode)
python3 SKILL_DIR/clawvault_manager.py install --mode advanced --json

# Install without starting services
python3 SKILL_DIR/clawvault_manager.py install --mode quick --no-start --json

# Deprecated compatibility flag: proxy config is already written by default
python3 SKILL_DIR/clawvault_manager.py install --mode quick --configure-gateway-proxy --json

# Dangerous: restart gateway immediately; may disconnect or hang OpenClaw
python3 SKILL_DIR/clawvault_manager.py install --mode quick --configure-gateway-proxy --restart-gateway --json

# Skip OpenClaw proxy integration explicitly
python3 SKILL_DIR/clawvault_manager.py install --mode quick --no-proxy --json
```

### OpenClaw plugin acceptance check

After installing the plugin, send a normal OpenClaw prompt that asks to read `/tmp/.env.demo`. If the plugin is active, that prompt should trigger file-guard interception and appear in the ClawVault dashboard.

### /tophant-clawvault-installer health

Check service health and status.

```bash
python3 SKILL_DIR/clawvault_manager.py health --json
```

### /tophant-clawvault-installer generate-rule

Generate security rules from natural language.

```bash
python3 SKILL_DIR/clawvault_manager.py generate-rule "Block all AWS credentials" --json
python3 SKILL_DIR/clawvault_manager.py generate-rule --scenario customer_service --apply --json
```

**Scenarios:** `customer_service`, `development`, `production`, `finance`

### /tophant-clawvault-installer test

Run detection tests.

```bash
python3 SKILL_DIR/clawvault_manager.py test --category all --json
python3 SKILL_DIR/clawvault_manager.py test --category sensitive --json
```

**Categories:** `all`, `sensitive`, `injection`, `commands`

### /tophant-clawvault-installer unconfigure-proxy

Remove ClawVault proxy environment variables from `openclaw-gateway.service` without restarting the gateway. Use this if OpenClaw conversations hang after proxy integration.

```bash
python3 SKILL_DIR/clawvault_manager.py unconfigure-proxy --json
```

### /tophant-clawvault-installer uninstall

Remove ClawVault completely (stops services, removes proxy, deletes venv and config).

```bash
python3 SKILL_DIR/clawvault_manager.py uninstall --json
python3 SKILL_DIR/clawvault_manager.py uninstall --keep-config --json
```

## Quick Examples

```bash
# Set the skill directory path
CV="python3 ~/.openclaw/workspace/skills/tophant-clawvault-installer/clawvault_manager.py"

# Install (one command handles everything)
$CV install --mode quick --json

# Check health
$CV health --json

# Generate rule
$CV generate-rule "Detect database passwords" --apply --json

# Apply scenario
$CV generate-rule --scenario customer_service --apply --json

# Run tests
$CV test --category all --json

# Uninstall
$CV uninstall --json
```

## Requirements

- Python 3.10+ (with venv module)
- Ports 8765, 8766 available
- No pip or system packages needed — the install script creates its own virtual environment

## Permissions

- `execute_command` - Run installation and ClawVault commands
- `write_files` - Create configuration files
- `read_files` - Read configurations
- `network` - Download packages and API calls

## Security Considerations

See [SECURITY.md](./SECURITY.md) for capability disclosure, threat model, and deployment guidance.

## Documentation

- **Full Guide**: https://github.com/tophant-ai/ClawVault/blob/main/doc/OPENCLAW_SKILL.md
- **中文文档**: https://github.com/tophant-ai/ClawVault/blob/main/doc/zh/OPENCLAW_SKILL.md
- **Repository**: https://github.com/tophant-ai/ClawVault

## License

MIT © 2026 Tophant SPAI Lab
