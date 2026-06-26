# Setup — Speedtest.net

## Requirements

| Dependency | Min Version | Required |
|------------|-------------|----------|
| Python 3 | 3.6+ | ✅ Yes |
| speedtest-cli | 2.x | ✅ Yes |

## Installation

**Install speedtest-cli before using this skill.**

### Option 1: pip

```bash
pip3 install speedtest-cli
```

### Option 2: apt (Debian/Ubuntu/Kali)

```bash
sudo apt update && sudo apt install speedtest-cli
```

> Note: apt versions may lag behind pip.

### Option 3: Homebrew (macOS)

```bash
brew install speedtest-cli
```

## Verify Installation

```bash
speedtest-cli --version
# Expected: speedtest-cli 2.x.x

python3 scripts/speedtest.py
# Expected: Ping / Download / Upload results
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: speedtest-cli` | Reinstall via `pip3 install speedtest-cli` |
| Permission denied | Use `pip3 install --user speedtest-cli` |
| Timeout / no server found | Check firewall; ensure outbound TCP 443 is open |

## Firewall Requirements

- **Outbound TCP 443** (HTTPS) to Speedtest servers
- No inbound ports required
