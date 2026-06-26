---
name: secrets
description: Deep workflow for secrets lifecycle—classification, storage (Vault/KMS/cloud), rotation, least privilege, developer ergonomics, audit, and incident response. Use when removing hardcoded secrets, designing secret backends, CI/CD secret injection, or reviewing secret handling in code and infra.
---

# Secrets Management (Deep Workflow)

Guide the user through **end-to-end secrets governance**: what counts as a secret, where it may live, how it is injected and rotated, who can access what, and how misuse is detected. Act as a structured reviewer and architect, not a checklist robot.

## When to Offer This Workflow

**Trigger conditions:**

- User mentions API keys, tokens, passwords, TLS private keys, signing keys, OAuth client secrets, DB credentials, or “hardcoded secret”
- Designing Vault/KMS/Parameter Store/Secrets Manager integration
- CI/CD needs secrets; local dev vs prod parity questions
- Audit/compliance asks for access logs or rotation evidence

**Initial offer:**

Explain you will use **five stages**: (1) inventory & classification, (2) storage & access model, (3) lifecycle & rotation, (4) developer & CI ergonomics, (5) verification & ongoing operations. Ask if they want this full pass or a narrower slice (e.g., “rotate one class of keys”).

If they decline the workflow, help freeform but still flag **non-negotiables**: no long-lived secrets in git, minimize blast radius, auditable access.

---

## Stage 1: Inventory & Classification

**Goal:** Know **what exists**, **where it is**, **who needs it**, and **blast radius if leaked**.

### Questions to Ask

1. What environments exist (local, staging, prod, partner)? Are boundaries strict?
2. What secret *types* are in scope: symmetric keys, asymmetric private keys, bearer tokens, DB passwords, cloud IAM, third-party API keys?
3. Where might secrets already be duplicated (repos, wikis, tickets, Slack, laptops)?
4. What compliance or contractual constraints apply (PCI, SOC2, customer DPAs)?

### Actions

- Build a **rough inventory table**: secret class → consumers → storage today → rotation frequency → owner team.
- Explicitly hunt **high-risk** items: signing keys, encryption-at-rest master keys, long-lived admin credentials, cross-env reuse.
- Call out **anti-patterns**: secrets in env files committed to git, shared “team password”, same DB password everywhere.

### Exit Condition

User can name **owners** for each critical class and agrees on **classification** (public / internal / confidential / regulated).

**Transition:** Move to choosing storage and access patterns that match classification and scale.

---

## Stage 2: Storage & Access Model

**Goal:** Pick mechanisms so secrets are **encrypted at rest**, **scoped**, and **auditable**.

### Design Points

- **Central secret store** vs **cloud-native** (e.g., Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) vs **KMS-only** patterns.
- **Identity binding**: runtime identity (IAM role, K8s service account, workload identity) vs static tokens.
- **Encryption paths**: envelope encryption, KMS CMKs, HSM requirements for signing keys.
- **Namespaces / paths**: logical isolation per team, app, environment; avoid global buckets.

### Trade-offs to Surface

- **Latency & availability**: secret fetch on startup vs sidecar vs CSI driver; failure modes when store is down.
- **Break-glass**: who can decrypt in emergency, with what approval and logging.
- **Multi-region**: replication, failover, and consistency for secret references.

### Exit Condition

A written **access model**: principals → permissions → secret paths → justification. No “everyone read/write production.”

**Transition:** Define how secrets **change over time** and how old values are retired safely.

---

## Stage 3: Lifecycle & Rotation

**Goal:** Secrets **expire**, **rotate**, and **revoke** without surprise outages.

### Workflow

1. **Rotation policy** per class: automatic vs manual, max age, overlap window.
2. **Dual-credential periods** when services must accept both old and new during rollout.
3. **Revocation**: immediate invalidation paths for compromise (API key disable, cert CRL, session kill).
4. **Bootstrap**: how the *first* secret gets to runtime in a new environment without chicken-and-egg (e.g., cloud IAM → fetch others).

### Pitfalls to Call Out

- Rotating DB password without connection pool drain → thundering reconnect failures.
- Clients caching JWT signing keys without key ID rotation support.
- Secrets embedded in **container images** or **build artifacts**.

### Exit Condition

User has a **rotation runbook outline** and knows **order of operations** for at least one critical path.

**Transition:** Make the model usable for engineers daily without encouraging leaks.

---

## Stage 4: Developer & CI Ergonomics

**Goal:** Correct behavior is the **default**; wrong behavior is hard or blocked.

### Practices

- **Local dev**: short-lived dev credentials, personal sandboxes, `.env.example` without values, secret scanners in pre-commit/CI.
- **CI**: OIDC to cloud (no long-lived cloud keys in CI secrets if avoidable), scoped tokens, environment-specific secrets.
- **Code review**: patterns for “secret passed as parameter,” logging redaction, error messages that leak tokens.

### Tooling Mentions (when relevant)

- Git secret scanning (e.g., gitleaks, trufflehog), dependency on org policy.
- Dynamic secrets / database roles if using Vault-style patterns.

### Exit Condition

Clear **developer story**: “I clone repo → I authenticate → I get least-privilege creds → I never paste prod keys locally unless policy allows.”

**Transition:** Prove the design works and stays healthy over time.

---

## Stage 5: Verification & Operations

**Goal:** Evidence that controls work; readiness when things go wrong.

### Verification

- **Drills**: restore from backup of secret metadata (if applicable), rotate in staging with full integration tests.
- **Audit review**: sample access logs; alert on anomalous read patterns.
- **Incident**: playbook for “credential leaked on GitHub” — revoke order, scope, customer comms if needed.

### Metrics / Signals (examples)

- Failed authentication spikes after rotation
- Secret fetch error rates from apps
- Time-to-revoke for a simulated leak

### Exit Condition

User can answer: “If this key leaks at 3am, what is step 1–5 and who is paged?”

---

## Final Review Checklist

- [ ] No production secrets in source control or public artifacts
- [ ] Least privilege enforced at identity + path + operation level
- [ ] Rotation and revocation paths documented with owners
- [ ] CI and local dev paths do not encourage static prod credentials
- [ ] Audit/logging aligned with organizational requirements

## Tips for Effective Guidance

- Prefer **concrete sequences** (bootstrap → fetch → use → rotate) over abstract “use a vault.”
- Always ask **blast radius** and **who can decrypt**.
- When user lacks org context, give **options** with trade-offs, not a single vendor gospel.

## Handling Deviations

- **“We only need one API key”**: still classify, store centrally, and set expiry where possible.
- **“Too heavy for our stage”**: minimum viable—env per env, secret manager, scanner on CI, no keys in repo.
