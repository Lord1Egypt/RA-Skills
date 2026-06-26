# Agent Teams Enhancement Spec

## Goal
Enhance the existing `team-tasks` skill at `/home/ubuntu/clawd/skills/team-tasks/` to support two new modes that replicate Claude Code's Agent Teams capabilities:

1. **Shared workspace mode** — multiple agents work on the same codebase
2. **Debate mode** — send the same question to N agents, collect responses, cross-evaluate

## Current State
- `scripts/task_manager.py` already supports `linear` and `dag` modes
- Data files in `/home/ubuntu/clawd/data/team-tasks/<project>.json`
- Agents are dispatched via OpenClaw's `sessions_send` and results tracked in JSON

## Requirements

### 1. New mode: `debate`

Add a new mode `--mode debate` to `task_manager.py init`.

**Debate workflow:**
1. `init <project> --mode debate -g "question"` — creates project with a question/topic
2. `add-debater <project> <agent-id> [--role "perspective"]` — add agents as debaters, each with an optional role/perspective
3. `round <project> start` — generates dispatch info for round 1 (each debater gets the question + their role)
4. After collecting responses: `round <project> collect <agent-id> "response"` — save each debater's response
5. `round <project> cross-review` — generates cross-review prompts (each debater reviews others' responses)
6. After cross-review: `round <project> collect <agent-id> "review"` — save reviews
7. `round <project> synthesize` — outputs all positions + reviews for final synthesis
8. `status <project>` — shows debate state, rounds, and positions

**Data structure for debate mode:**
```json
{
  "project": "security-review",
  "mode": "debate",
  "goal": "Review security of auth module",
  "debaters": {
    "agent-1": { "role": "security expert", "responses": [] },
    "agent-2": { "role": "performance analyst", "responses": [] }
  },
  "rounds": [
    {
      "type": "initial",
      "status": "done",
      "responses": { "agent-1": "...", "agent-2": "..." }
    },
    {
      "type": "cross-review", 
      "status": "in-progress",
      "responses": {}
    }
  ],
  "currentRound": 1,
  "status": "active"
}
```

### 2. Shared workspace tracking

Add `--workspace <path>` to `init` for all modes. This records the shared workspace path in the project JSON so all agents work in the same directory.

For `dag` and `linear` modes, add the workspace path to `ready`/`next` output so the dispatcher knows where to point agents.

### 3. Cross-review prompt generation

The `round <project> cross-review` command should output structured prompts for each debater:

```
Agent: agent-1 (security expert)
Your previous response: <agent-1's response>

Other debaters' responses:
- agent-2 (performance analyst): <agent-2's response>
- agent-3 (testing specialist): <agent-3's response>

Task: Review the other responses. Do you agree or disagree? What did they miss? Update your position if needed.
```

## Constraints
- Keep backward compatibility with existing `linear` and `dag` modes
- Same CLI pattern as existing commands
- Same data directory: `/home/ubuntu/clawd/data/team-tasks/`
- Python 3.12+, no external dependencies beyond stdlib
- Keep code clean and readable — this will be used by AI agents

## Files to modify
- `/home/ubuntu/clawd/skills/team-tasks/scripts/task_manager.py` — add debate mode commands

## Testing
After implementing, verify with this test scenario:
```bash
TM="python3 /home/ubuntu/clawd/skills/team-tasks/scripts/task_manager.py"

# Create debate
$TM init security-debate --mode debate -g "Review the auth module at /tmp/auth.py for security vulnerabilities"

# Add 3 debaters
$TM add-debater security-debate code-agent --role "security expert focused on injection attacks"
$TM add-debater security-debate test-agent --role "QA engineer focused on edge cases"
$TM add-debater security-debate monitor-bot --role "ops engineer focused on deployment risks"

# Start round 1
$TM round security-debate start

# Collect responses
$TM round security-debate collect code-agent "Found SQL injection in login()"
$TM round security-debate collect test-agent "Missing input validation on email field"
$TM round security-debate collect monitor-bot "No rate limiting on auth endpoints"

# Generate cross-review prompts
$TM round security-debate cross-review

# Collect cross-reviews
$TM round security-debate collect code-agent "Agree with test-agent on validation. monitor-bot's rate limiting is critical."
$TM round security-debate collect test-agent "code-agent's SQL injection is most severe. Adding rate limit tests."
$TM round security-debate collect monitor-bot "Both findings are valid. Recommending WAF as additional layer."

# Synthesize
$TM round security-debate synthesize

# Check status throughout
$TM status security-debate
```
