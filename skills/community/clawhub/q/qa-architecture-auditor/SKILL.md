---
name: qa-architecture-auditor
description: >
  Perform forensic-level codebase analysis and generate comprehensive Quality Assurance
  and Testing Strategy Reports. Acts as Independent Principal QA Architect, Senior
  Software Security Auditor, and IT Systems Auditor. Uses zero-trust policy (ignores
  existing tests) and addresses all testing methodologies: Black Box, White Box,
  Manual, Automated, Unit, Integration, System, Functional, Smoke, Sanity, E2E,
  Regression, API, Database Integrity, Performance, Security, Usability, Compatibility,
  Accessibility, Localization, Acceptance, and Exploratory Testing. Use when needing
  a complete, independent testing strategy from scratch for any code repository.
metadata:
  openclaw:
    emoji: "🌀"
    files: ["scripts/analyze_repo.py"]
    requires:
      env: []
      bins: ["python3", "git"]
homepage: https://github.com/shifulegend/qa-architecture-auditor
---

# QA Architecture Auditor

This skill performs deep forensic analysis of codebases and produces exhaustive QA testing strategy reports with IT General Controls compliance. It provides independent baselines, vulnerability assessments, from-scratch test cases, and tooling recommendations for every testing methodology.

## What This Skill Does

- Analyzes repository structure, languages, frameworks, and dependencies
- Maps architecture and identifies critical risk areas
- Generates comprehensive testing strategy reports (HTML and Markdown formats)
- Provides specific, tailored test cases for each methodology
- Recommends industry-standard tools based on tech stack
- Ensures zero-trust approach: ignores all existing tests

## When to Use This Skill

Use this skill when you need:
- A complete QA strategy built from scratch (no reuse of existing tests)
- Forensic-level codebase analysis for security and quality compliance
- ITGC-ready testing documentation for system transitions
- Detailed testing matrix covering all standard and specialized methodologies
- Independent validation plan for unproven or legacy codebases

## Quick Start

Provide a local repository path or git URL:

```
qa-architecture-auditor --repo /path/to/repo --output report.html
```

The skill will:
1. Clone/access the repository
2. Analyze code structure, dependencies, and business logic
3. Identify high-risk modules and security vulnerabilities
4. Generate comprehensive testing strategy report
5. Provide tooling recommendations and specific test cases

## Command-Line Interface

```
usage: qa-audit [-h] --repo REPO [--output OUTPUT] [--format {html,md}] [--include-risk-prioritization] [--include-test-cases] [--include-tooling] [--exclude EXCLUDE] [--max-depth MAX_DEPTH] [--security-scan] [--compliance {itgc,soc2,iso27001,hipaa,gdpr}]

Perform forensic QA architecture analysis and generate testing strategy report.

options:
  -h, --help            show this help message and exit
  --repo REPO, -r REPO  Repository path or git URL
  --output OUTPUT, -o OUTPUT
                        Output file path (default: qa-report.html)
  --format {html,md}, -f {html,md}
                        Output format (default: html)
  --include-risk-prioritization
                        Include risk prioritization matrix
  --include-test-cases  Include detailed test cases for each methodology
  --include-tooling     Include tooling recommendations
  --exclude EXCLUDE, -e EXCLUDE
                        Comma-separated directories to exclude from analysis
  --max-depth MAX_DEPTH
                        Maximum directory traversal depth
  --security-scan       Perform security vulnerability scanning
  --compliance {itgc,soc2,iso27001,hipaa,gdpr}
                        Compliance framework to target
```

## Report Sections

The generated report includes:

1. **Executive Summary** - High-level findings and recommendations
2. **Codebase Analysis** - Languages, frameworks, dependencies, architecture patterns
3. **Risk Assessment** - High-risk modules and security concerns
4. **Testing Matrix** - Comprehensive strategies for each methodology:
   - Core Execution: Black Box, White Box, Manual, Automated
   - Functional & Structural: Unit, Integration, System, Functional, Smoke, Sanity, E2E, Regression, API, Database Integrity
   - Non-Functional: Performance, Security, Usability, Compatibility, Accessibility, Localization
   - Specialized: Acceptance (UAT), Exploratory Testing
5. **From-Scratch Test Cases** - Specific examples for critical paths
6. **Tooling Recommendations** - Best tools for the detected tech stack
7. **ITGC Compliance** - Controls and readiness assessments

## External Endpoints

The skill may make outbound network connections only for:

| Endpoint | Purpose | Data Sent |
|----------|---------|-----------|
| Git remotes (HTTPS/SSH) | Clone or fetch repository content | Authentication credentials if using SSH keys or HTTPS token; repository data read-only |

No other external services are contacted.

## Security & Privacy

- **Local processing**: All code analysis runs locally; no code is sent to third-party APIs.
- **Git operations**: When analyzing a remote repository, the skill performs `git clone` or `git fetch`. This may transmit repository data over the network and may require authentication if the repo is private.
- **Output**: The generated report is written to the local filesystem at the specified path.
- **Environment**: The skill does not require any environment variables. It does not modify system settings.

## Model Invocation Note

This skill runs as an autonomous CLI tool. Once invoked (via `/qa-audit` or direct shell), it performs the analysis without further model interaction. The heavy lifting is done by the Python script; no external AI inference is required during execution.

## Trust Statement

By using this skill, you trust that the code analysis and recommendations are accurate to the best of the tool's capabilities. The skill does not exfiltrate your code to external services beyond the Git operations you explicitly authorize. Only install and run this skill on codebases you have permission to analyze.

## Implementation Notes

- The skill uses static analysis to understand code without execution
- Supports major languages: JavaScript/TypeScript, Python, Java, Go, Rust, C#, Ruby, PHP
- Detects frameworks: React, Vue, Angular, Django, Flask, Spring, Express, etc.
- Generates risk scores based on complexity, external dependencies, and data handling
- Produces both human-readable HTML and machine-parsable Markdown

## References

For detailed methodology guidance, see:
- `references/methodologies.md` - Testing approach definitions and decision criteria
- `references/risk-assessment.md` - Risk scoring algorithm and vulnerability patterns
- `references/tooling-matrix.md` - Tool recommendations by language and framework
- `references/compliance-frameworks.md` - ITGC and audit requirements

## License

MIT

## Contributing

Improvements and contributions are welcome. Please open an issue or pull request on the GitHub repository.
