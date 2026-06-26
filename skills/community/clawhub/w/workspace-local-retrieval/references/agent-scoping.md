# Agent Scoping

Use this file when mapping corpora and memory roots to agents.

## Principle

Use deny-by-default. Add access intentionally.

## Retrieval allowlists

A minimal pattern:

```json
{
  "version": 1,
  "defaultPolicy": {
    "mode": "deny-by-default",
    "allowedCorpora": []
  },
  "agents": {
    "main": {
      "allowedCorpora": ["workspace-core"]
    },
    "specialist-agent": {
      "allowedCorpora": ["workspace-specialist"]
    }
  }
}
```

## Memory boundaries

Do not assume retrieval scope and memory scope are the same thing.

Example:
- a coordinator may need broad workspace retrieval but narrow personal memory
- a therapist-like agent may need highly isolated memory and highly isolated retrieval
- a health agent may need health data but not the user's general long-term memory

A minimal memory-boundary pattern:

```json
{
  "version": 1,
  "agents": {
    "main": {
      "memoryMode": "broad-coordination",
      "memoryRoots": ["MEMORY.md", "memory/"]
    },
    "specialist-agent": {
      "memoryMode": "domain-scoped",
      "memoryRoots": ["specialist/data/", "specialist-guide.md"]
    }
  }
}
```

## Design questions

Before granting access, answer:
- Does this agent need broad recall or only domain recall?
- Is the corpus reusable knowledge or user-private memory?
- Would an accidental quote from this corpus be acceptable in another chat?
- Can the same outcome be achieved with a smaller corpus?

## Smell checks

Revisit the design if:
- most agents can see most corpora
- one corpus exists only because boundary design was skipped
- an agent requires many unrelated corpora to do routine work
- private notes are included because filtering them later seems easier
