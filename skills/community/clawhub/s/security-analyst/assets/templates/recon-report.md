# Recon Report — LOD Architecture

The recon report uses the same Level of Detail architecture as findings. Instead of a single monolithic file, recon data is written as atomic section files consumed selectively by downstream agents.

## File Structure

```
{RUN_DIR}/recon/
├── index.md                    # LOD-0 table + LOD-1 briefs (assembled by orchestrator)
├── step-01-metadata.md
├── step-02-docs.md
├── step-03-http.md
├── step-04-boundaries.md
├── step-05-crown-jewels.md
├── step-06-auth.md
├── step-07-integrations.md
├── step-08-secrets.md
├── step-09-data-flows.md
├── step-10-security-work.md
├── step-11-config.md
├── step-12-frontend.md
├── step-13-dependencies.md
└── step-14-scope.md
```

---

## LOD-0: Summary Table (in index.md)

Each recon agent returns one LOD-0 row. The orchestrator assembles these into the index.

Format: `| [Step #] | [Section Name] | [Key facts — one line] |`

Example:
```
| # | Section | Key Facts |
|---|---------|-----------|
| 1 | Project Metadata | TypeScript, Firebase Cloud Functions, Node 22, Jest |
| 3 | HTTP Entry Points | 12 endpoints: 4 unauth, 8 auth, 5 background |
| 5 | Crown Jewels | OAuth tokens (KMS encrypted), PII (email/name), automated email sending |
| 6 | Auth & AuthZ | Firebase Auth, Firestore rules, Cloud KMS token encryption |
```

---

## LOD-1: Section Brief (in index.md)

Each recon agent returns one LOD-1 paragraph. The orchestrator assembles these below the LOD-0 table.

Format:
```
### Step N: [Section Name]
**[Key metric]:** [value]
**Key files:** [2-4 most important file paths with line numbers]
**Notable:** [1-2 sentences on security-relevant observations — facts only, not analysis]
**Details:** recon/step-{NN}-{name}.md
```

Example:
```
### Step 3: HTTP Entry Points
**Endpoints:** 12 (4 unauthenticated, 8 authenticated, 5 background/scheduled)
**Key files:** functions/src/index.ts:1-50, functions/src/webhooks.ts:1-30
**Notable:** 2 unauthenticated webhook endpoints accept external input. processUserEmails is a Cloud Task handler.
**Details:** recon/step-03-http.md
```

---

## LOD-2: Atomic Section Files

Each recon agent writes its full section to `{RECON_DIR}/step-{NN}-{name}.md`. These contain the complete tables with every file:line reference. The format for each step follows.

Every table row MUST include **absolute file paths with line numbers** (e.g., `/path/to/file.ts:42`) so downstream agents can `Read` directly.

---

### step-01-metadata.md — Project Metadata

| Field | Value |
|-------|-------|
| Project Name | |
| Primary Language(s) | |
| Framework(s) | |
| Runtime(s) | |
| Infrastructure | |
| Architecture Style | |
| Package Manager(s) | |
| Test Framework(s) | |
| Build System | |
| Monorepo? | Yes/No — list packages if yes |

---

### step-02-docs.md — Documentation Index

| Document | Path | Relevance |
|----------|------|-----------|
| README | | Project overview |
| Specification | | Architecture, data model, API details |
| Contributing guide | | Dev workflow, code style |
| Security docs | | Existing security policies/audits |
| CI/CD config | | Pipeline, deploy targets |
| Project instructions | | CLAUDE.md or similar |
| API documentation | | Endpoint docs |
| Changelog | | Version history, security fixes |

List ALL documentation files found. Mark missing items as "Not found".

---

### step-03-http.md — HTTP Entry Points

#### Unauthenticated Endpoints

| Endpoint | File:Line | Method | Purpose | Auth Required | Input Sources |
|----------|-----------|--------|---------|---------------|---------------|

#### Authenticated Endpoints

| Endpoint | File:Line | Method | Purpose | Auth Mechanism | Input Sources |
|----------|-----------|--------|---------|----------------|---------------|

#### Background/Scheduled Functions

| Function | File:Line | Trigger | Schedule/Event | Auth Mechanism |
|----------|-----------|---------|----------------|----------------|

Include: HTTP handlers, webhooks, API routes, RPC endpoints, scheduled jobs, event-driven functions, message queue consumers.

---

### step-04-boundaries.md — Trust Boundaries

| Boundary | Direction | Source | Destination | Data Exchanged | Protection |
|----------|-----------|--------|-------------|----------------|------------|

Categories to identify:
- **External → System**: Webhooks, callbacks, API endpoints receiving external input
- **User → System**: Authenticated user actions, client-side writes
- **System → External**: Outbound API calls, email sending, third-party integrations
- **Client → Database**: Direct database reads/writes from client code

---

### step-05-crown-jewels.md — Crown Jewels

| Asset | Storage Location | Protection Mechanism | Impact if Compromised |
|-------|-----------------|---------------------|----------------------|

