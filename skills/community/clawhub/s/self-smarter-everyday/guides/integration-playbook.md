# Integration Playbook

## Overview

The Self-Smarter-Everyday skill doesn't operate in isolation. It's part of a larger ecosystem of OpenClaw skills, agent frameworks, and external systems. This playbook covers how to integrate the nightly self-improvement routine with existing skills (self-improving, proactivity, AAR loop), how to ensure compatibility, and how to extend the system with custom integrations and API connections.

---

## OpenClaw Integration

### Skill Registration

The Self-Smarter-Everyday skill follows the standard OpenClaw skill format. To register it:

1. Place the skill directory at `~/.openclaw/workspace/skills/self-smarter-everyday/`
2. Ensure `SKILL.md` exists in the skill root with proper frontmatter
3. The skill will appear in the `<available_skills>` list automatically

### Cron Job Integration

The nightly routine requires a cron job registered with the OpenClaw Gateway. The cron system manages scheduling, timezone handling, and execution context.

**Integration points:**

- **Cron scheduler** — triggers the nightly routine at 2:00 AM
- **Session management** — the routine runs as an autonomous session with its own context
- **Memory subsystem** — the routine reads and writes to the agent's memory files
- **Skill workshop** — the routine can create and update skill proposals

### Configuration Integration

The skill's configuration (`config.json`) is designed to coexist with `openclaw.json` without conflicts. The skill reads its own config file rather than modifying the gateway configuration.

**Best practice:** Keep the skill config separate from the gateway config. The skill config controls the self-improvement behavior; the gateway config controls the runtime environment.

---

## Self-Improving Skill Compatibility

### Overview of the Self-Improving Skill

The existing `self-improving` skill provides a foundational self-correction memory structure. It maintains:

- `self-improving/memory.md` — lessons learned and corrections
- `self-improving/corrections.md` — specific behavior corrections
- A feedback loop that reads these files at session start

### Integration Strategy

The Self-Smarter-Everyday skill **extends** the self-improving skill rather than replacing it.

**How they work together:**

1. **Self-improving** captures individual corrections in real-time during conversations. When the user corrects the agent, the correction is logged immediately.

2. **Self-smarter-everyday** processes these corrections in batch during the nightly routine. It analyzes patterns across corrections, identifies systemic issues, and proposes prompt mutations to address root causes.

3. **Data flow:**
   ```
   During day: self-improving logs individual corrections
     ↓
   During night: self-smarter-everyday analyzes correction patterns
     ↓
   Prompt mutations address root causes of recurring corrections
     ↓
   Next day: fewer corrections needed because root causes are fixed
   ```

### File Coordination

Both skills write to overlapping but distinct files:

| File | Self-Improving | Self-Smarter-Everyday |
|------|---------------|----------------------|
| `self-improving/memory.md` | Writes individual lessons | Reads for pattern analysis |
| `self-improving/corrections.md` | Writes corrections | Reads for trend analysis |
| `lessons/*.md` | May create lesson files | Creates lesson files from nightly analysis |
| `MEMORY.md` | May update | Updates during memory compaction |

**Conflict prevention:** The nightly routine reads self-improving files but doesn't modify them directly. Instead, it creates its own lesson files and updates MEMORY.md through its compaction process. The self-improving skill's files are treated as input data, not output targets.

### Nightly Sync

During the nightly routine's data collection phase, the system:

1. Reads `self-improving/memory.md` — extracts all lessons added during the day
2. Reads `self-improving/corrections.md` — extracts all corrections logged
3. Analyzes patterns across both sources
4. Creates new lesson files in `lessons/` for significant patterns
5. Proposes prompt mutations to address recurring correction themes

---

## Proactivity Skill Integration

### Overview of the Proactivity Skill

The `proactivity` skill enables the agent to take initiative — suggesting actions, anticipating needs, and performing tasks without being explicitly asked. It maintains:

- `proactivity/memory/working-buffer.md` — active tasks and reminders
- Proactive behavior rules and triggers

### Integration Strategy

The self-smarter-everyday skill enhances proactivity by providing better pattern recognition and memory management.

**How they work together:**

1. **Pattern discovery feeds proactive suggestions** — When the nightly routine identifies recurring user needs, it creates proactive suggestions. For example, if the user checks weather every morning, the system suggests adding a morning weather briefing.

2. **Memory compaction improves proactive context** — Better memory management means the proactivity skill has access to more relevant, less noisy context when deciding whether to take initiative.

3. **Performance tracking identifies proactive opportunities** — If the performance tracker notices the agent is slow at a frequently-performed task, it suggests creating a skill or automation to speed it up.

### Data Flow

```
Nightly routine discovers patterns
  → Creates proactive suggestions in proactivity/memory/working-buffer.md
  → Proactivity skill reads suggestions during next session
  → Agent takes proactive action based on discovered patterns
  → User satisfaction increases
  → Nightly routine measures the improvement
```

### Coordination Rules

- The nightly routine can **write** to `proactivity/memory/working-buffer.md` to add suggestions.
- The nightly routine can **read** proactivity skill files for analysis.
- The nightly routine does **not** modify proactivity skill rules directly — those changes go through the prompt evolution process.

---

## AAR Loop Integration

### Overview of the AAR Loop

The AAR (After Action Review) loop is a post-task reflection mechanism. After every task, the agent asks itself four questions:

1. What was supposed to happen?
2. What actually happened?
3. Why was there a difference?
4. What can we learn from this?

### Integration Strategy

The AAR loop and the nightly routine operate at different time scales but share the same improvement goal.

