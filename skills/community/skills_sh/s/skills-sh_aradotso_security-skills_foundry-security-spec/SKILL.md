---
name: foundry-security-spec
description: Implement Cisco's Foundry specification for agentic AI security evaluation systems with multi-agent architecture
triggers:
  - implement foundry security evaluation
  - set up agentic security testing
  - create foundry spec system
  - build security evaluation agents
  - configure foundry security roles
  - design ai vulnerability discovery
  - implement foundry detector agents
  - create security finding workflow
---

# Foundry Security Spec

> Skill by [ara.so](https://ara.so) — Security Skills collection.

Foundry is an open specification from Cisco for building agentic AI security evaluation systems. It defines a multi-agent architecture with 8 core roles and 5 extension roles that coordinate to discover, validate, and report security findings. This is NOT a tool to install—it's a blueprint for building your own security evaluation system.

## Core Concepts

Foundry provides:
- **Architecture**: 8 core agent roles (Orchestrator, Planner, Navigator, Detector, Explorer, Validator, Investigator, Publisher)
- **Finding Lifecycle**: States, verdicts, evidence gates, fingerprinting
- **Coordination Model**: Atomic claims, heartbeat liveness, auto-blocking
- **Governance**: Sandboxing, budgets, yield-gated auto-stop, coverage gates
- **Detection-to-Prevention Flywheel**: Rules catch known issues, explorers find new ones, gaps become new rules

Works with CodeGuard rule format for portable detection rules that transfer between evaluation and prevention.

## Repository Structure

```
foundry-security-spec/
├── spec.md              # Main specification (~130 functional requirements)
├── constitution.md      # 11 inviolable principles
├── GLOSSARY.md         # Terminology reference
└── README.md           # Implementation guide
```

## Implementation Workflow

### Step 1: Read the Constitution

```bash
# The constitution contains 11 principles that constrain all implementations
cat constitution.md
```

Key principles to understand:
- **No unsupervised execution**: Every finding requires explicit confirmation
- **Evidence-gated findings**: Claims without evidence don't become findings
- **Reproducibility**: Every finding must be reproducible from its evidence
- **Atomic progress**: Claims are indivisible units of work
- **Fail-safe defaults**: When stuck, escalate or yield—never guess

### Step 2: Install spec-kit

```bash
# In your project directory
npm install -g @github/spec-kit
# or follow spec-kit installation for your coding agent

# Initialize in your project
cd your-security-eval-project
speckit init
```

This creates `.specify/` directory for spec-driven development.

### Step 3: Register the Constitution

```bash
# Copy constitution into spec-kit memory
cp path/to/foundry-security-spec/constitution.md .specify/memory/constitution.md

# Register it with your agent
/speckit.constitution
# Select "adopt existing constitution" when prompted
```

### Step 4: Seed Your Specification

```bash
# Create specs directory
mkdir -p specs/001-foundry

# Copy seed specification
cp path/to/foundry-security-spec/spec.md specs/001-foundry/spec.md
```

### Step 5: Clarify for Your Environment

```bash
# Run clarification workflow
/speckit.clarify
```

Answer questions in these categories:

**Identity & Scope:**
```
Q: What is your system name?
A: acme-security-eval

Q: Does "authorized evaluation with source access" hold?
A: yes

Q: Merge, split, or keep the 8 core roles as-is?
A: keep as-is for first implementation
```

**Integration Choices:**
```
Q: Version control system?
A: GitLab self-hosted at https://gitlab.internal

Q: Issue tracker?
A: Jira at https://jira.acme.com

Q: LLM provider?
A: OpenAI via internal gateway at https://llm.internal/v1

Q: Datastore?
A: PostgreSQL

Q: Isolation runtime?
A: Docker containers with network isolation

Q: Deployment target?
A: Kubernetes cluster
```

**Policy Choices:**
```
Q: Severity taxonomy?
A: Critical/High/Medium/Low matching our existing CVE scale

Q: Surface needs-review findings?
A: No, validator rejects inconclusive findings

Q: Label naming convention?
A: foundry:role/name format
```

**Extension Scope (recommend NO for first build):**
```
Q: Include Attack-Mapper role?
A: no

Q: Include Regression-Tracker role?
A: no

Q: Include Compliance-Mapper role?
A: no

Q: Include Impact-Assessor role?
A: no

Q: Include Remediation-Drafter role?
A: no
```

### Step 6: Generate Your Specification

```bash
# Harden clarified spec
/speckit.specify

# Check for remaining clarifications
/speckit.clarify

# Repeat until no markers remain
```

Your `specs/001-foundry/spec.md` now contains YOUR specification with decisions filled in.

### Step 7: Implement

```bash
# Generate technical design
/speckit.plan

# Generate task backlog
/speckit.tasks

# Start implementation
/speckit.implement
```

## Agent Role Implementation Examples

### Orchestrator Pattern

```python
# orchestrator.py
import asyncio
from typing import List, Dict
from datastore import FindingStore, ClaimStore
from agents import Planner, Detector, Explorer, Validator

class Orchestrator:
    def __init__(self, 
                 llm_client,
                 finding_store: FindingStore,
                 claim_store: ClaimStore,
                 budget_manager):
        self.llm = llm_client
        self.findings = finding_store
        self.claims = claim_store
        self.budget = budget_manager
        
        # Initialize agent roles
        self.planner = Planner(llm_client)
        self.detector = Detector(llm_client, rules_corpus)
        self.explorer = Explorer(llm_client)
        self.validator = Validator(llm_client)
    
    async def evaluate(self, target_repo: str) -> Dict:
        """Run complete evaluation coordinating all agents."""
        
        # FR-001: Orchestrator creates evaluation record
        eval_id = await self.findings.create_evaluation(
            target=target_repo,
            status="running"
        )
        
        try:
            # FR-010: Planner creates work plan
            plan = await self.planner.create_plan(target_repo)
            await self.claims.store_plan(eval_id, plan)
            
            # FR-020: Distribute work to detection and exploration
            detection_task = asyncio.create_task(
                self.run_detection(eval_id, plan)
            )
            exploration_task = asyncio.create_task(
                self.run_exploration(eval_id, plan)
            )
            
            # FR-005: Monitor heartbeats and budgets
            monitor_task = asyncio.create_task(
                self.monitor_health(eval_id)
            )
            
            # Wait for completion
            await asyncio.gather(
                detection_task,
                exploration_task,
                monitor_task
            )
            
            # FR-006: Check coverage gate before completion
            coverage = await self.calculate_coverage(eval_id)
            if coverage < plan.required_coverage:
                raise InsufficientCoverageError(
                    f"Coverage {coverage}% < required {plan.required_coverage}%"
                )
            
            # Mark evaluation complete
            await self.findings.update_evaluation(
                eval_id,
                status="complete",
                coverage=coverage
            )
            
            return {
                "eval_id": eval_id,
                "status": "complete",
                "findings": await self.findings.count(eval_id),
                "coverage": coverage
            }
            
        except Exception as e:
            # FR-008: Fail-safe: mark evaluation failed
            await self.findings.update_evaluation(
                eval_id,
                status="failed",
                error=str(e)
            )
            raise
    
    async def monitor_health(self, eval_id: str):
        """Monitor agent heartbeats and budgets."""
        while True:
            await asyncio.sleep(30)
            
            # FR-007: Check heartbeats
            stalled = await self.claims.find_stalled_claims(
                eval_id,
                heartbeat_threshold=300  # 5 minutes
            )
            
            for claim in stalled:
                # FR-007: Auto-block stalled claims
                await self.claims.block_claim(
                    claim.id,
                    reason="heartbeat_timeout"
                )
            
            # FR-009: Check budget exhaustion
            if await self.budget.is_exhausted(eval_id):
                await self.findings.update_evaluation(
                    eval_id,
                    status="budget_exhausted"
                )
                break
```

### Detector with CodeGuard Rules

```python
# detector.py
from typing import List
from codeguard import RuleEngine, Finding as CodeGuardFinding
from models import Claim, Finding

class Detector:
    def __init__(self, llm_client, rules_corpus_path: str):
        self.llm = llm_client
        # FR-030: Load CodeGuard rules
        self.rule_engine = RuleEngine.load(rules_corpus_path)
    
    async def process_claim(self, claim: Claim) -> List[Finding]:
        """Apply detection rules to a code claim."""
        
        # FR-031: Extract relevant code from claim
        code_units = await self.extract_code_units(claim)
        
        findings = []
        
        for unit in code_units:
            # FR-032: Run rule engine
            rule_hits = await self.rule_engine.evaluate(
                code=unit.content,
                context=unit.context,
                language=unit.language
            )
            
            for hit in rule_hits:
                # FR-033: Convert rule hit to finding
                finding = Finding(
                    claim_id=claim.id,
                    rule_id=hit.rule_id,
                    severity=hit.severity,
                    weakness_id=hit.cwe_id,
                    location=hit.location,
                    evidence={
                        "rule_match": hit.matched_pattern,
                        "code_snippet": unit.content,
                        "line_range": hit.line_range
                    },
                    verdict="confirmed",  # Rules are deterministic
                    status="validated"
                )
                findings.append(finding)
                
                # FR-034: Record coverage
                await self.record_coverage(claim.id, unit.path)
        
        return findings
    
    async def extract_code_units(self, claim: Claim):
        """Use LLM to identify relevant code units in claim scope."""
        
        prompt = f"""
        Claim: {claim.description}
        Scope: {claim.scope}
        
        Identify all code units (functions, methods, classes) that should be
        evaluated for security issues related to this claim.
        
        Return as JSON array with: path, name, start_line, end_line
        """
        
        response = await self.llm.complete(prompt)
        return parse_code_units(response)
```

### Explorer for Novel Issues

```python
# explorer.py
import asyncio
from typing import List, Optional
from models import Claim, Finding, RuleGap

class Explorer:
    def __init__(self, llm_client, sandbox_runtime):
        self.llm = llm_client
        self.sandbox = sandbox_runtime
    
    async def investigate_claim(self, claim: Claim) -> List[Finding]:
        """Creative exploration beyond static rules."""
        
        findings = []
        
        # FR-040: Generate investigation hypotheses
        hypotheses = await self.generate_hypotheses(claim)
        
        for hypothesis in hypotheses:
            # FR-041: Execute in isolated sandbox
            async with self.sandbox.session() as session:
                result = await self.test_hypothesis(
                    session,
                    hypothesis,
                    claim
                )
                
                if result.is_vulnerability:
                    # FR-042: Evidence-gated finding
                    if not result.has_reproduction:
                        # Don't create finding without evidence
                        continue
                    
                    finding = Finding(
                        claim_id=claim.id,
                        severity=result.severity,
                        weakness_id=result.weakness_id,
                        description=result.description,
                        evidence=result.evidence,
                        verdict="needs-validation",
                        status="pending"
                    )
                    findings.append(finding)
                    
                    # FR-043: Check if rules missed this
                    if await self.should_have_detected(finding):
                        await self.record_rule_gap(finding)
        
        return findings
    
    async def generate_hypotheses(self, claim: Claim) -> List[Dict]:
        """Use LLM to generate creative test hypotheses."""
        
        prompt = f"""
        You are exploring code for security issues that static rules may miss.
        
        Claim: {claim.description}
        Code scope: {claim.scope}
        
        Generate 3-5 security hypotheses to test:
        - Focus on logic bugs, state confusion, race conditions
        - Consider what rules can't express (context-dependent issues)
        - Prioritize high-impact scenarios
        
        For each hypothesis provide:
        - What to test
        - Why it might be vulnerable
        - How to reproduce if vulnerable
        
        Return as JSON array.
        """
        
        response = await self.llm.complete(
            prompt,
            temperature=0.7  # Higher for creative exploration
        )
        return parse_hypotheses(response)
    
    async def record_rule_gap(self, finding: Finding):
        """Record that rules failed to detect this issue."""
        
        gap = RuleGap(
            finding_id=finding.id,
            weakness_id=finding.weakness_id,
            pattern=finding.evidence.get("vulnerable_pattern"),
            reason="explorer_found_missed_by_detector",
            suggested_rule=await self.draft_rule(finding)
        )
        
        # FR-044: Feed into rule corpus improvement
        await self.rule_gaps.store(gap)
```

### Validator for Finding Confirmation

```python
# validator.py
from models import Finding, ValidationResult

class Validator:
    def __init__(self, llm_client, sandbox_runtime):
        self.llm = llm_client
        self.sandbox = sandbox_runtime
    
    async def validate_finding(self, finding: Finding) -> ValidationResult:
        """Reproduce and confirm finding from evidence."""
        
        # FR-050: Check evidence completeness
        if not self.has_sufficient_evidence(finding):
            return ValidationResult(
                verdict="rejected",
                reason="insufficient_evidence"
            )
        
        # FR-051: Attempt reproduction
        async with self.sandbox.session() as session:
            reproduced = await self.reproduce_issue(
                session,
                finding.evidence
            )
            
            if not reproduced:
                return ValidationResult(
                    verdict="rejected",
                    reason="not_reproducible"
                )
            
            # FR-052: Verify severity assessment
            actual_severity = await self.assess_severity(
                session,
                finding
            )
            
            if actual_severity != finding.severity:
                finding.severity = actual_severity
                finding.evidence["severity_adjustment"] = {
                    "original": finding.severity,
                    "validated": actual_severity
                }
            
            # FR-053: Generate fingerprint for deduplication
            fingerprint = await self.generate_fingerprint(finding)
            
            return ValidationResult(
                verdict="confirmed",
                fingerprint=fingerprint,
                severity=actual_severity,
                reproduction_evidence=session.get_transcript()
            )
    
    def has_sufficient_evidence(self, finding: Finding) -> bool:
        """Check if finding has required evidence."""
        required = ["location", "description"]
        
        if finding.severity in ["critical", "high"]:
            required.extend(["reproduction_steps", "impact"])
        
        return all(k in finding.evidence for k in required)
    
    async def generate_fingerprint(self, finding: Finding) -> str:
        """Create stable fingerprint for deduplication."""
        
        # FR-054: Fingerprint combines weakness + location + root cause
        components = [
            finding.weakness_id,
            finding.location.get("file_path"),
            finding.location.get("function_name"),
            finding.evidence.get("root_cause_pattern")
        ]
        
        fingerprint_input = "|".join(str(c) for c in components if c)
        return hashlib.sha256(fingerprint_input.encode()).hexdigest()[:16]
```

### Publisher for Issue Tracker Integration

```python
# publisher.py
import aiohttp
from typing import Dict
from models import Finding

class Publisher:
    def __init__(self, issue_tracker_config: Dict):
        self.tracker_url = issue_tracker_config["url"]
        self.project_key = issue_tracker_config["project"]
        self.api_token = issue_tracker_config["token"]  # From env: ISSUE_TRACKER_TOKEN
    
    async def publish_finding(self, finding: Finding) -> str:
        """Create issue in tracker for confirmed finding."""
        
        # FR-060: Only publish confirmed findings
        if finding.verdict != "confirmed":
            raise ValueError(f"Cannot publish {finding.verdict} finding")
        
        # FR-061: Check for existing issue via fingerprint
        existing = await self.find_existing_issue(finding.fingerprint)
        if existing:
            return existing.issue_id
        
        # FR-062: Format issue according to tracker schema
        issue_body = self.format_issue(finding)
        
        # FR-063: Create issue
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.tracker_url}/rest/api/2/issue",
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                },
                json=issue_body
            ) as resp:
                resp.raise_for_status()
                result = await resp.json()
                issue_id = result["key"]
        
        # FR-064: Update finding with issue reference
        finding.issue_id = issue_id
        finding.status = "published"
        await finding.save()
        
        return issue_id
    
    def format_issue(self, finding: Finding) -> Dict:
        """Format finding as issue tracker ticket."""
        
        description = f"""
        *Security Finding from Foundry Evaluation*
        
        *Severity:* {finding.severity.upper()}
        *Weakness:* {finding.weakness_id}
        *Location:* {finding.location.get('file_path')}:{finding.location.get('line_number')}
        
        h3. Description
        {finding.description}
        
        h3. Evidence
        {self.format_evidence(finding.evidence)}
        
        h3. Reproduction
        {finding.evidence.get('reproduction_steps', 'See evidence above')}
        
        ---
        Fingerprint: {finding.fingerprint}
        Evaluation ID: {finding.eval_id}
        """
        
        return {
            "fields": {
                "project": {"key": self.project_key},
                "summary": f"[{finding.severity.upper()}] {finding.weakness_id}: {finding.get_short_description()}",
                "description": description,
                "issuetype": {"name": "Security Vulnerability"},
                "priority": {"name": self.map_severity_to_priority(finding.severity)},
                "labels": [
                    f"foundry:eval:{finding.eval_id}",
                    f"foundry:weakness:{finding.weakness_id}",
                    f"foundry:fingerprint:{finding.fingerprint}"
                ]
            }
        }
```

## Configuration Examples

### Evaluation Configuration

```yaml
# config/evaluation.yaml
evaluation:
  name: "acme-security-eval"
  
  # Orchestrator settings
  orchestrator:
    max_concurrent_claims: 10
    heartbeat_interval: 60
    stall_threshold: 300
    
  # Budget limits
  budget:
    max_tokens: 10000000
    max_duration_hours: 48
    per_agent_token_limit: 1000000
    
  # Coverage requirements
  coverage:
    required_percentage: 80
    scope:
      - src/**/*.py
      - lib/**/*.js
    exclude:
      - tests/**
      - docs/**
  
  # Agent roles enabled
  agents:
    core:
      - orchestrator
      - planner
      - navigator
      - detector
      - explorer
      - validator
      - investigator
      - publisher
    extensions: []  # Start with core only
  
  # Integration endpoints
  integrations:
    llm:
      provider: "openai"
      endpoint: "${LLM_GATEWAY_URL}"
      model: "gpt-4"
      api_key: "${LLM_API_KEY}"
    
    vcs:
      type: "gitlab"
      url: "${GITLAB_URL}"
      token: "${GITLAB_TOKEN}"
    
    issue_tracker:
      type: "jira"
      url: "${JIRA_URL}"
      project: "SEC"
      token: "${JIRA_TOKEN}"
    
    datastore:
      type: "postgresql"
      connection_string: "${DATABASE_URL}"
  
  # Security controls
  sandbox:
    runtime: "docker"
    network_isolation: true
    timeout_seconds: 300
    resource_limits:
      cpu: "1"
      memory: "2Gi"
```

### Detection Rules Configuration

```yaml
# config/detection.yaml
detection:
  # CodeGuard rules corpus
  rules_corpus: "/etc/foundry/rules/codeguard"
  
  # Rule categories to enable
  enabled_categories:
    - injection
    - authentication
    - authorization
    - cryptography
    - data-exposure
    - configuration
  
  # Severity mapping
  severity_mapping:
    critical: ["CWE-89", "CWE-78", "CWE-79"]  # SQLi, Command Injection, XSS
    high: ["CWE-306", "CWE-862"]               # Missing Auth, Authorization
    medium: ["CWE-327", "CWE-338"]             # Weak Crypto, Weak PRNG
    low: ["CWE-209", "CWE-532"]                # Info Leak, Log Injection
  
  # Rule gap tracking
  rule_gaps:
    enabled: true
    auto_draft_rules: true
    review_queue: "rule-improvements"
```

## Running an Evaluation

```python
# run_evaluation.py
import asyncio
from orchestrator import Orchestrator
from config import load_config

async def main():
    # Load configuration
    config = load_config("config/evaluation.yaml")
    
    # Initialize orchestrator
    orchestrator = Orchestrator(
        llm_client=create_llm_client(config.integrations.llm),
        finding_store=FindingStore(config.integrations.datastore),
        claim_store=ClaimStore(config.integrations.datastore),
        budget_manager=BudgetManager(config.budget)
    )
    
    # Run evaluation
    result = await orchestrator.evaluate(
        target_repo="https://gitlab.internal/acme/webapp"
    )
    
    print(f"Evaluation {result['eval_id']} complete")
    print(f"Findings: {result['findings']}")
    print(f"Coverage: {result['coverage']}%")

if __name__ == "__main__":
    asyncio.run(main())
```

## Common Patterns

### Atomic Claim Processing

```python
# Every agent processes claims atomically
async def process_claim(self, claim: Claim):
    # Claim the work atomically
    if not await self.claims.try_claim(claim.id, self.agent_id):
        return  # Another agent got it
    
    try:
        # Send heartbeat while working
        heartbeat_task = asyncio.create_task(
            self.send_heartbeats(claim.id)
        )
        
        # Do the work
        result = await self.do_work(claim)
        
        # Mark complete
        await self.claims.complete(claim.id, result)
        
    except Exception as e:
        # Fail claim, don't retry (constitution principle)
        await self.claims.fail(claim.id, str(e))
    finally:
        heartbeat_task.cancel()
```

### Evidence-Gated Finding Creation

```python
# Never create findings without evidence
def create_finding(self, claim: Claim, issue: Dict) -> Optional[Finding]:
    # Check evidence requirements
    if not issue.get("location"):
        logger.warning(f"No location for issue in {claim.id}, skipping")
        return None
    
    if not issue.get("reproduction"):
        logger.warning(f"No reproduction for issue in {claim.id}, skipping")
        return None
    
    # Evidence is sufficient
    return Finding(
        claim_id=claim.id,
        location=issue["location"],
        evidence={
            "reproduction": issue["reproduction"],
            "impact": issue["impact"],
            "code_snippet": issue["code"]
        },
        verdict="needs-validation"
    )
```

### Budget Enforcement

```python
class BudgetManager:
    async def check_budget(self, eval_id: str, tokens_requested: int) -> bool:
        """Check if budget allows operation."""
        used = await self.get_tokens_used(eval_id)
        limit = self.config.max_tokens
        
        if used + tokens_requested > limit:
            await self.notify_budget_exhausted(eval_id)
            return False
        
        return True
    
    async def record_usage(self, eval_id: str, tokens: int):
        """Record token usage."""
        await self.db.execute(
            "INSERT INTO token_usage (eval_id, tokens, timestamp) VALUES ($1, $2, NOW())",
            eval_id, tokens
        )
```

## Troubleshooting

### Agents Not Finding Issues

**Check rule corpus:**
```bash
# Verify rules loaded
foundry-ctl list-rules --corpus /etc/foundry/rules/codeguard

# Test rule against sample code
foundry-ctl test-rule CWE-89 --file sample.py
```

**Check explorer creativity:**
```python
# Increase temperature for hypothesis generation
hypotheses = await self.llm.complete(
    prompt,
    temperature=0.8  # Higher = more creative, less reliable
)
```

### Claims Stalling

**Check heartbeat configuration:**
```python
# Ensure heartbeats are sent frequently enough
HEARTBEAT_INTERVAL = 60  # seconds
STALL_THRESHOLD = 300     # 5 minutes

# Heartbeats must be faster than threshold
assert HEARTBEAT_INTERVAL < STALL_THRESHOLD / 2
```

**Check for deadlocks:**
```sql
-- Find stalled claims
SELECT claim_id, agent_id, last_heartbeat, status
FROM claims
WHERE status = 'in_progress'
  AND last_heartbeat < NOW() - INTERVAL '5 minutes';
```

### Findings Not Publishing

**Check verdict state:**
```python
# Only confirmed findings publish
if finding.verdict != "confirmed":
    logger.error(f"Cannot publish {finding.id}, verdict={finding.verdict}")
    # Finding needs validation first
```

**Check deduplication:**
```python
# Verify fingerprints are stable
f1 = generate_fingerprint(finding)
f2 = generate_fingerprint(finding)
assert f1 == f2, "Fingerprints must be deterministic"
```

### Low Coverage

**Check scope configuration:**
```yaml
# Ensure scope includes all target code
coverage:
  scope:
    - src/**/*.py      # Include all source
    - lib/**/*.{js,ts} # Multiple extensions
  exclude:
    - tests/**         # Don't count tests
    - vendor/**        # Don't count dependencies
```

**Check claim distribution:**
```python
# Verify planner creates sufficient claims
plan = await planner.create_plan(target)
print(f"Claims created: {len(plan.claims)}")
print(f"Surface area: {plan.surface_area}")
# Claims should cover all in-scope files
```

## Integration with CodeGuard

```python
# Load CodeGuard rules as Detector corpus
from codeguard import RuleEngine

class Detector:
    def __init__(self, rules_path: str):
        # Load portable CodeGuard rules
        self.rules = RuleEngine.load(rules_path)
        
    async def scan(self, code: str, language: str):
        # Rules execute deterministically
        return await self.rules.evaluate(code, language)

# Export rule gaps back to CodeGuard corpus
async def export_rule_gap(gap: RuleGap):
    """Convert discovered gap into CodeGuard rule."""
    rule = {
        "id": f"CWE-{gap.weakness_id}-{gap.pattern_hash}",
        "name": gap.suggested_name,
        "description": gap.description,
        "pattern": gap.pattern,
        "severity": gap.severity,
        "languages": gap.applicable_languages
    }
    
    # Write to CodeGuard format
    await write_codeguard_rule(rule, "rules/corpus/custom/")
```

## Best Practices

1. **Start with 8 core roles only** — Get foundational pipeline working before adding extensions
2. **Constitution is non-negotiable** — Each principle prevents a real production failure
3. **Evidence gates everything** — No evidence = no finding, regardless of confidence
4. **Fingerprints must be stable** — Same issue in same place = same fingerprint always
5. **Budgets prevent runaway** — Set token limits, enforce them, auto-stop when exhausted
6. **Coverage before completion** — Don't mark evaluation complete until coverage gate passes
7. **Rule gaps feed corpus** — When explorer finds something detector missed, create a rule
8. **Sandbox everything** — Never execute in evaluation environment, always isolate

## References

- **Specification**: `spec.md` — 130 functional requirements with rationale
- **Constitution**: `constitution.md` — 11 inviolable principles
- **Glossary**: `GLOSSARY.md` — Foundry terminology
- **CodeGuard**: https://project-codeguard.org — Portable rule format
- **spec-kit**: https://github.com/github/spec-kit — Spec-driven development workflow
