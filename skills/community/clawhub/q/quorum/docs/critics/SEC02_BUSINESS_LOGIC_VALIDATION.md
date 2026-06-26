# SEC-02: Business Logic Validation Workflow

**Status:** 🔜 Documented workflow — runtime integration planned  
**Date:** March 2026  
**Framework Basis:** OWASP ASVS 5.0.0 V2 (Validation and Business Logic), CWE-20, CWE-606

---

## The Problem

SEC-02 (Input Validation & Sanitization) covers two distinct concerns:

1. **Technical validation** — type checking, format enforcement, bounds checking. SAST and regex patterns handle this reasonably well.
2. **Business logic validation** — does the code enforce domain-specific rules? Can a user order -1 items? Set a future birth date? Access another user's data through a valid but unauthorized input?

SAST tools are blind to business logic. They can't know that a negative quantity is invalid unless someone encodes that rule. This is the Security Critic's highest-value contribution in SEC-02 — and the area where it needs the most guidance to be useful.

---

## Requirements → Critic Path

The workflow for business logic validation follows a three-stage pipeline:

### Stage 1: Requirements Capture (User-Provided)

Business rules must come from somewhere. Quorum does not invent them — they are declared by the user through one of three mechanisms:

**Option A: Rubric Criteria (Recommended)**

Encode business rules directly as rubric criteria:

```json
{
  "id": "BL-001",
  "criterion": "Order quantities must be positive integers between 1 and 9999",
  "severity": "HIGH",
  "evidence_type": "tool",
  "evidence_instruction": "Search for order quantity handling. Verify bounds checking exists before the value reaches business logic or database.",
  "framework_refs": ["CWE-20", "ASVS V2.2.*"]
}
```

This is the most explicit path. Each business rule becomes a testable criterion with clear evidence requirements.

**Option B: Relationship Manifest — Threat Context**

Use the `threat_context` relationship type to declare sensitive operations and roles:

```yaml
- type: threat_context
  target: app/orders/views.py
  context:
    sensitive_operations:
      - "Order creation (quantity must be positive, price must match catalog)"
      - "Discount application (percentage must be 0-100, requires manager role)"
      - "Refund processing (amount cannot exceed original order total)"
```

The Security Critic receives this context and evaluates whether the code enforces these constraints. Less precise than rubric criteria, but lower friction for initial assessment.

**Option C: Inline Documentation**

If the codebase uses docstrings, comments, or type annotations to express business rules, the Security Critic can extract and verify them:

```python
def process_order(quantity: int, price: Decimal) -> Order:
    """Create a new order.
    
    Business rules:
    - quantity must be 1-9999
    - price must match catalog price (no client-side price override)
    - total must not exceed account credit limit
    """
```

This is the weakest path — it depends on documentation accuracy and completeness. But it's better than nothing when rubrics and manifests aren't available.

**When Option C works well:** Docstrings follow a consistent pattern (e.g., `Business rules:` header), rules are co-located with the code they govern, and the codebase has reasonable documentation coverage.

**When Option C produces junk findings:** Business rules are scattered across comments, commit messages, Slack threads, or tribal knowledge. The critic finds docstrings but they describe *what* the function does, not *what constraints it must enforce*. If your inline docs don't express rules, use Option A or B instead.

### Composing Relationship Types — Full Manifest Example

A single `quorum-relationships.yaml` can combine `implements`, `threat_context`, and other relationship types to give critics a complete picture:

```yaml
# quorum-relationships.yaml — e-commerce order service
relationships:
  # Code implements the order specification
  - type: implements
    source: docs/order-spec.md
    target: app/orders/views.py

  # Threat model context for authorization + business logic
  - type: threat_context
    target: app/orders/views.py
    context:
      sensitive_operations:
        - "Order creation (quantity 1-9999, price from catalog only)"
        - "Discount application (0-100%, manager role required)"
        - "Refund processing (cannot exceed original total)"
      roles: ["customer", "manager", "admin"]
      trust_boundary: "All inputs cross trust boundary from public API"

  # Schema contract between API and database
  - type: schema_contract
    source: app/orders/serializers.py
    target: app/orders/models.py

  # Documents relationship for cross-artifact consistency
  - type: documents
    source: docs/order-spec.md
    target: app/orders/models.py
```

This manifest feeds the Security Critic (SEC-02 business logic + SEC-04 authorization), the Correctness Critic (implements relationship), and the Cross-Artifact Consistency check (all relationships). One file, multiple critics, composable.

### Stage 2: Critic Evaluation

The Security Critic evaluates business logic validation using this checklist:

| Check | What the Critic Looks For | Evidence Required |
|-------|--------------------------|-------------------|
| **Boundary enforcement** | Are numeric inputs bounds-checked before use? | Code showing validation + the boundary values |
| **State transition validity** | Can entities move to invalid states? (e.g., cancelled order → shipped) | State machine or status field handling code |
| **Cross-field consistency** | Are related fields validated together? (e.g., start_date < end_date) | Validation logic that checks field relationships |
| **Negative/zero handling** | Do quantities, amounts, and counts reject non-positive values? | Input validation before business logic |
| **Privilege-gated operations** | Are sensitive operations (refund, delete, admin actions) role-checked? | Authorization check before the operation |
| **Idempotency** | Can the same request be safely repeated? Double-submit protection? | Idempotency keys or duplicate detection |
| **Rate limiting on business operations** | Can a user trigger expensive operations without throttling? | Rate limit or queue mechanism |

