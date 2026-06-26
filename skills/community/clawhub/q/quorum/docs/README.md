# Quorum Documentation

Everything you need to use, configure, and extend Quorum.

---

## Getting Started

| Doc | Description |
|-----|-------------|
| [Quick Start](getting-started/QUICK_START.md) | Your first validation in 60 seconds |
| [Installation](getting-started/INSTALLATION.md) | Detailed setup, dependencies, and troubleshooting |
| [For Beginners](getting-started/FOR_BEGINNERS.md) | New to AI agent tooling? Start here |
| [Tutorial](getting-started/TUTORIAL.md) | Walkthrough of a full validation workflow |
| [Model Requirements](getting-started/MODEL_REQUIREMENTS.md) | Which models work with Quorum and why |

## Configuration

| Doc | Description |
|-----|-------------|
| [Config Reference](configuration/CONFIG_REFERENCE.md) | Every config option, rubric format, and CLI flag |

## Guides

| Doc | Description |
|-----|-------------|
| [Rubric Building Guide](guides/RUBRIC_BUILDING_GUIDE.md) | How to build rubrics for new domains step by step |
| [Cross-Artifact Design](guides/CROSS_ARTIFACT_DESIGN.md) | Checking consistency between related files |

## Architecture

| Doc | Description |
|-----|-------------|
| [SPEC.md](../SPEC.md) | Full architectural specification |
| [The Nine Critics](architecture/THE_NINE.md) | The critic architecture — what each one does and why |
| [Implementation Notes](architecture/IMPLEMENTATION.md) | Technical decisions and internals |

## Critics — Deep Dives

| Doc | Description |
|-----|-------------|
| [Security Critic Framework](critics/SECURITY_CRITIC_FRAMEWORK.md) | OWASP ASVS 5.0, CWE Top 25, NIST SA-11 coverage |
| [Code Hygiene Framework](critics/CODE_HYGIENE_FRAMEWORK.md) | ISO 25010:2023, CISQ quality model |
| [Tester Critic Brief](critics/TESTER_CRITIC_BRIEF.md) | L1 deterministic + L2 LLM claim verification |
| [Business Logic Validation](critics/SEC02_BUSINESS_LOGIC_VALIDATION.md) | SEC-02 workflow for business logic review |
| [Evidence Integrity](critics/SEC03_EVIDENCE_INTEGRITY.md) | SEC-03 evidence grounding and integrity |
| [Pipeline Resilience](critics/SEC05_PIPELINE_RESILIENCE.md) | SEC-05 crash recovery and fault tolerance |
| [Rubric Framework](critics/SEC06_RUBRIC_FRAMEWORK.md) | SEC-06 rubric architecture and extensibility |
| [Self-Validation Convergence](critics/SEC07_SELF_VALIDATION_CONVERGENCE.md) | SEC-07 Quorum validating itself |
| [PowerShell Coverage](critics/POWERSHELL_COVERAGE.md) | PSScriptAnalyzer integration details |

## Reviews & Research

| Doc | Description |
|-----|-------------|
| [External Reviews](reviews/EXTERNAL_REVIEWS.md) | Community and practitioner evaluations |
| [Changelog](CHANGELOG.md) | Version history and release notes |
| [Code of Conduct](CODE_OF_CONDUCT.md) | Community guidelines |

## Platform Ports

Quorum runs natively in other agent platforms:

| Port | Description |
|------|-------------|
| [Copilot CLI](../ports/copilot-cli/) | GitHub Copilot skill — stdlib-only pre-screen + 5 LLM critics |
| [Claude Code](../ports/claude-code/) | Claude Code subscription — zero API cost validation |

## Contributing

→ [CONTRIBUTING.md](../CONTRIBUTING.md)

We especially welcome rubric contributions for new domains.
