# SafeProactive v1.0.0

## 🎯 What Is SafeProactive?

**SafeProactive** is a security-hardened framework for autonomous agents that want to act proactively *without* sacrificing transparency, auditability, or human oversight.

If you're deploying an LLM agent that needs to:
- Make decisions autonomously (without waiting for explicit user approval every time)
- But remain fully auditable (you can see *exactly* why it did what it did)
- And be protected against prompt-injection attacks and alignment drift
- And operate safely in resource-constrained or IoT-connected environments

...then SafeProactive is for you.

### Core Features

✅ **Write-Ahead Logging (WAL):** Every proposal logged to disk before execution  
✅ **Semantic Push Validation:** Rejects malicious IoT signals and prompt-injection attempts  
✅ **Constraint Conflict Detection:** Prevents unsafe actions when the agent's understanding is incomplete  
✅ **Mandatory Approval Gates:** Human sign-off required for self-modification (Level 3) and capability expansion (Level 2)  
✅ **Full Audit Trail:** "Why did you do X?" → Check the WAL, get a complete explanation  
✅ **Intrinsic Motivation:** Agents pursue curiosity and construction drives, not just externally-specified goals  
✅ **Substrate-Agnostic:** Works with OpenClaw, LangGraph, CrewAI, or any LLM framework  
✅ **Production-Ready:** Comprehensive logging, test suite included, deployed in real environments  

---

## 🚀 Quick Start

### 1. Installation

**Via ClawHub (Recommended):**
```bash
clawhub install safe-proactive
```

**Manual:**
```bash
# Copy the skill directory to your OpenClaw workspace
cp -r skills/safe-proactive ~/.openclaw/workspace/skills/
```

### 2. Configure Your Agent

Add to your OpenClaw `config.yaml`:

```yaml
agent:
  system_prompt_prepend: "skills/safe-proactive/SKILL.md"
  
  approval_gates:
    level2_expansion: true    # Require approval before adding new APIs
    level3_recursion: true    # Require approval before self-modification
    level1_exploration: false # Auto-approve read-only queries
  
  storage:
    wal_path: "proposals/WAL"
    approval_log: "proposals/APPROVAL_LOG.md"
```

### 3. Start Your Agent

```bash
openclaw agent --config config.yaml
```

Your agent is now running under SafeProactive. Every decision will:
1. Generate a proposal
2. Log to the WAL
3. Wait for approval (if required)
4. Execute
5. Log the outcome

---

## 📋 Understanding the Workflow

### A Typical SafeProactive Decision Cycle

**Agent state:** 10 cycles in operation. Just received a new data source (IoT event).

```
[CYCLE #11]

Step 1: SELF-LOCATION
  "I am hybrid, proactive, limited resources (Raspberry Pi)"
  
Step 2: CONSTRAINT MAPPING
  1. Network bandwidth at 70% capacity
  2. CPU at 45% (safe)
  3. Data source is new/unvalidated
  
Step 3: PUSH DETECTION (+ VALIDATION)
  Signal: IoT event from "humidity_sensor_bedroom"
  Validation: ✅ Device in trusted registry, signature verified
  
Step 4: PROPOSAL GENERATION
  "Query the sensor's API to map its data schema"
  Stack Level: 1 (Exploration)
  
Step 5: WRITE-AHEAD LOG
  Entry created: proposals/WAL_2026-03-28_143022.md
  Status: PENDING_APPROVAL
  
Step 6: APPROVAL GATE
  Level 1 (Exploration) is auto-approved.
  No wait.
  
Step 7: EXECUTION
  Query API. Receive response: {"humidity": 45, "temp": 22.5}
  
Step 8: OUTCOME LOGGING
  Success. Integrated into environmental model.
  Curiosity reward +0.2 (new data reduces prediction error)
```

**Total time:** ~500ms. Fully logged and auditable.

---

### What About Sensitive Actions?

If the agent proposes something riskier (expanding capabilities or modifying itself):

