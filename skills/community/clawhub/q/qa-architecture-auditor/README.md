# QA Architecture Auditor

[![ClawHub](https://img.shields.io/badge/ClawHub-install-blue?logo=clawhub)](https://clawhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A forensic, zero-trust QA auditing skill for **OpenClaw**. This skill performs deep, independent analysis of any codebase and generates a comprehensive testing strategy report covering 20+ methodologies, including specialized categories like boundary analysis, fuzz testing, mutation testing, and full non-functional evaluation.

## Features

- **Forensic Codebase Analysis** – Detects languages, frameworks, architecture, dependencies, and maps modules with complexity metrics
- **Risk Assessment** – Scores modules (0-100) based on cyclomatic complexity, external calls, authentication handling, data persistence, cryptography, file I/O, and coupling
- **Security Surface Mapping** – Identifies authentication, authorization, input validation, output encoding, session management, cryptography, file ops, network ops, and database operations
- **Zero-Trust Policy** – Ignores existing tests; designs complete test plan from scratch
- **Multi-Format Reports** – Generates HTML or Markdown reports with statistics, risk tables, security surface, testing matrix, tooling recommendations, ITGC controls, and dependencies
- **Complete Methodology Coverage** – Black Box, White Box, Manual, Automated, Unit, Integration, System, Functional, Smoke, Sanity, E2E, Regression, API, Database, Performance, Security, Usability, Compatibility, Accessibility, Localization, Acceptance, Exploratory, Boundary, Monkey, Fuzz, Mutation, Non-Functional General
- **Compliance Ready** – Includes ITGC controls and mapping to SOC2, ISO27001, HIPAA, GDPR

## Installation

### From ClawHub (Recommended)

```bash
clawhub install shifulegend/qa-architecture-auditor
```

### Manual Install

Clone the repository into your OpenClaw workspace:

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/shifulegend/qa-architecture-auditor.git ~/.openclaw/workspace/skills/qa-architecture-auditor
```

## Usage

### In OpenClaw Chat (Slash Command)

```
/qa-audit --repo /path/to/local/repo --format html --output report.html
```

or for a remote repository:

```
/qa-audit --repo https://github.com/owner/repo.git --format md --output audit.md --security-scan --compliance soc2
```

### Direct CLI

```bash
qa-audit --repo ./myapp --output report.html
```

#### Common Options

- `--repo` – Local path or Git URL (required)
- `--output` – Output file path (default: `qa-report.html`)
- `--format` – `html` or `md` (default: `html`)
- `--include-test-cases` – Include detailed test cases (default: true)
- `--security-scan` – Enable additional security vulnerability scanning
- `--compliance` – Target compliance framework: `itgc`, `soc2`, `iso27001`, `hipaa`, `gdpr` (default: `itgc`)
- `--exclude` – Comma-separated directories to exclude (default: `node_modules,.git,__pycache__,.venv,venv,build,dist,target`)

See `qa-audit --help` for full options.

## Report Structure

The generated report includes:

1. **Executive Summary** – High-level findings
2. **Codebase Statistics** – Languages, file counts, dependencies
3. **Frameworks Detected** – Recognized frameworks
4. **Risk Assessment Table** – Prioritized modules by severity
5. **Security Surface Mapping** – Sensitive areas by domain
6. **Testing Methodology Matrix** – All methodologies with baseline, risk assessment, strategy, and from-scratch test cases
7. **Tooling Recommendations** – Language-specific toolchain suggestions
8. **ITGC Controls** – Audit-ready control checklist
9. **Dependencies Analysis** – Detected third‑party packages

## Example Output

```html
<!DOCTYPE html>
<html>... comprehensive report ...</html>
```

Or in Markdown:

```markdown
# Independent QA and Security Strategy Report

## Executive Summary
... etc ...
```

## How It Works

The skill performs static analysis of the repository to understand structure, complexity, and risk. It does not execute the application. It applies a zero‑trust policy: all test strategies are designed from first principles regardless of any existing tests. The result is an exhaustive, unbiased QA plan ready for implementation.

## Supported Languages & Frameworks

**Languages**: Python, JavaScript, TypeScript, Java, Go, Rust, C#, Ruby, PHP, Kotlin, Swift, Scala, C, C++, HTML, CSS, SQL, Shell

**Frameworks**: React, Vue, Angular, Django, Flask, FastAPI, Spring, Express, NestJS, Rails, Laravel, ASP.NET, and more.

## Security Considerations

- The skill may perform `git clone` or `git fetch` when analyzing remote URLs. It does not send your code to any external AI service.
- No environment variables are required.
- All analysis is local; reports are written to your filesystem.

See `SECURITY.md` for details (if available).

## Development

The skill consists of:

```
qa-architecture-auditor/
├── SKILL.md                 # Skill definition (OpenClaw spec)
├── scripts/
│   └── analyze_repo.py     # Core analysis engine (Python)
├── references/
│   ├── methodologies.md    # Detailed testing methodology guidance
│   ├── risk-assessment.md  # Risk scoring algorithm
│   ├── tooling-matrix.md   # Tool recommendations per language
│   └── compliance-frameworks.md  # Compliance mapping
├── README.md                # This file
├── LICENSE
└── .gitignore
```

To modify the analysis logic, edit `scripts/analyze_repo.py` and update the `QAAuditor` class.

### Testing the Skill

```bash
# Analyze a sample project
qa-audit --repo ./sample-app --format html --output sample-report.html
```

## License

MIT License – see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open issues or pull requests on GitHub.

## Credits

Published by [shifulegend](https://github.com/shifulegend) • Powered by [OpenClaw](https://openclaw.ai)
