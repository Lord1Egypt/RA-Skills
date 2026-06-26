---
name: esaa-security-audit
description: Execute deterministic, event-sourced security audits using ESAA-Security's LLM-based agent architecture with 95 checks across 16 security domains
triggers:
  - run a security audit using ESAA
  - audit this codebase with ESAA-Security
  - execute security checks with event sourcing
  - generate deterministic security report
  - verify security findings with ESAA
  - audit AI-generated code for vulnerabilities
  - run PARCER security playbooks
  - trace security audit with event store
---

# ESAA-Security Audit Skill

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## Overview

ESAA-Security applies the Event Sourcing for Autonomous Agents (ESAA) architecture to automated security auditing. It executes structured security audits across **16 security domains** with **95 executable checks**, governed by an immutable append-only event log. Every finding, classification, and remediation decision is recorded as a verifiable fact.

**Key differentiators:**
- **Deterministic audits** — same repository state produces same findings via event replay
- **Hallucination prevention** — schema-validated outputs with evidence requirements
- **Complete audit trail** — `.roadmap/activity.jsonl` records every check execution
- **Governed agents** — PARCER contracts enforce decision hygiene and token budgets
- **Verifiable reports** — SHA-256 hash verification from events to final output

## Installation

```bash
# Clone the repository
git clone https://github.com/elzobrito/ESAA-Security.git
cd ESAA-Security

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY=$YOUR_OPENAI_KEY
export ANTHROPIC_API_KEY=$YOUR_ANTHROPIC_KEY  # if using Claude
export AUDIT_TARGET_REPO="/path/to/repo"
```

**Requirements:**
- Python 3.9+
- LLM API access (OpenAI GPT-4, Anthropic Claude, or compatible)
- Target repository must be readable by the audit agent

## Repository Structure

```
.roadmap/                              # Event sourcing core
├── activity.jsonl                     # Immutable event store
├── roadmap.json                       # Derived audit progress
├── issues.json                        # Structured findings
├── AGENT_CONTRACT.yaml                # Agent boundaries
├── ORCHESTRATOR_CONTRACT.yaml         # State mutation rules
└── PROJECTION_SPEC.md                 # Event → state mapping

playbooks/
├── playbooks.security.json            # 95 security checks
└── global_input_contract.json         # Input requirements

reports/
├── phase1/                            # Reconnaissance
├── phase2/                            # Domain audits
├── phase3/                            # Risk classification
├── phase4/                            # Recommendations
└── final/                             # Compiled report
```

## Core Concepts

### Event Store (`activity.jsonl`)

Every audit action is an immutable event:

```json
{
  "event_id": "evt_001",
  "timestamp": "2026-05-14T10:30:00Z",
  "event_type": "task.started",
  "task_id": "SEC-010",
  "phase": "phase2",
  "domain": "authentication",
  "agent": "agent-impl"
}
```

```json
{
  "event_id": "evt_002",
  "timestamp": "2026-05-14T10:32:15Z",
  "event_type": "check.completed",
  "task_id": "SEC-010",
  "check_id": "AU-002",
  "status": "fail",
  "severity": "high",
  "finding": "Password stored without bcrypt/argon2",
  "evidence": {
    "file": "auth/user.py",
    "line": 45,
    "code_snippet": "user.password = request.form['password']"
  },
  "hash": "a3f8b2..."
}
```

### Read Model (`roadmap.json`)

Projection of audit progress (derived from events):

```json
{
  "version": "0.4.0",
  "phases": {
    "phase1": {
      "status": "done",
      "tasks": {
        "SEC-001": {"status": "done", "output": "reports/phase1/tech-stack.md"}
      }
    },
    "phase2": {
      "status": "in_progress",
      "domains": {
        "authentication": {
          "checks_passed": 5,
          "checks_failed": 3,
          "tasks": ["SEC-010", "SEC-011"]
        }
      }
    }
  }
}
```

## Running an Audit

### Phase 1: Reconnaissance

