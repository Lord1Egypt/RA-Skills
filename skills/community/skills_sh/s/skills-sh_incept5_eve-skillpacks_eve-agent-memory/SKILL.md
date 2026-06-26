---
name: eve-agent-memory
description: Choose and combine Eve storage primitives to give agents persistent memory — short-term workspace, medium-term attachments and threads, long-term org docs and filesystem. Use when designing how agents remember, retrieve, and share knowledge.
---

# Eve Agent Memory

Agents on Eve Horizon have no built-in "memory" primitive, but the platform provides storage systems at every timescale. This skill teaches how to compose them into coherent memory for agents that learn, remember, and share.

## The Memory Problem

Every agent starts cold. Without deliberate memory design, agents:

- Re-discover the same facts on every job.
- Lose context when jobs end.
- Cannot share learned knowledge with sibling agents.
- Accumulate stale information with no expiry.

Solve this by mapping **what to remember** to **where to store it**, using the right primitive for each timescale.

## Storage Primitives by Timescale

### Short-Term (within a job)

**Workspace files** — the git repo checkout available during job execution.

```bash
# Workspace is at $EVE_REPO_PATH
# Write working state to .eve/ (gitignored by convention)
echo '{"findings": [...]}' > .eve/agent-scratch.json

# Workspace modes control sharing:
#   job       — fresh checkout per job (default)
#   session   — shared across jobs in a session
#   isolated  — no git state, pure scratch
eve job create --workspace-mode session --workspace-key "auth-sprint"
```

Use for: scratch notes, intermediate results, coordination inbox files. Ephemeral by design — workspace state does not survive the job unless committed to git or saved elsewhere.

**Coordination inbox** — `.eve/coordination-inbox.md` is auto-generated from coordination thread messages at job start. Read it for sibling status without API calls.

**Agent KV Store** — lightweight operational state with optional TTL. Use for: feature flags, rate counters, agent state machines, deduplication keys. Namespace-partitioned.

```bash
# Set a KV value with TTL
eve kv set --org $ORG_ID --agent $AGENT_SLUG --key "pr-123-status" --value '{"phase":"review"}' --namespace workflow --ttl 86400

# Get a KV value
eve kv get --org $ORG_ID --agent $AGENT_SLUG --key "pr-123-status" --namespace workflow

# List keys in a namespace
eve kv list --org $ORG_ID --agent $AGENT_SLUG --namespace workflow

# Batch get multiple keys
eve kv mget --org $ORG_ID --agent $AGENT_SLUG --keys "pr-123-status,pr-456-status" --namespace workflow

# Delete a key
eve kv delete --org $ORG_ID --agent $AGENT_SLUG --key "pr-123-status" --namespace workflow
```

### Medium-Term (across jobs within a project)

**Job attachments** — named key-value pairs attached to any job. Survive after job completion.

```bash
# Store findings
eve job attach $EVE_JOB_ID --name findings.json --content '{"patterns": [...]}'
eve job attach $EVE_JOB_ID --name summary.md --file ./analysis-summary.md

# Retrieve from any job (including parent/child)
eve job attachment $PARENT_JOB_ID findings.json --out ./prior-findings.json
eve job attachments $JOB_ID  # list all
```

Use for: job outputs, decision records, analysis results. Attached to a specific job, so retrievable by job ID. Good for passing structured data between parent and child jobs.

**Threads** — message sequences with continuity across sessions.

```bash
# Project threads maintain chat context
eve thread messages $THREAD_ID --since 1h

# Coordination threads connect parent/child agents
eve thread post $COORD_THREAD_ID --body '{"kind":"update","body":"Found 3 auth issues"}'
eve thread follow $COORD_THREAD_ID  # poll for sibling updates
```

Use for: inter-agent communication, rolling context, coordination. Thread summaries provide compressed history. Coordination threads (`coord:job:{parent_job_id}`) are auto-created for team dispatches.

**Thread Distillation** — convert thread conversations into memory docs or org docs. Use for: preserving valuable discussion outcomes as searchable knowledge.

```bash
eve thread distill $THREAD_ID --org $ORG_ID --agent reviewer --category learnings --key "auth-discussion-findings"
```

**Resource refs** — versioned pointers to org documents, mounted into job workspaces.

```bash
eve job create \
  --description "Review the approved plan" \
  --resource-refs='[{"uri":"org_docs:/pm/features/FEAT-123.md@v3","label":"Plan","mount_path":"pm/plan.md"}]'
```

Use for: pinning specific document versions as job inputs. The referenced document is hydrated into the workspace at the specified mount path. Events track hydration success/failure.

### Long-Term (across projects, persistent)

**Org Document Store** — versioned documents scoped to the organization.

```bash
# Store knowledge
eve docs write --org $ORG_ID --path /agents/learnings/auth-patterns.md --file ./auth-patterns.md

# Retrieve
eve docs read --org $ORG_ID --path /agents/learnings/auth-patterns.md
eve docs list --org $ORG_ID --prefix /agents/learnings/

# Search
eve docs search --org $ORG_ID --query "authentication retry"
```

