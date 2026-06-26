# reference/ (CLI-focused)

Parent skill: **`$SKILL`** = directory above this folder (`superpicky-cli/`). Layout: see [SKILL.md](../SKILL.md).

## Files

| Path | Contents |
|------|----------|
| [cli-help-captured.txt](cli-help-captured.txt) | Frozen `superpicky_cli.py` / `birdid_cli.py` `--help` |
| [docs/cli-reference.md](docs/cli-reference.md) | Bilingual CLI summary |
| [docs/manifest机制说明.md](docs/manifest机制说明.md) | Manifest / reset behavior |
| [docs/BIRDID_OPTIMIZATION_GUIDE.md](docs/BIRDID_OPTIMIZATION_GUIDE.md) | BirdID performance notes |
| [requirements.txt](requirements.txt) / [requirements_base.txt](requirements_base.txt) / [requirements_cuda.txt](requirements_cuda.txt) | Dependency lists (mirror upstream) |
| [SOURCE.md](SOURCE.md) | Help-capture metadata; `install.sh` / pip notes |

## Commands (use absolute paths in automation)

```bash
SKILL="$(cd …/superpicky-cli && pwd)"
"${SKILL}/scripts/install.sh"
"${SKILL}/scripts/run.sh" process ~/Photos
"${SKILL}/scripts/run.sh" --region-query shanghai
"${SKILL}/scripts/capture-cli-help.sh"
"${SKILL}/.upstream/.venv/bin/python" "${SKILL}/scripts/ebird_region_query_test.py"
```