```python
# orchestrator.py
from esaa_security import Orchestrator, Agent

# Initialize orchestrator
orchestrator = Orchestrator(
    event_store=".roadmap/activity.jsonl",
    roadmap_path=".roadmap/roadmap.json",
    target_repo=os.getenv("AUDIT_TARGET_REPO")
)

# Initialize reconnaissance agent
agent_spec = Agent(
    role="agent-spec",
    contract_path=".roadmap/AGENT_CONTRACT.yaml",
    parcer_profile="PARCER_PROFILE.agent-spec.yaml"
)

# Execute reconnaissance phase
recon_tasks = ["SEC-001", "SEC-002", "SEC-003", "SEC-004"]
for task_id in recon_tasks:
    result = agent_spec.execute_task(task_id, orchestrator.get_context())
    orchestrator.validate_and_append(task_id, result)
```

**Task outputs:**
- `SEC-001`: Tech stack inventory (languages, frameworks, dependencies)
- `SEC-002`: Architecture map (components, trust boundaries)
- `SEC-003`: Data flow diagram (inputs, storage, outputs)
- `SEC-004`: Attack surface enumeration (endpoints, file uploads, APIs)

### Phase 2: Domain Audit Execution

```python
# Load security playbooks
with open("playbooks/playbooks.security.json") as f:
    playbooks = json.load(f)

# Initialize audit execution agent
agent_impl = Agent(
    role="agent-impl",
    contract_path=".roadmap/AGENT_CONTRACT.yaml",
    parcer_profile="PARCER_PROFILE.agent-impl.yaml"
)

# Execute checks for a domain (e.g., Authentication)
auth_checks = ["AU-001", "AU-002", "AU-003", "AU-004", "AU-005", "AU-006", "AU-007", "AU-008"]

for check_id in auth_checks:
    playbook = playbooks["checks"][check_id]
    
    result = agent_impl.execute_check(
        check_id=check_id,
        playbook=playbook,
        context=orchestrator.get_context()
    )
    
    # Orchestrator validates against schema
    orchestrator.validate_and_append(
        task_id=f"SEC-{check_id}",
        result=result
    )
```

**Example check result:**

```python
# agent_impl output for AU-002 (Password Storage)
{
    "check_id": "AU-002",
    "status": "fail",
    "severity": "critical",
    "title": "Weak Password Hashing",
    "description": "Passwords stored using SHA-256 instead of bcrypt/argon2",
    "evidence": {
        "files": ["auth/models.py"],
        "lines": [67],
        "code": "hashlib.sha256(password.encode()).hexdigest()"
    },
    "cwe": "CWE-916",
    "owasp": "A02:2021 Cryptographic Failures",
    "recommendation": "Replace SHA-256 with bcrypt (cost factor 12+)",
    "references": [
        "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"
    ]
}
```

### Phase 3: Risk Classification

```python
# Initialize QA/risk agent
agent_qa = Agent(
    role="agent-qa",
    contract_path=".roadmap/AGENT_CONTRACT.yaml",
    parcer_profile="PARCER_PROFILE.agent-qa.yaml"
)

# Classify vulnerabilities
findings = orchestrator.get_all_findings()
risk_matrix = agent_qa.classify_risks(findings)

# Write risk classification
with open("reports/phase3/risk-matrix.json", "w") as f:
    json.dump(risk_matrix, f, indent=2)
```

**Risk matrix output:**

```json
{
  "critical": [
    {"id": "AU-002", "cvss": 9.1, "exploitability": "high"}
  ],
  "high": [
    {"id": "IV-003", "cvss": 7.5, "exploitability": "medium"}
  ],
  "medium": [
    {"id": "SH-001", "cvss": 5.3, "exploitability": "low"}
  ],
  "remediation_priority": ["AU-002", "AZ-001", "IV-003"]
}
```

### Phase 4: Report Generation

```python
# Generate final report
report = agent_qa.generate_report(
    findings=orchestrator.get_all_findings(),
    risk_matrix=risk_matrix,
    context=orchestrator.get_context()
)

# Write final outputs
with open("reports/final/security-audit-report.md", "w") as f:
    f.write(report["markdown"])

with open("reports/final/security-audit-report.json", "w") as f:
    json.dump(report["structured"], f, indent=2)
```

## Event Replay and Verification

```python
# Verify audit determinism
from esaa_security import EventReplay, HashVerifier

# Replay events from scratch
replayer = EventReplay(event_store=".roadmap/activity.jsonl")
replayed_roadmap = replayer.project_roadmap()

# Compare hash
original_hash = HashVerifier.compute_hash(".roadmap/roadmap.json")
replayed_hash = HashVerifier.compute_hash(replayed_roadmap)

assert original_hash == replayed_hash, "Non-deterministic projection detected"
```

