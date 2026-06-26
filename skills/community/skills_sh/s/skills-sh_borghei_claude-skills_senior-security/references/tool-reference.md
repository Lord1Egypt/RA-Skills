# Tool Reference

Read this when you need the full flag tables, usage examples, and output-format details for the bundled scripts (`threat_modeler.py`, `secret_scanner.py`).

## Scripts Overview

| Script | Purpose | Usage |
|--------|---------|-------|
| [threat_modeler.py](../scripts/threat_modeler.py) | STRIDE threat analysis with risk scoring | `python threat_modeler.py --component "Authentication"` |
| [secret_scanner.py](../scripts/secret_scanner.py) | Detect hardcoded secrets and credentials | `python secret_scanner.py /path/to/project` |

**Threat Modeler Features:**
- STRIDE analysis for any system component
- DREAD risk scoring
- Mitigation recommendations
- JSON and text output formats
- Interactive mode for guided analysis

**Secret Scanner Features:**
- Detects AWS, GCP, Azure credentials
- Finds API keys and tokens (GitHub, Slack, Stripe)
- Identifies private keys and passwords
- Supports 20+ secret patterns
- CI/CD integration ready

---

## threat_modeler.py

**Purpose:** Performs STRIDE threat analysis on system components with DREAD risk scoring, mitigation recommendations, and structured reporting.

**Usage:**

```bash
python threat_modeler.py --component "User Authentication"
python threat_modeler.py --component "API Gateway" --assets "user_data,tokens" --json
python threat_modeler.py --component "Database" --output report.txt
python threat_modeler.py --interactive
python threat_modeler.py --list-threats
```

**Flags:**

| Flag | Short | Type | Required | Description |
|------|-------|------|----------|-------------|
| `--component` | `-c` | string | Yes (unless `--interactive` or `--list-threats`) | Component to analyze (e.g., "User Authentication", "API Gateway", "Database") |
| `--assets` | `-a` | string | No | Comma-separated list of assets to protect |
| `--json` | | flag | No | Output report as JSON instead of text |
| `--interactive` | `-i` | flag | No | Run guided interactive threat modeling session |
| `--list-threats` | `-l` | flag | No | List all threats in the built-in database |
| `--output` | `-o` | string | No | Write report to file path instead of stdout |

**Example:**

```bash
$ python threat_modeler.py --component "API Gateway" --json --output api-threats.json
Report written to api-threats.json
```

**Output Formats:**
- **Text (default):** Structured report grouped by STRIDE category with risk scores, DREAD ratings, attack vectors, and mitigations.
- **JSON (`--json`):** Machine-readable object containing `component`, `analysis_date`, `summary` (counts by risk level), and `threats` array with full DREAD breakdown per threat.

---

## secret_scanner.py

**Purpose:** Detects hardcoded secrets, API keys, credentials, and private keys in source code. Supports 20+ secret patterns across cloud providers (AWS, GCP, Azure), authentication tokens (GitHub, GitLab, Slack, Stripe, Twilio, SendGrid), cryptographic keys, and generic credential patterns. Exits with code 1 when critical or high findings are present, making it CI/CD-ready.

**Usage:**

```bash
python secret_scanner.py /path/to/project
python secret_scanner.py /path/to/file.py
python secret_scanner.py /path/to/project --format json --output report.json
python secret_scanner.py /path/to/project --severity critical
python secret_scanner.py --list-patterns
```

**Flags:**

| Flag | Short | Type | Required | Description |
|------|-------|------|----------|-------------|
| `path` | | positional | Yes (unless `--list-patterns`) | File or directory path to scan |
| `--format` | `-f` | choice: `text`, `json` | No | Output format (default: `text`) |
| `--output` | `-o` | string | No | Write report to file path instead of stdout |
| `--list-patterns` | `-l` | flag | No | List all detection patterns with IDs and severity |
| `--severity` | `-s` | choice: `critical`, `high`, `medium`, `low` | No | Minimum severity threshold to report (includes all levels from critical down to the specified level) |

**Example:**

```bash
$ python secret_scanner.py ./src --severity high --format json
{
  "target": "./src",
  "scan_date": "2026-03-21T10:30:00",
  "summary": { "total": 2, "by_severity": { "critical": 1, "high": 1, "medium": 0, "low": 0 } },
  "findings": [ ... ]
}
```

**Output Formats:**
- **Text (default):** Severity-grouped report showing pattern ID, file path with line number, masked match text, and remediation recommendation.
- **JSON (`--format json`):** Machine-readable object with `target`, `scan_date`, `summary` (counts by severity), and `findings` array. Each finding includes `pattern_id`, `name`, `severity`, `file_path`, `line_number`, `matched_text` (masked), and `recommendation`.
