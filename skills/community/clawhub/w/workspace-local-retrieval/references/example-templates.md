# Example Templates

Use these as sanitized starting points. Replace placeholders before use.

## `corpora.json`

```json
{
  "version": 1,
  "global": {
    "workspaceRoot": "/ABSOLUTE/PATH/TO/WORKSPACE",
    "defaultDbPath": "/ABSOLUTE/PATH/TO/WORKSPACE/retrieval/indexes/workspace_retrieval.sqlite",
    "includeExtensions": [".md", ".txt"],
    "excludeGlobs": [
      "memory/**",
      "my_note/**",
      "my_profile/**",
      ".openclaw/**",
      ".clawhub/**",
      ".git/**",
      "out/**",
      "tmp/**",
      "node_modules/**",
      "retrieval/indexes/**"
    ],
    "chunking": {
      "maxChars": 2800,
      "softBreakChars": 1800,
      "overlapChars": 300
    }
  },
  "corpora": [
    {
      "id": "workspace-core",
      "description": "Core workspace docs and shared rules.",
      "include": [
        "AGENTS.md",
        "USER.md",
        "TOOLS.md",
        "SOUL.md",
        "skills/**",
        "agents/**"
      ]
    },
    {
      "id": "workspace-specialist",
      "description": "Specialist domain docs.",
      "include": [
        "specialist/**"
      ]
    }
  ]
}
```

## `agent_corpora.json`

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

## `agent_memory.json`

```json
{
  "version": 1,
  "agents": {
    "main": {
      "memoryMode": "broad-coordination",
      "memoryRoots": ["MEMORY.md", "memory/"],
      "notes": "Main coordinator can use broad continuity."
    },
    "specialist-agent": {
      "memoryMode": "domain-scoped",
      "memoryRoots": ["specialist/data/", "specialist-guide.md"],
      "notes": "Specialist stays inside domain memory by default."
    }
  }
}
```
