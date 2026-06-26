# Configurability

A shareable skill should not depend on project-specific agent names like `gorilla`, `panda`, or `sheep`.

## Make these configurable

### 1. Agent list

The agent list must be variable-length. Do not assume a fixed team shape like coordinator + ops + writer. Some users may have one assistant, some may have three, some may have many specialized agents.

Allow a list of entries such as:

```json
[
  {
    "agentId": "main",
    "displayName": "主助理",
    "description": "综合处理、调度、总结",
    "aliases": ["主助理", "总助理"]
  },
  {
    "agentId": "ops",
    "displayName": "技术助手",
    "description": "维护、配置、诊断",
    "aliases": ["技术", "运维"]
  }
]
```

### 2. Default agent

Do not assume the default agent is always `main` unless the user's environment already uses that convention.

### 3. Timeout

Make inactivity fallback configurable.

### 4. Command aliases

Do not bake project-private vocabulary into the public skill without a config layer.

## Public-skill guidance

When preparing a public skill:

- use neutral placeholder names like `{agent}` instead of private names
- do not imply a fixed number of agents unless the user explicitly wants an opinionated preset
- keep examples realistic but obviously customizable
- document which parts must be adapted before deployment

## Migration guidance

If the current implementation is project-specific:

1. identify hard-coded display names
2. identify hard-coded command aliases
3. identify any hidden assumption about fixed agent count
4. move all of the above to configuration
5. update all user-facing examples to generic placeholders
6. validate again with at least two different agent maps
