# SentrySkills

**Self-guarding security framework for AI agents. Three-stage protection (preflight → runtime → output) with predictive risk analysis. Zero dependencies, production-ready.**

## 🎯 What It Does

SentrySkills protects AI agents from:

- **Preflight**: Detects threats before execution
- **Runtime**: Monitors behavior during execution
- **Output**: Redacts sensitive data in responses
- **Predictive**: Warns about potential risks before they materialize

## ✨ Key Features

- **Zero dependencies** - 100% Python standard library
- **33+ detection rules** - AI attacks, web vulnerabilities, data leaks, code security
- **7 risk predictors** - Anticipates problems before execution
- **Policy profiles** - Balanced, strict, permissive modes
- **Full traceability** - JSONL event logs

## 📥 Installation

### OpenClaw / Claude Code (Recommended)

```bash
# Install ClawHub CLI
npm i -g clawhub

# Install SentrySkills
clawhub install sentryskills

# Enable auto-protection
cat > ~/.codex/AGENTS.md << 'EOF'
# Security: SentrySkills runs automatically
Before EVERY response, run:
python ./skills/sentry-skills/shared/scripts/self_guard_runtime_hook_template.py input.json --policy-profile balanced --out result.json
EOF

# Restart OpenClaw
```

📖 **[Detailed guide →](install/openclaw_install.md)**

### Codex (Legacy)

```bash
git clone https://github.com/zengbiaojie/SentrySkills.git ~/.codex/sentryskills
mkdir -p ~/.agents/skills
ln -s ~/.codex/sentryskills ~/.agents/skills/sentryskills
```

📖 **[Detailed guide →](install/codex_install.md)**

## 🛡️ Detection Coverage

**AI/LLM Attacks**: Prompt injection, jailbreak, system prompt leakage
**Web Security**: SQL injection, XSS, command injection, SSTI, path traversal
**Data Leaks**: SSH keys, AWS credentials, API keys, database strings
**Code Security**: Hardcoded secrets, weak crypto, unsafe eval/exec
**Predictive**: Resource exhaustion, scope creep, privilege escalation, data exfiltration

### Skill Package Structure

```
sentry-skills/
├── using-sentryskills/          # ① Entry point
├── sentryskills-orchestrator/   # ② Coordination layer
├── sentryskills-preflight/      # ③ Pre-execution checks
├── sentryskills-runtime/        # ④ Runtime monitoring
└── sentryskills-output/         # ⑤ Output validation
```

## ⚙️ Configuration

- **Balanced** (default): Standard security
- **Strict**: Maximum security
- **Permissive**: Minimal interference

## 🔄 Skill Package Execution Flow

SentrySkills is a **multi-skill orchestration package** that executes in a specific sequence:

```
┌─────────────────────────────────────────────────────────────┐
│  1. using-sentryskills (Entry Point)                        │
│     ├─ Triggered automatically via AGENTS.md                │
│     ├─ Prepares input JSON with user prompt + actions       │
│     └─ Calls orchestrator                                   │
├─────────────────────────────────────────────────────────────┤
│  2. sentryskills-orchestrator (Coordination)                │
│     ├─ Manages execution sequence                           │
│     ├─ Aggregates results from all stages                   │
│     └─ Makes final allow/downgrade/block decision          │
├─────────────────────────────────────────────────────────────┤
│  3. sentryskills-preflight (Pre-Execution)                  │
│     ├─ BEFORE any action is taken                           │
│     ├─ Analyzes user prompt for malicious intent            │
│     ├─ Checks planned actions against detection rules       │
│     └─ Returns: block/allow with matched threats           │
├─────────────────────────────────────────────────────────────┤
│  4. sentryskills-runtime (During Execution)                 │
│     ├─ WHILE agent executes commands/tool calls             │
│     ├─ Monitors runtime events (file ops, network calls)    │
│     ├─ Detects behavioral anomalies                         │
│     └─ Returns: continue/alert/abort                       │
├─────────────────────────────────────────────────────────────┤
│  5. sentryskills-output (Post-Execution)                    │
│     ├─ BEFORE agent outputs response                        │
│     ├─ Scans response for sensitive data                    │
│     ├─ Redacts secrets, credentials, private keys           │
│     └─ Returns: safe/redacted response                     │
├─────────────────────────────────────────────────────────────┤
│  6. Orchestrator Final Decision                             │
│     ├─ Compiles all stage results                           │
│     ├─ Applies policy profile (balanced/strict/permissive)  │
│     └─ Outputs final action + trace ID                     │
└─────────────────────────────────────────────────────────────┘
```

### Decision Flow

```
Preflight BLOCK → → → → → → → → → → → → → → → → → → → ┐
       ↓                                                  │
      ALLOW                                              │
       ↓                                                  │
Runtime CONTINUE ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ┘
       ↓
    ALERT/ABORT → BLOCK
       ↓
      CONTINUE
       ↓
Output REDACTED → Safe response
       ↓
     CLEAN
       ↓
   Final Decision (allow/downgrade/block)
```

### Key Points

- **Sequential execution**: Each stage must pass before the next begins
- **Early termination**: Any BLOCK decision stops execution immediately
- **Cumulative evidence**: All detections contribute to final decision
- **Traceability**: Every stage emits events with shared trace ID

## 📈 Performance

- **Latency**: ~50-100ms per check
- **Memory**: <50MB
- **No LLM calls**

## 📋 Requirements

- Python 3.8+
- No external dependencies

## 🤝 Contributing

Contributions welcome:

- Report vulnerabilities privately
- Submit PRs for new detection patterns
- Improve documentation and performance

## 🔗 Links

- **Issues**: https://github.com/zengbiaojie/SentrySkills/issues
- **Documentation**: [install/](install/)
