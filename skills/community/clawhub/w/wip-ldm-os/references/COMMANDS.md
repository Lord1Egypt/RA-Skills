# LDM OS Commands

| Command | What it does |
|---------|-------------|
| `ldm init` | Scaffold `~/.ldm/` and write version.json |
| `ldm install <org/repo>` | Clone, detect interfaces, deploy, register |
| `ldm install /path/to/repo` | Install from local path |
| `ldm install` | Update all registered extensions |
| `ldm doctor` | Check health of all extensions |
| `ldm status` | Show version and extension list |
| `ldm --version` | Show version |

All commands support `--dry-run` (preview changes) and `--json` (machine-readable output).