Use for: curated knowledge, decision logs, learned patterns. Versioned (every update creates a new version). Emits `system.doc.created/updated/deleted` events on the event spine. Best for knowledge that is reviewed, refined, and shared.

**Agent Memory Namespaces** — curated knowledge stored as org docs with agent-scoped path conventions. Categories: `learnings`, `decisions`, `runbooks`, `context`, `conventions`. Supports confidence scores, tags, review dates, and expiration. Use for: accumulated expertise, decision logs, operational runbooks.

```bash
# Store a memory entry
eve memory set --org $ORG_ID --agent reviewer --category learnings --key "auth-retry-patterns" \
  --content "Always use exponential backoff..." --confidence 0.9 --tags "auth,reliability" --review-in 30d

# Get a memory entry
eve memory get --org $ORG_ID --agent reviewer --key "auth-retry-patterns" --category learnings

# List entries
eve memory list --org $ORG_ID --agent reviewer --category learnings --limit 20

# Delete an entry
eve memory delete --org $ORG_ID --agent reviewer --category learnings --key "auth-retry-patterns"

# Search across memory (all agents or specific)
eve memory search --org $ORG_ID --query "auth retry patterns" --agent reviewer --limit 10
```

Namespace convention: `/agents/{slug}/memory/{category}/{key}.md` or `/agents/shared/memory/...`

**Org Filesystem** — shared per-org file storage mounted at `.org/` in agent workspaces and synced to local machines.

```bash
# Agents access .org/ directly in their workspace (all execution paths)
ls .org/                                    # browse org files
cat .org/shared/runbook.md                  # read shared knowledge
echo "new finding" >> .org/agents/reviewer/notes.md  # write agent-scoped files

# Developers sync to local machines
eve fs sync init --org $ORG_ID --local ~/Eve/acme --mode two-way
eve fs sync status --org $ORG_ID
eve fs sync logs --org $ORG_ID --follow
```

Use for: large knowledge bases, design assets, documentation trees. Agents see `.org/` in their workspace regardless of execution path (agent-runtime or worker). Markdown-first defaults. Event-driven notifications (`file.created/updated/deleted`). Best for knowledge that lives as a file tree and benefits from both agent and human editing.

**Skills and Skillpacks** — distilled patterns packaged for reuse.

Use for: encoding recurring workflows and hard-won knowledge as reusable instructions. When an agent discovers a pattern worth preserving, distill it into a skill (see `eve-skill-distillation`). Skills are the highest-fidelity form of long-term memory — they don't just store information, they teach how to use it.

**Managed databases** — environment-scoped Postgres instances with agent-accessible SQL.

```bash
eve db sql --env $ENV --sql "SELECT key, value FROM agent_memory WHERE agent_id = 'reviewer' AND expires_at > NOW()"
eve db sql --env $ENV --sql "INSERT INTO agent_memory (agent_id, key, value) VALUES ('reviewer', 'last_review', '...')" --write
```

Use for: structured queries, relationship data, anything that benefits from SQL. Requires schema setup via migrations. Use `eve db rls init --with-groups` for access-controlled agent memory tables.

### Shared (coordination across agents)

**Org threads** — org-scoped message sequences for cross-project coordination.

```bash
eve thread list --org $ORG_ID
eve thread post $ORG_THREAD_ID --body '{"kind":"directive","body":"All agents: use new auth pattern"}'
```

**Event spine** — pub/sub event bus for reactive workflows.

```bash
eve event emit --type=agent.memory.updated --source=app --payload '{"agent":"reviewer","key":"patterns"}'
eve event list --type agent.memory.*
```

Use for: broadcasting knowledge updates, triggering reactive workflows when memory changes.

**Unified Search** — single query across memory, docs, threads, attachments, events. Use for: finding relevant prior knowledge before starting work.

```bash
eve search --org $ORG_ID --query "auth retry patterns" --sources memory,docs,threads --limit 10 --agent reviewer
```

## Memory Patterns

### Pattern 1: Job-Scoped Scratch

The simplest pattern. Write working state to workspace files during execution. Nothing survives the job.

```
Job starts → read inputs → write .eve/scratch.json → process → complete
```

When to use: single-job tasks with no memory requirement.

### Pattern 2: Parent-Child Knowledge Passing

Pass knowledge between orchestrator and workers using attachments and threads.

```
Parent creates children with resource-refs →
Children execute, attach findings →
Parent resumes, reads child attachments →
Parent synthesizes into final output
```

```bash
# Child stores its findings
eve job attach $EVE_JOB_ID --name findings.json --content "$FINDINGS"

# Parent reads child findings on resume
for child_id in $CHILD_IDS; do
  eve job attachment $child_id findings.json --out ./child-${child_id}.json
done
```

When to use: orchestrated work where children discover information the parent needs.

