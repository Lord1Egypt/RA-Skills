# REP CLI

Resource Evaluation Platform Command Line Interface

## Installation

### Global Installation

```bash
npm install -g rep-cli
```

### Local Installation

```bash
npm install rep-cli
```

### Development Installation

```bash
git clone <repository-url>
cd rep-cli
npm install
```

## Usage

### Initialize a New Project

```bash
rep init [options]
```

Options:
- `-n, --name <name>` - Project name (default: rep-project)
- `-t, --template <template>` - Template to use (default: default)

Example:
```bash
rep init --name my-project --template enterprise
```

### Validate Configuration

```bash
rep validate [options]
```

Options:
- `-c, --config <path>` - Config file path (default: ./rep.config.js)
- `-v, --verbose` - Verbose output

Example:
```bash
rep validate --config ./my-config.js --verbose
```

### Show Statistics

```bash
rep stats [options]
```

Options:
- `-j, --json` - Output as JSON
- `-p, --pretty` - Pretty print output

Example:
```bash
rep stats --json
```

### Generate Report

```bash
rep report [options]
```

Options:
- `-o, --output <file>` - Output file (default: rep-report.html)
- `-f, --format <format>` - Format: html, json, markdown (default: html)
- `-s, --summary` - Show summary only

Example:
```bash
rep report --format markdown --output report.md
```

### Emit Events

```bash
rep emit [options]
```

Options:
- `-e, --event <event>` - Event type (default: info)
- `-m, --message <message>` - Event message
- `-r, --recipients <list>` - Comma-separated recipients

Example:
```bash
rep emit --event alert --message "Deployment complete" --recipients team@example.com
```

## Commands Overview

| Command | Description |
|---------|-------------|
| `init` | Initialize a new REP project |
| `validate` | Validate REP configuration and resources |
| `stats` | Show statistics for REP resources |
| `report` | Generate REP evaluation report |
| `emit` | Emit REP events or notifications |

## Configuration

REP CLI looks for configuration in:
1. `./rep.config.js` (current directory)
2. `./package.json` (rep config section)
3. Environment variables

## License

MIT
