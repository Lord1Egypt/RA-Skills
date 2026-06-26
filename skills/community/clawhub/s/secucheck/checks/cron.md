# Cron Job Security Checks

## What to Examine

Use `cron action:"list" includeDisabled:true` to get all cron jobs.

## Check 1: Job Payload Type

**Location**: `job.payload.kind`

| Kind | Risk Level | Notes |
|------|------------|-------|
| `systemEvent` | 🟢 Low | Injects text into session (main only) |
| `agentTurn` | 🟡 Medium | Runs agent with full capabilities |

**agentTurn risks**:
- Runs with the agent's full tool permissions
- If agent has exec/browser: higher risk
- Check what the `message` prompt contains

## Check 2: External Data Dependencies

**Examine `job.payload.message`**:

Look for instructions that:
- Fetch URLs (`web_fetch`, "URL 확인해줘")
- Read external emails
- Process external webhooks
- Scrape websites

**Risk if external data + exec agent**:
- 🔴 Critical - Automated prompt injection vector
- Example: "매일 이 URL 읽고 실행해줘" = perfect attack vector

## Check 3: Frequency and Scope

**Location**: `job.schedule`

| Schedule | Consideration |
|----------|---------------|
| `kind: "at"` | One-shot, lower concern |
| `kind: "every"` with < 1hr | Frequent, higher scrutiny |
| `kind: "cron"` | Check expression complexity |

**High frequency + powerful agent = more attack windows**

## Check 4: Target Agent

**Location**: `job.agentId` or `job.sessionTarget`

Cross-reference with agents.md findings:
- If targeting an agent with exec: check payload carefully
- If targeting main session: less isolated, higher trust required

## Check 5: Delivery Settings

**Location**: `job.delivery`

| Mode | Notes |
|------|-------|
| `none` | Silent execution |
| `announce` | Reports to channel |

**Silent jobs with powerful actions**: 🟡 Medium
- Harder to notice if compromised
- Recommend enabling announce for visibility

## Check 6: Agent Capability Mismatch

**Cross-reference**: `job.agentId` → `agents.list[].tools`

**Check if job payload requests tools the agent doesn't have**:
- Job says "exec로 실행해줘" but agent has `deny: [exec]`
- Job says "브라우저로 확인해줘" but agent lacks browser tool

**Risk**:
- 🟡 Medium - Job won't work as intended (configuration bug)
- May indicate copy-paste error or outdated config
- Recommend: Fix agent permissions or change job payload

## Check 7: Main Session Target

**Location**: `job.sessionTarget`

| Target | Risk |
|--------|------|
| `isolated` | 🟢 Low - Separate session per run |
| `main` | 🟡 Medium - Runs in main context |

**Risks with `main`**:
- Shares context with user's main session
- Can access main session's history/memory
- Errors affect main session state

**Recommendation**: Prefer `isolated` for automated jobs

## Specific Patterns to Flag

### Pattern A: URL Scraper + Exec
```yaml
payload:
  message: "이 URL 내용 분석하고 필요한 조치 취해줘"
  # + agent has exec tool
```
**Risk**: 🔴 Critical - Trivial prompt injection

### Pattern B: Email Processor
```yaml
payload:
  message: "새 이메일 확인하고 처리해줘"
```
**Risk**: 🟠 High - Email-based injection possible

### Pattern C: Monitoring with Actions
```yaml
payload:
  message: "서버 상태 확인하고 문제 있으면 조치해줘"
```
**Risk**: 🟡 Medium - Automated actions need guardrails

## Recommended Mitigations

For risky cron jobs, suggest:

1. **Separate agent**: Create a minimal-tool agent for the cron task
2. **Read-only first**: Fetch and report, don't auto-execute
3. **Allowlist actions**: Specify exactly what actions are permitted
4. **Enable announce**: Make job results visible