### Pattern 3: Org Knowledge Base

Build persistent, searchable knowledge that survives across projects and time.

```
Agent discovers pattern →
Check if existing doc covers it (eve docs search) →
  If yes: update with new information (eve docs write)
  If no: create new document (eve docs write) →
Emit event for other agents (eve event emit)
```

Namespace convention for agent-maintained docs:

```
/agents/{agent-slug}/learnings/     — patterns and discoveries
/agents/{agent-slug}/decisions/     — decision records with rationale
/agents/{agent-slug}/runbooks/      — operational procedures
/agents/shared/                     — cross-agent shared knowledge
```

When to use: knowledge that accumulates over time and should be available to any agent in the org.

### Pattern 4: Memory-Augmented Job Start

Combine primitives to give an agent relevant context at the start of every job.

```
Job starts →
Read coordination inbox (.eve/coordination-inbox.md) →
Query org docs for relevant prior knowledge (eve docs search) →
Check parent/sibling attachments for recent findings →
Proceed with enriched context
```

```bash
# Startup sequence
cat .eve/coordination-inbox.md 2>/dev/null  # sibling context
ls .org/ 2>/dev/null                         # org filesystem (shared files)
eve docs search --org $ORG_ID --query "$JOB_DESCRIPTION_KEYWORDS"  # prior knowledge
eve job attachments $PARENT_JOB_ID  # parent context
```

When to use: any agent that benefits from remembering what happened before.

### Pattern 5: Search-Before-Write

Search existing knowledge before creating new docs.

```
eve search --org $ORG_ID --query "auth retry patterns" --sources memory,docs →
  If relevant result exists: read and update it
  If no result: create new memory doc
```

When to use: any agent that creates knowledge documents. Prevents duplication.

### Pattern 6: KV State Machine

Use KV store to track multi-step agent workflows.

```
eve kv set --org $ORG_ID --agent reviewer --namespace workflow --key "pr-123" --value '{"phase":"review","started":"..."}' --ttl 86400
```

When to use: tracking step-by-step progress in multi-phase jobs where state must survive brief interruptions but not forever.

### Pattern 7: Thread-to-Knowledge Pipeline

Distill valuable thread conversations into searchable memory.

```
eve thread distill $THREAD_ID --org $ORG_ID --agent reviewer --category learnings --key "auth-discussion-findings"
```

When to use: after a thread produces knowledge worth preserving beyond the conversation.

## Choosing the Right Primitive

| Question | Answer → Primitive |
|---|---|
| Need it only during this job? | Workspace files |
| Need lightweight state with TTL? | Agent KV Store |
| Need to pass data to parent/children? | Job attachments |
| Need rolling conversation context? | Threads |
| Need to distill a conversation into knowledge? | Thread distillation → Agent Memory |
| Need curated, categorized agent knowledge? | Agent Memory Namespaces |
| Need versioned, searchable documents? | Org Document Store |
| Need shared files across agents in the org? | Org Filesystem (`.org/` mount) |
| Need file-tree sync with local editing? | Org Filesystem (CLI sync) |
| Need app-scoped binary/object storage? | Object Store (manifest) |
| Need structured queries (SQL)? | Managed database |
| Need to encode a reusable workflow? | Skills |
| Need reactive notifications? | Event spine |
| Need to search across everything? | Unified Search |

## Access Control

Storage primitives respect Eve's access model:

- **Secrets**: scoped resolution (project → user → org → system). Never store memory in secrets.
- **Org docs**: org membership required. Use access groups for fine-grained control.
- **Database**: use RLS with group-aware policies for multi-agent isolation.
- **Threads**: project-scoped or org-scoped. Job tokens grant access to coordination threads.
- **Filesystem**: org-level permissions, with optional path ACLs via access groups.

```bash
# Check agent's effective access
eve access can --resource orgdocs:/agents/shared/ --action read
eve access memberships --org $ORG_ID
```

## Anti-Patterns

- **Storing everything in workspace files** — dies with the job. Use attachments or org docs for anything worth keeping.
- **Giant thread messages as memory** — threads are for communication, not storage. Post summaries, store details in docs.
- **No expiry strategy** — memory without lifecycle becomes noise. Date your documents, prune periodically.
- **Duplicating knowledge across primitives** — pick one source of truth per piece of knowledge. Reference it from other places, don't copy it.
- **Skipping search before writing** — always check if the knowledge already exists before creating a new document. Update beats create.

## Current Gaps and Workarounds

Some memory patterns require manual assembly today:

- **No automatic context carryover at job start** — build startup sequences manually (see Pattern 4). The platform does not auto-hydrate prior knowledge on job launch.
- **No automatic thread-to-knowledge distillation** — manual `eve thread distill` exists, but no cron or trigger-based automation yet.
- **No document lifecycle automation** — set review dates and expiration via `--review-in` and `--expires-in` flags. Use `eve docs stale` to find overdue documents. Automated cleanup is not yet available.
