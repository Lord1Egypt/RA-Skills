# Upgrade Audit Report Template

Use this template when presenting upgrade risk analysis to operators. Adapt based on actual findings.

## Report Structure

```markdown
# Upgrade Audit Report: v{FROM} → v{TO}

**Generated**: {TIMESTAMP}
**Analyzed by**: {AGENT_NAME}
**Analysis Scope**: {VERSION_RANGE} (e.g., 2026.3.3 – 2026.3.8)

---

## Executive Summary

I have analyzed the upcoming upgrade from **v{FROM}** to **v{TO}** and identified:

- **{N} configuration-level risks**
  - {N_CRITICAL} critical (P0)
  - {N_HIGH} high (P1)
  - {N_MEDIUM} medium (P2)
- **{N} runtime-level risks**
  - {N_HIGH} high (P1)
  - {N_MEDIUM} medium (P2)
  - {N_LOW} low (P3)

**Overall Recommendation**: [BLOCK UPGRADE / PROCEED WITH CAUTION / PROCEED]

---

## Configuration-Level Risks

### 🔴 Risk #1: {SHORT_NAME} [Priority: P0]

**Evidence**: The changelog states:
> "{QUOTE FROM CHANGELOG}"

**Our Vulnerability**: Our configuration file (`openclaw.json`) at path `{JQ_PATH}` relies on:
- `{CURRENT_BEHAVIOR}`

**Predicted Failure**: `{FAILURE_DESCRIPTION}`

**Recommended Mitigation**:
```json
{
  "{PATH}": "{PROPOSED_VALUE}"
}
```

**Verification Plan**:
- Pre-upgrade: `{VERIFICATION_STEP}`
- Post-upgrade: `{VERIFICATION_STEP}`

---

### 🟡 Risk #2: {SHORT_NAME} [Priority: P1]

[Same structure as above]

---

## Runtime-Level Risks

### 🟠 Risk #3: {SHORT_NAME} [Priority: P1]

**Evidence**: The changelog states:
> "{QUOTE FROM CHANGELOG}"

**Affected Workflows**:
- `{WORKFLOW_1}`: {DESCRIPTION}
- `{WORKFLOW_2}`: {DESCRIPTION}

**Predicted Behavioral Change**: `{BEHAVIOR_CHANGE}`

**Verification Plan**:
1. `{TEST_STEP_1}`
2. `{TEST_STEP_2}`

**Recommended Actions**:
- `{ACTION_1}`
- `{ACTION_2}`

---

### 🔵 Risk #4: {SHORT_NAME} [Priority: P2]

[Same structure as above]

---

## Low-Priority / Informational Changes

These changes are unlikely to cause issues but may affect edge cases or workflows:

- `{CHANGE_1}`: {BRIEF_DESCRIPTION}
- `{CHANGE_2}`: {BRIEF_DESCRIPTION}

---

## Pre-Upgrade Checklist

Complete these steps **before** upgrading:

- [ ] Run `openclaw doctor` and resolve any validation errors
- [ ] Create backup: `openclaw backup create --only-config`
- [ ] For each P0/P1 risk: [ ] Mitigated / [ ] Accepted with rollback plan
- [ ] Document current state (git diff, screenshots, logs)

**Rollback Plan**: If critical failures occur post-upgrade:
1. `{ROLLBACK_STEP_1}`
2. `{ROLLBACK_STEP_2}`

---

## Post-Upgrade Verification

Execute these tests **immediately after** upgrade completes:

### Critical Path Tests (P0/P1)

- [ ] Gateway starts successfully: `openclaw status`
- [ ] No errors in `gateway.err.log` (last 100 lines)
- [ ] Test bot response in group: `{GROUP_NAME}` → send `@{BOT} /status`
- [ ] Test model invocation: `{MODEL_ID}` → send test prompt

### Behavioral Tests (P2)

- [ ] Test `{WORKFLOW_1}`: {TEST_DESCRIPTION}
- [ ] Test `{WORKFLOW_2}`: {TEST_DESCRIPTION}

### Monitoring (P3)

- [ ] Monitor logs for `{PATTERN_TO_WATCH}` over next {TIME_PERIOD}
- [ ] Check session file sizes after compaction: `ls -lh ~/.openclaw/sessions/`

---

## Appendix: Detailed Analysis

### Full Changelog Scan Results

**Total commits analyzed**: {N_COMMITS}
**Breaking changes found**: {N_BREAKING}
**High-risk keywords detected**: {N_KEYWORDS}

**Keyword distribution**:
- `refactor`: {N}
- `unify`: {N}
- `fix`: {N}
- etc.

### Configuration Cross-Reference

**Config sections analyzed**:
- ✅ `gateway.auth`
- ✅ `channels.telegram`
- ✅ `models.providers`
- ✅ `agents.defaults`
- ✅ `bindings`

**Dependencies identified**:
- `{DEPENDENCY_1}`: {DESCRIPTION}
- `{DEPENDENCY_2}`: {DESCRIPTION}

### Workflow Analysis

**Active workflows detected**:
- `{WORKFLOW_1}`: {FREQUENCY} usage
- `{WORKFLOW_2}`: {FREQUENCY} usage

**Workflow-risk mapping**:
- `{WORKFLOW_1}` → affected by {RISK_#}
- `{WORKFLOW_2}` → affected by {RISK_#}

---

**Report End**
```

---

## Template Usage Guidelines

### 1. Prioritize Clarity Over Completeness
- Don't list every single change. Focus on what matters to this deployment.
- Group related changes together.
- Use clear, non-technical language when possible.

### 2. Be Specific About Vulnerabilities
- Don't say "config may break"
- Say: "Our config at `channels.telegram.accounts.claw_3po.groups['-1003593489589']` has `allowFrom: ['8245211057']` which may be affected by..."

### 3. Make Verification Steps Concrete
- Don't say "test the bot"
- Say: "Send message `@claw_config_bot /status` in 入管课 group and verify response"

### 4. Prioritize Risks
- P0 risks go at the top, even if there are only 1-2
- Group P1 together, then P2
- Put P3/P4 in appendix or "Informational" section

### 5. Provide Actionable Mitigations
- Every P0/P1 risk must have a clear mitigation or rollback plan
- Don't just identify problems; propose solutions

### 6. Adapt Based on Severity
- For minor upgrades (e.g., 2026.3.7 → 2026.3.8), you can use a shorter template
- For major version jumps, use the full template
- Always include at least: Executive Summary, Critical Risks, Post-Upgrade Verification

---

## Example: Short-Form Report

Use this for low-risk upgrades:

```markdown
# Upgrade Audit Report: v2026.3.7 → v2026.3.8

**Summary**: Analyzed {N_COMMITS} commits. No breaking changes. 2 low-risk behavioral changes.

**Recommendation**: ✅ PROCEED

### Low-Risk Changes

1. **TUI `/new` behavior** [P2]: Now creates independent sessions instead of resetting.
   - **Impact**: If you use `/new` to clear conversations, switch to `/reset`
   - **Verification**: Test `/new` in TUI post-upgrade

2. **Telegram DM draft streaming** [P3]: Fixes "flash duplicate" bug.
   - **Impact**: None (improvement)

### Pre-Upgrade
- [ ] Run `openclaw doctor`

### Post-Upgrade
- [ ] Test TUI `/new` creates independent session
- [ ] Verify bot responds in groups

**Rollback**: Not needed, but backup available if issues arise.
```