### Severity Calibration

Not all business logic gaps carry equal weight. Use these defaults unless domain context overrides:

| Check | Typical Severity | Rationale |
|-------|-----------------|-----------|
| **Boundary enforcement** | **HIGH** | Direct data corruption, financial impact (negative quantities, overflow) |
| **State transition validity** | **HIGH** | Invalid state transitions can be irreversible and break downstream workflows |
| **Cross-field consistency** | **MEDIUM** | Usually caught by downstream validation or database constraints; becomes HIGH if financial |
| **Negative/zero handling** | **HIGH** when financial, **MEDIUM** otherwise | A negative dollar amount is worse than a negative page count |
| **Privilege-gated operations** | **CRITICAL** if admin/financial, **HIGH** otherwise | Missing authorization on sensitive ops is always severe |
| **Idempotency** | **MEDIUM** | Duplicated operations are usually recoverable; becomes **HIGH** if financial (double-charge) |
| **Rate limiting** | **MEDIUM** | Abuse potential varies; becomes **HIGH** if expensive operations (bulk email, payment processing) |

The critic uses these defaults when no explicit severity is declared in rubric criteria. Override by setting `"severity"` in your rubric criterion definition.

### Stage 3: Finding Generation

Business logic findings use the standard finding format with SEC-02 category:

```json
{
  "issue_id": "SEC-02-BL-001",
  "critic": "security",
  "severity": "HIGH",
  "category": "SEC-02",
  "description": "Order quantity accepts negative values — no bounds check before database write",
  "evidence": {
    "type": "grep",
    "output": "def create_order(qty): Order.objects.create(quantity=qty)  # line 47",
    "tool_command": "grep -n 'create_order\\|quantity' app/orders/views.py"
  },
  "framework_refs": ["CWE-20", "ASVS V2.2.*", "CWE-606"],
  "remediation": "Add validation: if qty < 1 or qty > 9999: raise ValidationError"
}
```

---

## What the Critic Cannot Do (Honest Limitations)

1. **Invent business rules.** Without requirements (rubric, manifest, or docs), the critic can only flag obvious anti-patterns (negative quantities, missing null checks). It cannot determine that "maximum order value is $50,000" unless told.

2. **Validate complex state machines.** Multi-step workflows with branching transitions require more context than a single code review provides. The critic can spot missing guards but cannot verify the full state graph.

3. **Assess domain correctness.** The critic doesn't know if a 15% discount is reasonable or a data entry error. Domain-specific reasonableness checks require human judgment or domain-specific rubrics.

4. **Replace integration testing.** Business logic validation in code review catches structural gaps. It does not replace testing that exercises the actual execution paths.

---

## Integration with Other Categories

Business logic validation intersects with:

| Category | Intersection |
|----------|-------------|
| **SEC-04 (Authorization)** | Privilege-gated operations are both authorization and business logic. The `threat_context` manifest serves both. |
| **SEC-01 (Injection)** | Input that passes business validation but contains injection payloads. Business validation runs first; sanitization must also run. |
| **SEC-08 (Path Traversal)** | File paths that are valid business inputs but traverse outside allowed directories. |
| **SEC-14 (DoS)** | Business operations that are individually valid but can be abused at volume (e.g., bulk order creation without rate limiting). |

---

## Depth Levels and SEC-02

Business logic checks are available at **standard** and **thorough** depth:

| Depth | SEC-02 Coverage | Notes |
|-------|----------------|-------|
| **quick** | ❌ Not run | Quick runs only pre-screen + Correctness + Completeness. Security critic is not dispatched. |
| **standard** | ✅ Full SEC-02 | Security critic runs with all business logic checks. Rubric criteria and threat_context are evaluated. No fix loops. |
| **thorough** | ✅ Full SEC-02 + fix loop | Same coverage as standard, plus the Fixer proposes remediations for CRITICAL/HIGH findings and re-validates. |

If you need business logic validation, use `--depth standard` at minimum. The `quick` depth is designed for fast feedback on obvious issues, not comprehensive security review.

---

## Recommended Approach for Assessments

1. **Start with rubric criteria** — if you know the business rules, encode them. This gives the best results.
2. **Add threat context** — declare sensitive operations in the relationship manifest. This gives the critic enough to evaluate authorization and basic validation.
3. **Review findings critically** — business logic findings from LLM analysis are inherently more speculative than SAST findings. Cross-reference with domain experts.
4. **Iterate** — the first assessment reveals gaps in your requirements capture. Each subsequent run gets tighter.

---

> ⚖️ **LICENSE** — This file is part of [Quorum](https://github.com/SharedIntellect/quorum).  
> Copyright 2026 SharedIntellect. MIT License.  
> See [LICENSE](https://github.com/SharedIntellect/quorum/blob/main/LICENSE) for full terms.
