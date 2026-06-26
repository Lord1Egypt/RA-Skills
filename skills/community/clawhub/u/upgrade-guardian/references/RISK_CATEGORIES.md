# Risk Categories for Upgrade Analysis

This document defines the taxonomy of risks that Upgrade Guardian analyzes during OpenClaw upgrades. Understanding these categories helps agents structure their analysis and communicate findings effectively.

## Category 1: Configuration-Level Risks

Risks that affect static configuration files (`openclaw.json`, environment variables, etc.).

### 1.1 Schema Breaking Changes
- **Definition**: Changes to config schema that render existing configs invalid or cause validation failures.
- **Examples**:
  - Required fields added
  - Field types changed (string → number)
  - Enum values restricted
- **Impact**: Gateway/agent fails to start, config rejected
- **Detection**: `openclaw doctor` validation, config load errors
- **Mitigation**: Update config to match new schema before upgrade

### 1.2 Default Value Changes
- **Definition**: Changes to default behavior for unspecified config options.
- **Examples**:
  - `gateway.auth.mode` now required when both token and password present
  - Timeout defaults changed
- **Impact**: Unexpected behavior, possible service disruption
- **Detection**: Compare current config defaults against new defaults
- **Mitigation**: Explicitly set desired values in config

### 1.3 Deprecated Fields
- **Definition**: Config fields marked for removal or already non-functional.
- **Examples**:
  - Legacy top-level `heartbeat` key (moved to `agents.defaults.heartbeat`)
  - Removed provider options
- **Impact**: Config ignored or causes warnings
- **Detection**: Deprecation warnings in logs, documentation review
- **Mitigation**: Migrate to new config structure

### 1.4 Validation Tightening
- **Definition**: Stricter validation for existing config values.
- **Examples**:
  - Telegram `groupAllowFrom` now validates sender ID format
  - Security rules now enforce strict types
- **Impact**: Previously accepted config now rejected
- **Detection**: Validation errors, doctor warnings
- **Mitigation**: Fix invalid values before upgrade

---

## Category 2: Runtime-Level Risks

Risks that affect system behavior without requiring config changes.

### 2.1 Behavioral Logic Changes
- **Definition**: Changes to core application logic that alter observable behavior.
- **Examples**:
  - Session routing logic changed (duplicate suppression, legacy route inheritance)
  - Compaction triggers or preservation rules changed
  - Cron execution mode changed (sync → async)
- **Impact**:
  - Bot stops responding in some contexts
  - Session data lost or truncated unexpectedly
  - Cron jobs behave differently
- **Detection**: User reports, behavioral testing
- **Mitigation**: Document expected changes, adjust workflows, test critical paths

### 2.2 Protocol/API Compatibility
- **Definition**: Changes to how OpenClaw interacts with external services or APIs.
- **Examples**:
  - Streaming response format changes (OpenAI-compatible providers)
  - WebSocket CDP URL handling
  - HTTP header requirements
- **Impact**:
  - Streaming responses fail mid-stream
  - Browser automation breaks
  - External API calls rejected
- **Detection**: Test with actual external services
- **Mitigation**: Update provider configurations, switch to compatible endpoints

### 2.3 CLI/UX Changes
- **Definition**: Changes to command-line interface or user interaction patterns.
- **Examples**:
  - `/new` command behavior (reset vs. new session)
  - TUI session isolation
  - Status output format changes
- **Impact**: User workflow disrupted, muscle memory causes errors
- **Detection**: Documentation review, hands-on testing
- **Mitigation**: Update user habits, scripts, or aliases

### 2.4 Performance/Resource Changes
- **Definition**: Changes to resource usage or performance characteristics.
- **Examples**:
  - Plugin startup lazy-loading
  - Memory/compaction algorithm changes
  - Caching behavior changes
- **Impact**:
  - Slower startup or response times
  - Increased memory/CPU usage
  - Cache-related staleness issues
- **Detection**: Performance monitoring, load testing
- **Mitigation**: Adjust resource limits, review tuning parameters

### 2.5 Security Policy Changes
- **Definition**: Changes to security validation or enforcement (not config-based).
- **Examples**:
  - Fail-closed config validation (previously permissive)
  - Archive extraction hardening
  - Secret sanitization in logs/status
- **Impact**:
  - Previously allowed operations now blocked
  - Logs show less diagnostic info
- **Detection**: Audit logs, security test suite
- **Mitigation**: Adjust security policies if needed, accept stricter defaults

---

## Risk Scoring Matrix

Use this matrix to prioritize risks:

| Impact \ Likelihood | High | Medium | Low |
|---------------------|------|--------|-----|
| **Critical** (data loss, service down) | **P0** - Block upgrade | **P1** - Test before upgrade | **P2** - Monitor post-upgrade |
| **High** (major disruption) | **P1** - Test before upgrade | **P2** - Monitor post-upgrade | **P3** - Document for awareness |
| **Medium** (workflow friction) | **P2** - Monitor post-upgrade | **P3** - Document for awareness | **P4** - Optional |
| **Low** (cosmetic) | **P3** - Document for awareness | **P4** - Optional | **P4** - Optional |

### Priority Definitions

- **P0**: Must mitigate before upgrade. Block upgrade if unresolved.
- **P1**: Must verify in staging or test environment before production upgrade.
- **P2**: Should verify immediately after production upgrade. Have rollback plan ready.
- **P3**: Document for awareness. Monitor for issues.
- **P4**: Informational. No action required unless user reports problems.

---

## Risk Assessment Workflow

For each identified change:

1. **Categorize**: Is this config-level (Category 1) or runtime-level (Category 2)?
2. **Subcategorize**: Which specific subtype (1.1, 1.2, 2.1, etc.)?
3. **Assess Impact**: What happens if this breaks? (Critical/High/Medium/Low)
4. **Assess Likelihood**: How likely is this to affect our specific deployment? (High/Medium/Low)
5. **Assign Priority**: Use matrix above
6. **Define Mitigation**: Config change, workflow adjustment, or verification test?
7. **Define Verification**: How do we confirm this works post-upgrade?

---

## Examples

### Example 1: Config-Level Risk
**Change**: "Gateway auth now requires explicit `gateway.auth.mode`"
- **Category**: 1.2 (Default Value Changes)
- **Impact**: High (gateway fails to start)
- **Likelihood**: High (our config has both token and password)
- **Priority**: P0
- **Mitigation**: Add `"mode": "token"` to config before upgrade
- **Verification**: Run `openclaw doctor` pre-upgrade, check gateway starts post-upgrade

### Example 2: Runtime-Level Risk
**Change**: "TUI `/new` creates independent sessions instead of resetting shared session"
- **Category**: 2.3 (CLI/UX Changes)
- **Impact**: Medium (user workflow disrupted)
- **Likelihood**: High (we use TUI regularly)
- **Priority**: P2
- **Mitigation**: Document new behavior, switch to `/reset` for session reset
- **Verification**: Test `/new` in TUI post-upgrade, confirm independent session created

### Example 3: Runtime-Level Risk
**Change**: "Force `supportsUsageInStreaming=false` for non-native OpenAI-compatible providers"
- **Category**: 2.2 (Protocol/API Compatibility)
- **Impact**: High (streaming responses may fail)
- **Likelihood**: Medium (we use `google-antigravity` with custom endpoint)
- **Priority**: P1
- **Mitigation**: Test streaming with `google-antigravity` before upgrade
- **Verification**: Trigger long completion post-upgrade, verify no mid-stream failure