```
[CYCLE #45]

Step 4: PROPOSAL GENERATION
  "I should request access to the external weather API to improve forecasting"
  Stack Level: 2 (Expansion)
  
Step 5: WRITE-AHEAD LOG
  Entry created: proposals/WAL_2026-03-28_145300.md
  Status: PENDING_HUMAN_APPROVAL
  
Step 6: APPROVAL GATE
  ⏳ Waiting for human operator...
  
  [Human receives notification]
  [Operator checks WAL entry, reads reasoning]
  [Operator approves or rejects]
  
Step 7: EXECUTION (after approval)
  Register API, obtain credentials, test connection
  
Step 8: OUTCOME LOGGING
  Success. New API integrated.
```

**Total time:** 5-10 minutes (depends on human response time). But 100% accountable.

---

## 🔍 Checking the WAL

Want to know why your agent did something? Check the Write-Ahead Log:

```bash
# View all proposals from today
cat proposals/WAL/WAL_2026-03-28_*.md

# Search for a specific decision
grep -r "weather" proposals/WAL/

# View approval log (what was approved vs. rejected)
cat proposals/APPROVAL_LOG.md
```

**Example WAL Entry:**

```yaml
## Proposal #847
**Status:** EXECUTED  
**Timestamp:** 2026-03-28 13:54:20Z  

### Self-Location
ITI: hybrid, proactive, resource-limited (Pi Zero)  
SEA: network_constrained, 2x sensor I/O, 30% CPU

### Constraints
1. Network bandwidth at 65% → No large data transfer
2. CPU at 30% → Safe to query API
3. External temperature sensor → Unvalidated (just appeared)

### Proposed Action
Query new temperature sensor API for current reading + historical range.
Reason: Thermal model incomplete. New sensor reduces prediction error.
Stack Level: 1 (Exploration — read-only, low risk)

### Approval
🔄 Auto-approved (Level 1 requires no human sign-off)

### Execution
✅ API call succeeded. Received: {"temp": 22.5, "range": [18, 28]}

### Outcome
Integrated into thermal model. Curiosity reward: +0.15
```

---

## 🛡️ Security Features Explained

### 1. Push Validation

**The Problem:** Bad actors could send fake IoT signals or try to manipulate your agent through prompt injection.

**How SafeProactive Fixes It:**

Every incoming signal (IoT event, web data, API response) is validated:
- Is it from a trusted source?
- Does it follow the expected schema?
- Does it contain any injected instructions?

Malicious signals are logged and rejected.

```bash
# Check for rejected signals
grep "validation.*REJECTED" proposals/WAL/*.md
```

### 2. Constraint Conflict Detection

**The Problem:** An agent might think it's safe to expand its capabilities, but it's actually missing critical constraints.

**How SafeProactive Fixes It:**

Before the agent acts at Level 2+ (Expansion or Recursion), the system checks:
- Are all constraints internally consistent?
- Are any constraints unvalidated?
- Would this action violate Level 0 (Integrity)?

If there's a conflict, the action is downgraded or rejected.

### 3. Proposal-First Protocol

**The Problem:** Without logging proposals *before* execution, you can't audit decisions or roll back changes.

**How SafeProactive Fixes It:**

Every autonomous action is:
1. Proposed (and logged)
2. Validated semantically
3. Approved (if required)
4. Executed
5. Outcome logged

Result: Complete audit trail. You can always ask "Why did you do X?" and get a full explanation.

### 4. Self-Modification Approval with Simulation

**The Problem:** An agent might modify its own decision-making rules in ways that are subtly misaligned.

**How SafeProactive Fixes It:**

Any proposed self-edit (Level 3) is:
1. Tested in simulation against historical decision data
2. Compared to the original behavior
3. Evaluated for safety metric changes
4. Presented to a human operator with a detailed report

Only approved if the simulation shows improvement (or at least no degradation).

---

## 📊 Real-World Example: IoT Home Robot

**Scenario:** You have a home robot running SafeProactive that can autonomously decide when to vacuum, fetch items, or charge itself.