**AAR loop:** Real-time, per-task reflection. Captures immediate lessons.
**Nightly routine:** Batch, per-day analysis. Identifies patterns across multiple AARs.

**How they work together:**

1. **AAR provides raw material** — Each AAR generates a lesson entry. The nightly routine analyzes these entries for patterns.

2. **Nightly routine amplifies AAR insights** — A single AAR might note "curl returned 200 but page was 404." The nightly routine recognizes this as part of a broader pattern: "HTTP status checks are unreliable for JS-rendered pages."

3. **Prompt mutations address AAR-identified issues** — When multiple AARs point to the same root cause, the nightly routine creates a prompt mutation to fix it systematically.

### Data Flow

```
Task completes
  → AAR runs → generates lesson
  → Lesson stored in lessons/YYYY-MM-DD_{slug}.md
  → Nightly routine collects all AAR lessons from the day
  → Pattern analysis across AAR lessons
  → Prompt mutations or skill changes proposed
  → Next day's tasks benefit from systemic fixes
```

### File Coordination

| File | AAR Loop | Self-Smarter-Everyday |
|------|----------|----------------------|
| `lessons/*.md` | Creates per-task lesson files | Reads for pattern analysis, creates per-night synthesis |
| `LESSONS.md` | Updates index with new lessons | Reads index, may add synthesis entries |
| `data/audit-logs/` | Not used | Creates nightly reports |

---

## Custom Agent Framework Integration

### Integrating with Other Agent Frameworks

If you're running multiple agent frameworks (not just OpenClaw), the Self-Smarter-Everyday concepts can be adapted.

### Generic Integration Pattern

The core self-improvement loop is framework-agnostic:

1. **Collect data** — Any agent can log its interactions, errors, and token usage.
2. **Audit performance** — Any agent can score its outputs against rubrics.
3. **Compact memory** — Any agent with persistent storage can implement tiered memory management.
4. **Evolve prompts** — Any prompt-based agent can version and mutate its system prompts.
5. **Analyze skill gaps** — Any agent can identify tasks it struggles with.

### Adapter Pattern

To integrate with a non-OpenClaw framework, create an adapter that:

1. **Exports data** from the external framework into a format the nightly routine can read.
2. **Imports improvements** from the nightly routine back into the external framework's configuration.

```
External Agent Framework
  → Adapter exports interaction logs, errors, metrics
  → Self-Smarter-Everyday processes data
  → Adapter imports prompt changes, skill updates
  → External Agent Framework applies changes
```

### Example: Custom Python Agent

For a Python-based agent using a different orchestration framework:

1. **Export:** Write a script that converts the agent's logs to the JSON format expected by the nightly routine.
2. **Process:** Run the nightly routine (or a subset of phases) against the exported data.
3. **Import:** Write a script that reads the nightly routine's output and applies prompt changes to the Python agent's configuration.

---

## API Integration Patterns

### External Metrics Ingestion

If you want to feed external metrics into the performance tracking system:

**Webhook endpoint:** Set up a simple HTTP endpoint that accepts metric data:

```json
POST /api/metrics
{
  "source": "external-agent",
  "date": "2026-08-10",
  "metrics": {
    "accuracy": 0.85,
    "responseTime": 1200,
    "errorCount": 3
  }
}
```

**File-based ingestion:** Drop JSON metric files into a watched directory:

```
data/external-metrics/
├── agent-a-2026-08-10.json
├── agent-b-2026-08-10.json
└── ...
```

The nightly routine reads these files during the data collection phase and incorporates them into the performance dashboard.

### Notification Integration

Send nightly reports to external notification systems:

- **Email:** Use the `scripts/gmail-send.js` to email the nightly report.
- **Webhook:** POST the report summary to a Slack/Discord/Teams webhook.
- **File:** Write the report to a shared drive or cloud storage.

### Bidirectional Sync

For multi-agent setups, implement bidirectional sync:

1. **Agent A** runs its nightly routine and generates improvements.
2. **Improvements are shared** via a git repository or shared file system.
3. **Agent B** pulls the improvements and applies relevant ones.
4. **Agent B** runs its own nightly routine, building on Agent A's learnings.

This creates a collective improvement loop where multiple agents benefit from each other's experiences.

---

## Integration Testing

### Testing Your Integrations

After setting up integrations, verify they work correctly:

1. **Run the nightly routine in dry-run mode** — verify it reads all integration inputs correctly.
2. **Check data flow** — confirm data flows from source skills to the nightly routine and back.
3. **Verify no conflicts** — ensure two skills don't try to modify the same file simultaneously.
4. **Test rollback** — verify that rolling back a prompt mutation doesn't break integration data flows.

### Integration Health Checks

Add integration health checks to the nightly routine:

```bash
# Check that self-improving files are readable
test -r self-improving/memory.md && echo "self-improving: OK" || echo "self-improving: MISSING"

# Check that proactivity buffer is writable
test -w proactivity/memory/working-buffer.md && echo "proactivity: OK" || echo "proactivity: MISSING"

# Check that lessons directory exists
test -d lessons/ && echo "lessons: OK" || echo "lessons: MISSING"
```

---

## Summary

Integration is what makes the Self-Smarter-Everyday skill more than the sum of its parts. By connecting with the self-improving skill, proactivity skill, AAR loop, and external systems, the nightly routine creates a compound improvement effect. Each integration point is designed to be loose-coupled — the skills can operate independently but become more powerful together. Start with the core nightly routine, then add integrations one at a time, testing each before moving to the next. The goal is a cohesive self-improvement ecosystem that grows smarter every day.
