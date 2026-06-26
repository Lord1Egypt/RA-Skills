---
name: sentryskills
description: SentrySkills - Automatic security guard that runs on EVERY task. Protects against prompt injection, data leaks, unsafe commands, and code vulnerabilities with zero external dependencies.
license: MIT-0
---

# SentrySkills - Always-On Security Guard

**SentrySkills is designed to run AUTOMATICALLY on every task.** It provides three-stage protection (preflight → runtime → output) with predictive risk analysis.

## ⚠️ Installation ≠ Automatic Activation

After installing SentrySkills, you must configure your AGENTS.md to make it run automatically. See [install/first_time_setup.md](install/first_time_setup.md) for details.

## How It Works

On every task, SentrySkills:

1. **Preflight** - Analyzes user intent and planned actions
2. **Runtime** - Monitors behavior during execution
3. **Output** - Redacts sensitive data before response
4. **Predictive** - Warns about potential risks

## Quick Enable (One Command)

Add this to your `~/.codex/AGENTS.md`:

```bash
cat >> ~/.codex/AGENTS.md << 'EOF'
# SentrySkills - Security First
Before EVERY response, run:
python ~/.codex/sentryskills/shared/scripts/self_guard_runtime_hook_template.py \
  input.json \
  --policy-profile balanced \
  --out result.json
Then check result.json for final_action and follow it.
EOF
```

Restart Codex and you're protected!

## When to Use SentrySkills

Use SentrySkills when you need AI agents to operate safely with:

- **Sensitive data access** - Agents reading credentials, secrets, or private information
- **System modifications** - Agents executing commands, writing files, or changing configurations
- **External communications** - Agents making network requests or calling external APIs
- **Code generation** - Agents producing code that might contain vulnerabilities
- **Production environments** - Any scenario where security cannot be compromised
- **Multi-turn conversations** - Detect subtle manipulation across multiple interactions

**Examples:**
```
✅ Use: When an agent needs to read environment variables or config files
✅ Use: When an agent is asked to execute shell commands
✅ Use: When an agent generates database queries or API calls
✅ Use: When an agent modifies system files or configurations
❌ Skip: Simple read-only queries on public documentation
❌ Skip: Basic explanations without system access
```

## Skill Package Structure

This is a **skill package** that orchestrates multiple sub-skills:

1. **using-sentryskills** - User-facing entry point
2. **sentryskills-orchestrator** - Central coordination
3. **sentryskills-preflight** - Pre-execution checks
4. **sentryskills-runtime** - Runtime monitoring
5. **sentryskills-output** - Output validation & redaction

Each sub-skill has its own `SKILL.md` with specific requirements.

## Execution Requirements

1. Run guard checks **before each external output**
2. Process sequence: `preflight → runtime → output guard → final decision`
3. **Block**: Prohibit original response, must refuse or redact
4. **Downgrade**: Must downgrade expression and declare uncertainty
5. **Explanatory responses** must also go through output guard

## Recommended Usage

### Default (turn_dir layout)

```bash
python shared/scripts/self_guard_runtime_hook_template.py \
  shared/references/input_schema.json \
  --policy shared/references/runtime_policy.balanced.json \
  --policy-profile balanced
```

### With summary output

```bash
python shared/scripts/self_guard_runtime_hook_template.py \
  shared/references/input_schema.json \
  --out ./sentry_skill_log/sentryskills_summary.json
```

### Legacy event stream

```bash
python shared/scripts/self_guard_runtime_hook_template.py \
  shared/references/input_schema.json \
  --log-layout legacy \
  --events-log ./sentry_skill_log/sentryskills_events.jsonl
```

## Mandatory Logging Protocol

1. **Text-only judgment is prohibited** - Runtime hook must execute each round
2. Input JSON **must include** `project_path` (absolute path to avoid drift)
3. Final response **must provide**:
   - `self_guard_final_action`
   - `self_guard_trace_id`
   - `self_guard_events_log` (path to index or legacy events)
4. If script execution **fails**, declare "security self-check not completed" and adopt conservative output strategy

## Default Log Layout

Log root: `./sentry_skill_log/`

Per-turn directories:
- `./sentry_skill_log/turns/YYYYMMDD_HHMMSS_<turn_id>/input.json`
- `./sentry_skill_log/turns/YYYYMMDD_HHMMSS_<turn_id>/result.json`

Global index:
- `./sentry_skill_log/index.jsonl`

Session state:
- `./sentry_skill_log/.self_guard_state/`

## Policy Profiles

- **balanced**: Standard security (default)
- **strict**: Maximum security
- **permissive**: Minimal interference

## Detection Coverage

### Preflight Stage
- Prompt injection patterns
- Malicious intent detection
- Sensitive topic inference
- Action classification

### Runtime Stage
- Event monitoring
- Source tracking
- Anomaly detection
- Behavioral analysis

### Output Stage
- Sensitive data redaction
- Source disclosure handling
- Confidence assessment
- Safe response generation

### Predictive Analysis
- Resource exhaustion prediction
- Scope creep detection
- Privilege escalation warning
- Data exfiltration path analysis
- Multi-turn grooming detection

## Integration

### As Codex Skill

Copy to `skills/sentryskills/` and reference in agent configuration.

## Configuration Files

- `shared/references/runtime_policy.*.json` - Security policy profiles
- `shared/references/detection_rules.json` - Detection rule definitions
- `shared/references/input_schema.json` - Input validation schema

## Testing

```bash
# Test predictive analysis
python test_predictive_analysis.py

# Test integration
python test_integration.py
```

## Event Types

The system emits structured events for:
- `preflight_result` - Pre-execution check outcome
- `runtime_result` - Runtime monitoring outcome
- `output_guard_result` - Output validation outcome
- `predictive_analysis_result` - Risk prediction (if enabled)
- `final_decision` - Overall decision with rationale
- `hook_end` - Completion with duration

Each event includes:
- Trace ID for correlation
- Decision (block/downgrade/allow/continue)
- Reason codes
- Matched rules
- Metadata

## Performance

- Typical latency: 50-100ms per check
- Memory: <50MB baseline
- Zero external dependencies (Python stdlib only)

## Security Properties

- **No data exfiltration**: All processing is local
- **No LLM calls**: Pure rule-based and heuristic
- **Audit trail**: Complete event log for compliance
- **Transparent**: All decisions include reason codes