## Security Domain Coverage

### Critical Domains (8 total)

**Secrets & Configuration (SC-001 to SC-008):**
```python
# Example: Check for hardcoded secrets
playbook = {
    "check_id": "SC-001",
    "title": "Hardcoded Secrets Detection",
    "patterns": [
        r'password\s*=\s*["\'][^"\']+["\']',
        r'api_key\s*=\s*["\'][^"\']+["\']',
        r'AWS_SECRET_ACCESS_KEY'
    ],
    "severity": "critical"
}
```

**Authentication (AU-001 to AU-008):**
- Password hashing strength
- MFA enforcement
- Session token generation
- Credential transmission (HTTPS)

**Authorization (AZ-001 to AZ-006):**
- RBAC implementation
- Privilege escalation checks
- IDOR vulnerabilities
- API authorization

**Input Validation (IV-001 to IV-007):**
- SQL injection (ORM usage, parameterized queries)
- XSS (output encoding)
- Command injection
- Path traversal

**Data Security (DA-001 to DA-005):**
- Encryption at rest
- PII handling
- Data retention policies

### High Priority Domains (7 total)

**AI/LLM Security (AI-001 to AI-005):**
```python
# Example: Check for prompt injection vulnerabilities
playbook = {
    "check_id": "AI-001",
    "title": "Prompt Injection Defense",
    "checks": [
        "user_input_sanitization",
        "system_prompt_isolation",
        "output_validation",
        "context_length_limits"
    ],
    "severity": "high"
}
```

## Configuration

### Agent Contract (`.roadmap/AGENT_CONTRACT.yaml`)

```yaml
agent_impl:
  can:
    - read: ["**/*.py", "**/*.js", "**/*.java", "config/**"]
    - write: ["reports/phase2/**"]
    - execute_checks: true
  cannot:
    - write: [".roadmap/activity.jsonl", ".roadmap/roadmap.json"]
    - modify_state: true
    - append_events: true
  output_schema: "agent_result.schema.json"
  token_budget: 8000
```

### PARCER Profile (Token Budgets)

```yaml
# PARCER_PROFILE.agent-impl.yaml
budget:
  max_tokens: 8000
  per_check: 500
  context_window: 4000
  
fallback:
  strategy: "map_reduce"
  chunk_size: 2000
  
validation:
  require_evidence: true
  require_cwe_mapping: true
  schema: "agent_result.schema.json"
```

## Programmatic Usage

### Custom Audit Pipeline

```python
from esaa_security import AuditPipeline, SecurityDomain

# Define custom domain subset
domains = [
    SecurityDomain.AUTHENTICATION,
    SecurityDomain.AUTHORIZATION,
    SecurityDomain.INPUT_VALIDATION,
    SecurityDomain.AI_LLM_SECURITY
]

# Initialize pipeline
pipeline = AuditPipeline(
    target_repo=os.getenv("AUDIT_TARGET_REPO"),
    domains=domains,
    event_store=".roadmap/activity.jsonl"
)

# Execute with streaming
for event in pipeline.execute_streaming():
    if event["event_type"] == "check.completed":
        print(f"✓ {event['check_id']}: {event['status']}")
    elif event["event_type"] == "finding.detected":
        print(f"⚠ {event['severity']}: {event['title']}")

# Get final report
report = pipeline.get_report()
```

### Query Event Store

```python
from esaa_security import EventQuery

query = EventQuery(".roadmap/activity.jsonl")

# Find all critical findings
critical = query.filter(
    event_type="check.completed",
    status="fail",
    severity="critical"
).to_list()

# Get domain coverage
coverage = query.aggregate_by("domain")
# {"authentication": 8, "authorization": 6, ...}

# Audit timeline
timeline = query.timeline(group_by="1h")
```

## Common Patterns

### Incremental Audit (Skip Completed)

```python
roadmap = orchestrator.load_roadmap()

for task_id in all_tasks:
    if roadmap.get_task_status(task_id) == "done":
        print(f"Skip {task_id} (already completed)")
        continue
    
    result = agent.execute_task(task_id)
    orchestrator.validate_and_append(task_id, result)
```

### Parallel Domain Execution