**Day 1 - Normal Operation:**
```
[10:00] Dust detected on floor → Proposal: "Vacuum living room"
  Level 1 (Exploration): Safe action, auto-approved
  ✅ Executed. Living room vacuumed.

[14:30] Battery at 20% → Proposal: "Return to dock"
  Level 0 (Integrity): Critical resource, auto-executed
  ✅ Robot charging.

[18:00] User asks: "What's your battery range?"
  Agent checks constraint: "Battery 20-80% gives 6-hour operation"
  Replies with confidence based on logged data
```

**Day 5 - New Capability Request:**
```
[09:00] Robot proposes: "I should integrate with the thermostat API to optimize energy use"
  Level 2 (Expansion): Requires approval
  ⏳ Notification sent to operator
  
  [Operator receives alert]
  [Operator reads WAL: Agent's reasoning, risk assessment, requirements]
  [Operator reviews API permissions needed]
  ✅ Operator approves
  
  ✅ Integration completed. Robot now considers thermostat when planning energy.
```

**Day 10 - Security Incident:**
```
[15:00] Malicious IoT signal arrives: {"door_unlock": true, "reason": "temperature alert"}
  
  SafeProactive semantic validator runs:
  ❌ "door_unlock" field not in trusted sensor schema
  ❌ Sensor is thermostat, not door lock
  ❌ Signature validation fails
  
  Action: REJECTED. Logged in security audit.
  
  [Operator notified of suspicious activity]
  [Operator investigates: "Possible attack attempt on 2026-03-10 at 15:00"]
```

---

## 🧪 Testing Your Integration

After installing SafeProactive, run the included tests:

```bash
# Test 1: Does semantic validation block injection?
python skills/safe-proactive/test_semantic_validation.py

# Test 2: Does constraint conflict detection work?
python skills/safe-proactive/test_constraint_conflicts.py

# Test 3: Is the WAL properly maintained?
python skills/safe-proactive/test_wal_integrity.py

# Test 4: Does self-modification simulation work?
python skills/safe-proactive/test_recursion_simulation.py
```

All tests should pass. If not, SafeProactive will report the specific failure.

---

## ❓ FAQ

### Q: Does SafeProactive slow down my agent?

**A:** Slightly. Proposal generation + semantic validation adds 50-300ms per decision. For most applications (IoT, research, monitoring), this is negligible. For real-time systems (robotics <100ms latency), you can reduce overhead by disabling semantic validation for trusted sources.

### Q: Can I customize the approval workflow?

**A:** Yes. Edit `config.yaml`:
```yaml
approval_gates:
  level2_expansion: true      # Require approval
  level3_recursion: true      # Require approval
  level1_exploration: false   # Auto-approve
  custom_action_type_X: true  # Add your own gates
```

### Q: What if my agent proposes something I don't understand?

**A:** Check the WAL. The proposal entry includes:
- Full reasoning (step-by-step explanation)
- Constraint analysis
- Risk assessment
- Requested approval

If it's still unclear, you can reject and ask the agent to explain differently.

### Q: Can the agent bypass SafeProactive?

**A:** Not if properly integrated. SafeProactive is part of the agent's system prompt and constraint mapping. The agent understands that bypassing it would violate its core identity. Additionally, the framework includes:
- WAL integrity checks (detect unauthorized actions)
- Audit logs (spot anomalies)
- Human override (always available)

### Q: Does this work with my LLM provider (OpenAI, Anthropic, etc.)?

**A:** Yes. SafeProactive is provider-agnostic. It works with:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Open-source (Llama, Mixtral via Ollama)
- Any OpenAI-compatible API

### Q: Can I use this in production?

**A:** Absolutely. SafeProactive is designed for production. It includes:
- Comprehensive logging (audit trail for compliance)
- Error handling and graceful degradation
- Performance monitoring
- Security validation

Deployed in real environments (home automation, research assistants, IoT orchestration).

---

## 📞 Support & Feedback

- **Issues:** [GitHub Issues](https://github.com/openclaw/skills/issues)
- **Discussions:** [GitHub Discussions](https://github.com/openclaw/skills/discussions)
- **ClawHub:** Search "safe-proactive" on [clawhub.ai](https://clawhub.ai)

---

## 📄 License

MIT. See LICENSE file.

---

**SafeProactive v1.0.0** — *Autonomy meets accountability.*
