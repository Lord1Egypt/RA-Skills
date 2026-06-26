# Upgrade Guardian Skill

A cognitive protocol for safely managing OpenClaw application upgrades by identifying both configuration-level and runtime-level risks.

## Overview

Upgrade Guardian helps agents analyze OpenClaw changelogs and identify potential breaking changes before they cause problems. It goes beyond simple "BREAKING" labels to detect subtle behavioral shifts that could disrupt production systems.

## What It Does

Upgrade Guardian analyzes upgrades across **two risk categories**:

### 1. Configuration-Level Risks
Changes that affect `openclaw.json` or static config files:
- Schema breaking changes
- Default value changes
- Deprecated fields
- Validation tightening

### 2. Runtime-Level Risks
Changes that affect behavior without config modifications:
- Behavioral logic changes (routing, delivery, session handling)
- Protocol/API compatibility (streaming, CDP, providers)
- CLI/UX changes (command behavior, TUI workflow)
- Performance/resource changes (caching, lazy loading)

## Skill Structure

```
upgrade-guardian/
├── SKILL.md                              # Main protocol (router)
├── README.md                             # This file
└── references/
    ├── changelog_analysis_patterns.md    # Semantic analysis patterns
    ├── RISK_CATEGORIES.md                # Risk taxonomy & scoring matrix
    ├── AUDIT_REPORT_TEMPLATE.md          # Report structure & examples
    └── VERIFICATION_CHECKLIST.md         # Common verification tests
```

## How to Use

### When to Trigger
Use Upgrade Guardian when:
- Operator announces: "We're upgrading from vA to vB"
- Operator asks: "What changed between these versions?"
- Operator wants: "Risk assessment for upcoming upgrade"

### Protocol Execution

#### Phase 1: Information Gathering
1. Fetch CHANGELOG for target version range
2. Perform semantic analysis using `references/changelog_analysis_patterns.md`
3. Cross-reference with current `openclaw.json` and active workflows

#### Phase 2: Risk Assessment
1. Identify config-level risks (schema, defaults, validation)
2. Identify runtime-level risks (behavior, protocols, UX)
3. Score risks by Impact × Likelihood using matrix in `references/RISK_CATEGORIES.md`
4. Generate audit report using template in `references/AUDIT_REPORT_TEMPLATE.md`

#### Phase 3: Mitigation & Verification
1. Propose config hardening for config risks
2. Document workflow adjustments for runtime risks
3. Define verification tests using `references/VERIFICATION_CHECKLIST.md`
4. Execute verification post-upgrade and report results

### Example Output

```markdown
# Upgrade Audit Report: v2026.3.7 → v2026.3.8

**Summary**: 1 critical config risk, 2 medium runtime risks.

## 🔴 Critical Risk: Gateway Auth Mode [P0]
**Evidence**: "Gateway auth now requires explicit gateway.auth.mode"
**Our Vulnerability**: Our config has both token and password but no mode set
**Mitigation**: Add `"mode": "token"` to config
**Verification**: Run `openclaw doctor` pre-upgrade

## 🟠 Runtime Risk: TUI `/new` Behavior [P2]
**Evidence**: "TUI `/new` creates independent sessions instead of resetting"
**Affected Workflows**: Users who use `/new` to clear conversations
**Verification**: Test `/new` in TUI post-upgrade

## Recommendation
✅ PROCEED after applying P0 mitigation
```

## Key Concepts