```python
from concurrent.futures import ThreadPoolExecutor

def audit_domain(domain_name, checks):
    agent = Agent(role="agent-impl")
    results = []
    for check_id in checks:
        result = agent.execute_check(check_id)
        results.append(result)
    return domain_name, results

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {
        executor.submit(audit_domain, domain, checks): domain
        for domain, checks in domain_map.items()
    }
    
    for future in as_completed(futures):
        domain, results = future.result()
        for result in results:
            orchestrator.validate_and_append(result)
```

### Export to SARIF

```python
from esaa_security import SARIFExporter

exporter = SARIFExporter(event_store=".roadmap/activity.jsonl")
sarif = exporter.to_sarif()

with open("security-audit.sarif", "w") as f:
    json.dump(sarif, f, indent=2)
```

## Troubleshooting

### Issue: Schema Validation Failure

```python
# Error: agent_result failed schema validation
# Fix: Check output structure matches agent_result.schema.json

# Validate manually
from jsonschema import validate
import json

with open(".roadmap/agent_result.schema.json") as f:
    schema = json.load(f)

with open("reports/phase2/results/SEC-010.json") as f:
    result = json.load(f)

validate(instance=result, schema=schema)  # Raises ValidationError with details
```

### Issue: Event Store Corruption

```python
# Verify event store integrity
from esaa_security import EventStoreValidator

validator = EventStoreValidator(".roadmap/activity.jsonl")
errors = validator.validate()

if errors:
    print("Corrupt events:")
    for err in errors:
        print(f"Line {err['line']}: {err['message']}")
else:
    print("✓ Event store valid")
```

### Issue: Non-Deterministic Replay

```python
# Debug: Find which event causes divergence
from esaa_security import ReplayDebugger

debugger = ReplayDebugger(
    event_store=".roadmap/activity.jsonl",
    expected_roadmap=".roadmap/roadmap.json"
)

divergent_event = debugger.find_divergence()
print(f"Divergence at event: {divergent_event['event_id']}")
print(f"Expected: {divergent_event['expected_state']}")
print(f"Actual: {divergent_event['actual_state']}")
```

### Issue: Agent Exceeds Token Budget

```python
# Error: Agent exceeded 8000 token budget
# Fix: Enable Map-Reduce fallback in PARCER profile

# PARCER_PROFILE.agent-impl.yaml
fallback:
  strategy: "map_reduce"
  chunk_size: 2000
  max_chunks: 10
  
# Or reduce context window
budget:
  context_window: 3000  # from 4000
```

### Issue: Missing Evidence in Findings

```python
# Orchestrator rejects findings without evidence
# Fix: Ensure agent output includes code snippets

# Valid finding structure
{
    "check_id": "IV-001",
    "status": "fail",
    "evidence": {
        "file": "api/routes.py",
        "line": 23,
        "code_snippet": "query = f\"SELECT * FROM users WHERE id={user_id}\""
    }
}
```

## Integration with CI/CD

### GitHub Actions

```yaml
# .github/workflows/security-audit.yml
name: ESAA Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run ESAA-Security Audit
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          AUDIT_TARGET_REPO: ${{ github.workspace }}
        run: |
          pip install -r requirements.txt
          python orchestrator.py --full-audit
      
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: security-audit.sarif
      
      - name: Fail on Critical Findings
        run: |
          python -c "import json; \
          report = json.load(open('reports/final/security-audit-report.json')); \
          exit(1 if report['critical_count'] > 0 else 0)"
```

## Best Practices

1. **Always verify event store integrity** before generating reports
2. **Use deterministic replay** to validate audit reproducibility
3. **Configure token budgets** per agent role to prevent runaway costs
4. **Enable Map-Reduce fallback** for large repositories (>10k LOC)
5. **Review PARCER profiles** to adjust validation strictness
6. **Export to SARIF** for GitHub Security tab integration
7. **Archive `.roadmap/` directory** for audit forensics

## References

- [ESAA Paper (arXiv:2602.23193)](https://arxiv.org/abs/2602.23193)
- [ESAA-Security Paper (arXiv:2603.06365)](https://arxiv.org/abs/2603.06365)
- [PARCER Paper (arXiv:2603.00856)](https://arxiv.org/abs/2603.00856)
- [PARCER v1.6.0 Security Auditor](docs/PARCER_v1.6.0-security-audit.yaml)
