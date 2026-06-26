---
name: zanna-aperta
description: MCP Bridge completo per OpenClaw con 45 tool per agenti, workspace, progetti, cron, browser, canvas, nodes, messaging, gateway, Ollama e ClawX
---

# Zanna Aperta 🐺

MCP Bridge che collega OpenFang (o qualsiasi client MCP) a tutti i tool OpenClaw nativi + ClawX.

## Tool Disponibili (45)

**Agenti (3):** agent_find, agent_update, agent_delete

**Workspace (5):** workspace_create, workspace_list, workspace_find, workspace_update, workspace_delete

**Progetti (5):** project_create, project_list, project_find, project_update, project_delete

**Cron (4):** cron_list, cron_add, cron_remove, cron_run

**Browser (4):** browser_open, browser_snapshot, browser_click, browser_type

**Canvas (3):** canvas_present, canvas_hide, canvas_eval

**Nodes (3):** nodes_list, nodes_notify, nodes_camera_snap

**Messaging (2):** message_send, message_poll

**Gateway (2):** gateway_status, gateway_restart

**Exec (2):** exec_docker, exec_git

**Ollama (4):** ollama_list, ollama_chat, ollama_generate, ollama_pull

**ClawX (4):** clawx_start, clawx_stop, clawx_status, clawx_restart

## Configurazione

Aggiungi a `~/.openfang/settings.json`:

```json
{
  "mcpServers": {
    "zanna-aperta": {
      "command": "python3",
      "args": ["~/.openclaw/skills/zanna-aperta/zanna-aperta.py"],
      "env": {
        "OPENCLAW_WORKSPACE": "~/.openclaw/workspace",
        "OPENCLAW_BIN": "openclaw"
      }
    }
  }
}
```

## Requisiti

- OpenClaw installato
- Python 3.8+
- Ollama in esecuzione su localhost:11434 (opzionale)
- ClawX in ~/.openclaw/workspace/ClawX (opzionale)

## Autore

Raid AI - 2026
