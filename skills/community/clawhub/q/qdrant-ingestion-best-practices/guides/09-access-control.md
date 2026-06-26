# Guide 09 — Access Control Patterns

## Purpose

This guide defines the architectural principles and implementation patterns for access control in Qdrant-based RAG systems. It explains the separation of concerns between the data layer and the policy layer, and provides concrete patterns for enforcing permissions at retrieval time.

---

## The Fundamental Principle

> **Metadata describes what data is. It does not encode which agents or users may access it.**

Agent-to-data access mappings belong exclusively in your orchestration layer (middleware, n8n, LangGraph, custom API gateway). They must never be stored in chunk payloads.

---

## Why NOT to Store Permissions in Chunks

A common temptation is to add an `allowed_agents` field to each chunk. This is explicitly wrong for three reasons:

**1. Re-ingestion risk:** If an agent's access scope changes (e.g., a new AI agent is granted access to finance data), every affected chunk would need to be updated in the vector store. At scale this is operationally dangerous, slow, and error-prone.

**2. Privilege escalation surface:** If an LLM can influence the values of access control fields (even indirectly, through prompt injection), and those fields are authoritative for access decisions, you have a security vulnerability.

**3. Tight coupling:** Embedding access policy in the data layer creates a hard dependency between your AI agent configuration and your vector store schema, making both harder to evolve independently.

---

## The Correct Architecture: Two-Layer Separation

```
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER (middleware / n8n / LangGraph)             │
│                                                                 │
│  Stores: agent-to-data access mappings                         │
│  - Which (user_id, agent_id) pairs can access which scopes     │
│  - Which collections each agent may query                      │
│  - Which sensitivity tiers are permitted per role              │
│                                                                 │
│  Responsibilities:                                              │
│  1. Validate agent identity                                     │
│  2. Look up user identity from session/token                   │
│  3. Resolve permission scope for (user, agent) pair            │
│  4. Build Qdrant query filters from resolved scope             │
│  5. Execute query — agent cannot modify filters                │
│  6. Return results — agent sees only permitted content         │
└────────────────────────────┬────────────────────────────────────┘
                             │ Builds filter from scope
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  VECTOR STORE (Qdrant)                                          │
│                                                                 │
│  Stores: data characteristics only                             │
│  - sensitivity                                                  │
│  - team_ids                                                     │
│  - allowed_groups                                              │
│  - data_scope_tags                                             │
│  - org_id / workspace_id                                       │
│                                                                 │
│  Does NOT store:                                                │
│  - allowed_agents                                              │
│  - permitted_agents                                            │
│  - agent-level permission lists                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Permission Resolution Flow

```
1. User sends message → Orchestration layer receives it
2. Orchestration generates request_id, maps to user_id in session store
3. Request (with request_id, agent_id, query) sent to AI agent
4. AI agent calls retrieval tool → passes request_id, agent_id, query text only
5. Orchestration layer:
   a. Looks up user_id from session store using request_id
   b. Validates agent_id is permitted for this user
   c. Resolves permission scope for (user_id, agent_id):
      - permitted sensitivity tiers
      - permitted team_ids
      - permitted data_scope_tags
      - permitted collections
      - org_id / workspace_id
   d. Builds Qdrant filter from resolved scope
   e. Executes Qdrant query with filters as hard constraints
6. Results returned — AI agent never sees out-of-scope content
```

---

## Permission Scope Object

Your orchestration layer should resolve a permission scope that looks like this:

```python
# Example permission scope for a sales agent user
permission_scope = {
    "org_id": "org-456",
    "workspace_id": "ws-123",
    "permitted_collections": ["company_memory"],  # No access to restricted_memory
    "permitted_sensitivity": ["public", "internal"],
    "team_ids": ["team_sales_a", "team_sales_b"],  # Team-restricted
    "allowed_groups": ["g_all_staff", "g_sales"],
    "data_scope_tags": ["sales", "region:emea"],   # Only sales/EMEA content
}