Identify the most valuable data and capabilities: credentials, tokens, PII, financial data, automated actions, encryption keys.

#### Attacker Profiles

| Profile | Access Level | Capabilities | Primary Targets | Entry Points |
|---------|-------------|-------------|-----------------|-------------|
| Unauthenticated External | None | Can reach public endpoints | | |
| Authenticated User | User-level | CRUD own resources, call authenticated APIs | | |
| Malicious Input Source | None | Controls content processed by the system | | |
| Compromised Integration | API-level | Can send forged responses/callbacks | | |
| Insider/Admin | Elevated | Direct infrastructure access | | |

Add project-specific profiles as discovered.

---

### step-06-auth.md — Authentication & Authorization

#### Authentication Mechanisms

| Mechanism | Implementation | File:Line | Protects | Notes |
|-----------|---------------|-----------|----------|-------|

#### Authorization Rules

| Resource | Rule Type | File:Line | Who Can Access | Enforcement Point |
|----------|-----------|-----------|----------------|-------------------|

#### Session/Token Management

| Token Type | Storage | Lifetime | Refresh Mechanism | File:Line |
|------------|---------|----------|-------------------|-----------|

---

### step-07-integrations.md — External Integrations

| Integration | Client File:Line | Auth Method | Data Sent | Data Received | SSRF Risk |
|------------|-----------------|-------------|-----------|---------------|-----------|

For each integration, note:
- Is there a wrapper/client service?
- Are URLs hardcoded or configurable?
- Is response data validated/sanitized?
- Are errors handled without leaking details?

---

### step-08-secrets.md — Encryption & Secrets

#### Secret Storage

| Secret | Storage Method | Access Pattern | File:Line |
|--------|---------------|----------------|-----------|

#### Encryption at Rest

| Data Type | Encryption Method | Key Management | File:Line |
|-----------|------------------|----------------|-----------|

#### Plaintext Secrets Found

| Secret Type | File:Line | Risk Level | Notes |
|------------|-----------|------------|-------|

Search for: hardcoded API keys, tokens, passwords, connection strings in source code, config files, and environment files.

---

### step-09-data-flows.md — Data Flows

Identify the critical data flows through the system. For each, trace the path from source to destination.

#### Flow: [Name]

| Step | File:Line | Input | Transformation | Output | Sanitization |
|------|-----------|-------|----------------|--------|-------------|

Repeat for each critical flow (typically 3-6 flows covering: user input processing, credential lifecycle, external trigger handling, automated actions).

**Note:** This step runs in Wave B — it has access to Wave A LOD-0 summaries for entry points, auth mechanisms, and integrations. Read the relevant step files from `{RECON_DIR}/` for full detail.

---

### step-10-security-work.md — Existing Security Work

#### Security-Related Commits

| Commit | Date | Summary | Files Changed |
|--------|------|---------|---------------|

Use: `git log --all --oneline --grep="security" --grep="fix" --grep="vuln" --grep="inject" --grep="sanitiz" --grep="escap" --grep="auth" --grep="SSRF" --grep="XSS"`

#### Security Utilities

| Utility | File:Line | Purpose | Used By |
|---------|-----------|---------|---------|

#### SAST/Scan Results

| Tool | Results Location | Finding Count | Suppression Count |
|------|-----------------|---------------|-------------------|

#### Security Documentation

| Document | Path | Contents |
|----------|------|----------|

---

### step-11-config.md — Configuration

#### Security Headers

| Header | Value | Source File:Line |
|--------|-------|-----------------|

#### CORS Configuration

| Setting | Value | Source File:Line |
|---------|-------|-----------------|

#### Environment Files

| File | Contains | Git-Ignored? | Template Available? |
|------|----------|-------------|-------------------|

---

### step-12-frontend.md — Frontend

| Aspect | Details | File:Line |
|--------|---------|-----------|
| Framework | | |
| Rendering | SSR/CSR/SSG/Hybrid | |
| Client-Side Storage | localStorage/cookies/IndexedDB | |
| Service Workers | Present? Purpose? | |
| Authentication UI | Login flow, token handling | |
| Content Rendering | Does it render user-controlled HTML? | |

If no frontend exists, write "No frontend detected" and note what was checked.

---

### step-13-dependencies.md — Dependencies

#### Backend Dependencies

| Package | Version | Security Relevance | Last Updated |
|---------|---------|-------------------|-------------|

#### Frontend Dependencies

| Package | Version | Security Relevance | Last Updated |
|---------|---------|-------------------|-------------|

Focus on security-relevant packages: auth libraries, HTTP clients, parsers, crypto, database drivers, template engines.

---

### step-14-scope.md — Scope Notes

| Category | Details |
|----------|---------|
| Directories Analyzed | |
| Directories Skipped | |
| Total Source Files | |
| Languages Detected | |
| Limitations | |

**Note:** This step runs in Wave B — it summarizes what all Wave A agents analyzed.
