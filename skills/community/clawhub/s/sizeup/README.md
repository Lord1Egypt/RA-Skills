# sizeup

Disk usage analyzer with tree view, large file finder, and extension breakdown. Like `du` but actually readable. Pure Python, zero dependencies.

## Usage

```bash
# Tree view of current directory
sizeup

# Analyze specific path
sizeup /var/log --depth 2

# Only show items >= 10MB
sizeup --min 10M

# Top 20 largest files
sizeup /home --top 20

# Extension breakdown
sizeup . --ext

# JSON output
sizeup --top 10 --json
```

## Features

- **Color-coded tree** — red (≥1GB), yellow (≥100MB), cyan (≥10MB)
- **Large file finder** — `--top N` finds the biggest files fast
- **Extension breakdown** — see what file types eat your disk
- **Depth control** — `--depth N` limits recursion
- **Size filter** — `--min 10M` hides small items
- **JSON output** for scripting
- **Zero dependencies**

## License

MIT