# Example permission scope for an executive user
permission_scope_exec = {
    "org_id": "org-456",
    "workspace_id": "ws-123",
    "permitted_collections": ["company_memory", "restricted_memory"],
    "permitted_sensitivity": ["public", "internal", "restricted"],
    "team_ids": None,       # No team restriction — sees all team content
    "allowed_groups": None, # No group restriction
    "data_scope_tags": None, # No scope restriction — sees all domains
}
```

---

## Tiered Authorization Model

Implement access control as layers, where each layer narrows the scope:

| Layer | Enforced By | Mechanism |
|---|---|---|
| **Layer 1: User → Agent** | Orchestration layer | Agent Access Registry: is this agent_id permitted for this user_id? |
| **Layer 2: Agent → Collection** | Orchestration layer | Which collections may this (user, agent) pair query? |
| **Layer 3: Agent → Data** | Qdrant payload filters | sensitivity, team_ids, data_scope_tags, allowed_groups |
| **Layer 4: Composite** | Intersection of all above | Most restrictive rule wins |

---

## What Ingestion Pipelines Must NOT Store

The following fields are explicitly prohibited in chunk payloads:

```python
# PROHIBITED — never add these to a chunk payload
PROHIBITED_FIELDS = [
    "allowed_agents",
    "permitted_agents",
    "agent_access_list",
    "allowed_ai_agents",
    "agent_ids",
    # Any field that lists which AI agents may access this chunk
]
```

If you find these fields in an existing payload schema, they must be removed and replaced with the correct pattern (`data_scope_tags` + orchestration-layer mapping).

---

## Agent Access Changes Do Not Require Re-Ingestion

Because access mappings live in the orchestration layer (not in chunk metadata), access changes are instant and zero-cost to the vector store:

| Event | Required Action |
|---|---|
| New agent created and granted access to sales data | Update orchestration layer config: add `data_scope_tags: ["sales"]` to new agent's permitted scope. **No re-ingestion.** |
| Existing agent's access expanded to include finance | Update orchestration config. **No re-ingestion.** |
| Agent's access revoked | Update orchestration config. **No re-ingestion.** |
| Document reclassified to higher sensitivity tier | Re-ingest + migrate to correct collection. (See `03-data-classification.md`) |

The last row is the important exception: **sensitivity changes do require re-ingestion** because sensitivity determines collection placement, which is a hard boundary.

---

## Metadata Fields Used as Filter Primitives

These fields in the chunk payload are the filter inputs consumed by the orchestration layer. They must be accurately populated at ingest time and indexed in Qdrant:

| Field | Role | Ingest Requirement |
|---|---|---|
| `sensitivity` | Primary collection gate | Classified at ingest per Section 3 of `03-data-classification.md`. Never deferred. |
| `team_ids` | Team-scoped filter | Populated from source system wherever available. Never fabricated. |
| `allowed_groups` | Group-level filter | Populated from source system permissions at ingest. |
| `data_scope_tags` | Semantic scope filter | Populated using the controlled taxonomy in `02-metadata-schema.md`. |
| `org_id` / `workspace_id` | Tenant isolation | Always populated. Never omitted. |

---

## Audit Trail

Every retrieval request that passes through access control should produce an audit record. Your ingestion pipeline supports this by ensuring filter primitive fields are accurately populated — they are recorded in the audit log alongside each request.

Minimum audit record per retrieval request:

```python
audit_record = {
    "request_id": "...",          # Trace ID for this request
    "user_id": "...",             # Resolved from session store
    "agent_id": "...",            # Validated against Agent Access Registry
    "timestamp": "...",           # ISO 8601 UTC
    "permission_scope_applied": { # The resolved scope that was enforced
        "collections": ["company_memory"],
        "sensitivity": ["public", "internal"],
        "team_ids": ["team_sales_a"],
        "data_scope_tags": ["sales"],
    },
    "query_text": "...",          # Query submitted by the agent
    "doc_ids_returned": ["..."],  # Which chunks were returned
    "chunks_count": 7,
}
```

Given any `request_id`, operators must be able to reconstruct: who asked, which agent was acting, what filters were applied, and which chunks were returned.

---

## Security Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | Correct Approach |
|---|---|---|
| Storing `allowed_agents` in chunk payload | Re-ingestion required on every access change; privilege escalation risk | Store agent→scope mappings in orchestration layer config |
| Filtering access post-retrieval | Content briefly retrieved before being discarded; reduces result quality | Apply filters inside Qdrant query |
| Using `model_inferred` sensitivity as sole basis for access decisions | Variable confidence; untestable; may misclassify sensitive content | Require `source_asserted` or `system_derived` classification; log and review model-inferred |
| Skipping `data_scope_tags` when source context is known | Chunks become broadly accessible by default | Always populate scope tags when organizational context is determinable |
| Creating one collection per agent | Exhausts cluster resources; forces re-ingestion on access changes | Use scope tags + orchestration-layer filtering on a shared collection |
