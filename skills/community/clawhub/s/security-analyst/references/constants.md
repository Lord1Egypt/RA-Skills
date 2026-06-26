# Security Analyst — Constants

Single source of truth. Update here, not in individual files.

## Paths

```
PROJECT_ROOT  = (cwd)
SKILL_ROOT    = directory containing SKILL.md (.claude/skills/security-analyst or .cursor/skills/security-analyst)
PROMPTS_DIR   = {SKILL_ROOT}/references/prompts
TEMPLATES_DIR = {SKILL_ROOT}/assets/templates
PLUGINS_DIR   = {SKILL_ROOT}/references/plugins
RUN_DIR       = docs/security/runs/{YYYY-MM-DD-HHMMSS}
FINDINGS_DIR  = {RUN_DIR}/findings
RECON_DIR     = {RUN_DIR}/recon
REPORTS_DIR   = {RUN_DIR}/reports
```

Timestamp `YYYY-MM-DD-HHMMSS` is set once at run start.

## Reports

All reports write to `{REPORTS_DIR}/`:

| File | Producer |
|------|----------|
| `surface.md` | Orchestrator — attack surface, git history, deps, config |
| `logic.md` | Orchestrator — business logic exploitation |
| `tracing.md` | Orchestrator — data flow tracing |
| `exploits.md` | Orchestrator — exploit catalog with PoCs |
| `validation.md` | Orchestrator — critic-reviewed findings |
| `sbom.md` | Orchestrator — software bill of materials |
| `final.md` | Report writer agent |
| `fix-plan.md` | Fix planner agent |
| `compliance.md` | Orchestrator (when requested) |
| `delta.md` | Orchestrator (when requested) |
| `privacy.md` | Privacy agent (when requested) |
| `threat-model.md` | Threat model agent (when requested) |

Other output directories: `recon/` (index.md + 14 step files), `findings/` (atomic finding files + index.md).

## Templates

In `{TEMPLATES_DIR}/`:

| File | Used By |
|------|---------|
| `finding.md` | All analysis agents |
| `agent-common.md` | Appended to all agent prompts |
| `group-report.md` | Orchestrator (per-stage reports) |
| `recon-report.md` | Recon agents |
| `final-report.md` | Report writer agent |
| `fix-plan.md` | Fix planner agent |
| `sbom-report.md` | Orchestrator |
| `compliance-report.md` | Orchestrator |
| `delta-report.md` | Orchestrator |
| `privacy-report.md` | Privacy agent |

## Agent Registry

### Recon Stage

14 recon agents (`recon-agent.md`), one per step. Wave A: 12 parallel. Wave B: 2 (depend on A).

### Surface Stage

| Agent | Prompt | Prefix | Condition |
|-------|--------|--------|-----------|
| `surface-http` | `attack-surface-http.md` | `HTTP` | Always |
| `surface-authz` | `attack-surface-authz.md` | `AUTHZ` | Always |
| `surface-integrations` | `attack-surface-integrations.md` | `INT` | Has integrations |
| `surface-frontend` | `attack-surface-frontend.md` | `FE` | Has frontend |
| `surface-llm` | `attack-surface-llm.md` | `LLM` | Has AI/LLM |
| `api-schema` | `api-schema.md` | `API` | Has API schemas |
| `websocket-security` | `websocket-security.md` | `WS` | Has WebSocket/SSE |
| `file-upload-security` | `file-upload-security.md` | `UPLOAD` | Has file uploads |
| `history-injections` | `git-history-injections.md` | `INJ` | Always |
| `history-auth-bypass` | `git-history-auth-bypass.md` | `AUTH` | Always |
| `history-ssrf` | `git-history-ssrf.md` | `SSRF` | Always |
| `history-data-exposure` | `git-history-data-exposure.md` | `DATA` | Always |
| `deps-audit` | `dependency-audit.md` | `DEP` | Always |
| `config-infra` | `config-infrastructure.md` | `CFG` | Always |
| `cicd-pipeline` | `cicd-pipeline.md` | `CICD` | Has CI/CD |
| `container-security` | `container-security.md` | `CTR` | Has containers |

### Logic Stage

| Agent | Prompt | Prefix |
|-------|--------|--------|
| `logic-races` | `logic-race-conditions.md` | `RACE` |
| `logic-authz` | `logic-authz-escalation.md` | `PRIV` |
| `logic-pipeline` | `logic-pipeline-exploit.md` | `PIPE` |
| `logic-dos` | `logic-dos.md` | `DOS` |

### Tracing Stage

`flow-tracer-N` — `data-flow-tracer.md` — prefix `FLOW` — up to 4, one per critical data flow.

### Exploits → Validation → Reporting → Remediation

| Agent | Prompt | Prefix |
|-------|--------|--------|
| `exploit-dev` | `exploit-developer.md` | — |
| `finding-critic` | `finding-critic.md` | `CRIT` |
| `report-writer` | `report-writer.md` | — |
| `fix-planner` | `fix-planner.md` | — |
| `threat-model` | `threat-model-agent.md` | `TM` |

Incidental findings use `IX-{AGENT_PREFIX}` prefix.

## Stages

```
recon → surface → logic → tracing → exploits → validation → reporting → remediation
                ↘ sbom (parallel with logic)
```

| Stage | Depends On | Agents | Report |
|-------|------------|--------|--------|
| recon | — | 14 | `recon/index.md` |
| surface | recon | ≤16 | `reports/surface.md` |
| sbom | surface | 0 | `reports/sbom.md` |
| logic | surface | 4 | `reports/logic.md` |
| tracing | surface+logic | ≤4 | `reports/tracing.md` |
| exploits | all prior | 1 | `reports/exploits.md` |
| validation | exploits | 1 | `reports/validation.md` |
| reporting | all prior | 1 | `reports/final.md` |
| remediation | reporting | 1 | `reports/fix-plan.md` |

Team name: `security-analysis`