### Progressive Disclosure
- **SKILL.md**: Router-style overview (88 lines)
- **references/**: Detailed content for each aspect
- Each reference doc is self-contained and can be read independently

### Docs-First Approach
- Every protocol step has a corresponding reference doc
- Templates provided for reports and checklists
- Examples illustrate both config and runtime risks

### Risk Scoring Matrix

| Impact \ Likelihood | High | Medium | Low |
|---------------------|------|--------|-----|
| **Critical** | P0 - Block upgrade | P1 - Test before | P2 - Monitor |
| **High** | P1 - Test before | P2 - Monitor | P3 - Document |
| **Medium** | P2 - Monitor | P3 - Document | P4 - Optional |
| **Low** | P3 - Document | P4 - Optional | P4 - Optional |

### Priority Definitions
- **P0**: Must mitigate before upgrade. Block upgrade if unresolved.
- **P1**: Must test in staging before production upgrade.
- **P2**: Should verify immediately after upgrade. Have rollback plan.
- **P3**: Document for awareness. Monitor for issues.
- **P4**: Informational. No action required.

## Reference Docs Summary

### changelog_analysis_patterns.md
Semantic analysis patterns for identifying risks:
- High-risk keywords (refactor, unify, centralize)
- Config-level keywords (schema, validation, deprecate)
- Runtime-level keywords (routing, session, streaming, CLI)
- Pattern combinations and risk indicators
- Analysis process with examples

### RISK_CATEGORIES.md
Detailed risk taxonomy:
- Category 1: Configuration-level risks (1.1-1.4)
- Category 2: Runtime-level risks (2.1-2.5)
- Risk scoring matrix with priority definitions
- Risk assessment workflow
- Example risk analyses

### AUDIT_REPORT_TEMPLATE.md
Report structure for communicating findings:
- Executive summary template
- Config risk section (with jq paths, mitigations, verification)
- Runtime risk section (with workflows, behavioral changes, tests)
- Pre/post-upgrade checklists
- Short-form template for low-risk upgrades

### VERIFICATION_CHECKLIST.md
Catalog of common verification tests:
- Pre-upgrade: health checks, backup, documentation
- Post-upgrade: gateway, bot, models, sessions, TUI, cron, browser
- Risk-specific tests (auth mode, TUI /new, streaming, cron async)
- Quick reference: 5 essential tests
- Automation script example

## Design Principles

1. **Conservative by Default**: Better to flag false positives than miss silent breaking changes
2. **Explicit Over Implicit**: Make implicit assumptions explicit before they break
3. **Test-Driven Verification**: Every risk should have a concrete verification test
4. **Operator Empowerment**: Provide clear mitigations and rollback plans
5. **Workflow Awareness**: Runtime risks matter as much as config risks

## Common Workflows

### Low-Risk Upgrade (e.g., patch release)
```bash
# Quick analysis
1. Scan CHANGELOG for keywords
2. Identify no breaking changes
3. Generate short-form report
4. Run basic verification post-upgrade
```

### High-Risk Upgrade (e.g., major version)
```bash
# Full protocol
1. Deep semantic analysis of CHANGELOG
2. Cross-reference with entire config
3. Identify all active workflows
4. Score risks, generate full report
5. Pre-upgrade mitigations (config changes)
6. Staging testing for P1 risks
7. Production upgrade with rollback plan
8. Full verification checklist execution
```

### Config-Heavy Environment
```bash
# Focus on config risks
1. Schema validation analysis
2. Default value change detection
3. Deprecated field migration
4. Verification: `openclaw doctor` + config load tests
```

### Runtime-Heavy Environment
```bash
# Focus on runtime risks
1. Behavioral change analysis
2. Workflow dependency mapping
3. Protocol compatibility checks
4. Verification: User workflow testing, monitoring
```

## Contributing

When updating this skill:
1. Maintain progressive disclosure (SKILL.md as router)
2. Keep reference docs self-contained
3. Add examples for new risk patterns
4. Update verification checklist with new tests
5. Preserve risk scoring matrix consistency

## Related Skills

- `openclaw-source-of-truth`: For understanding OpenClaw architecture
- `telegram-group-manager`: For Telegram-specific config risks
- `gateway-healthcheck`: For post-upgrade health verification

## Version History

- **v2.0** (2026-03-09): Added runtime-level risk analysis
  - New: RISK_CATEGORIES.md with full taxonomy
  - New: AUDIT_REPORT_TEMPLATE.md with runtime sections
  - New: VERIFICATION_CHECKLIST.md with behavioral tests
  - Updated: changelog_analysis_patterns.md with runtime keywords
  - Updated: SKILL.md to cover both config and runtime risks

- **v1.0** (2026-03-01): Initial release
  - Config-focused risk analysis
  - Semantic patterns for changelog analysis
  - Basic verification checklist

## License

MIT © OpenClaw Community
