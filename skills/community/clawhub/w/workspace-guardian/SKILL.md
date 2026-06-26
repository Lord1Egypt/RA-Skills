---
name: workspace-guardian
description: >
  Auto-healing e proteção para workspaces OpenClaw. Valida e corrige problemas comuns
  automaticamente no startup e durante a execução. Usar quando: (1) Workspace novo precisa
  de setup inicial (criar MEMORY.md, memory/, etc), (2) Agente falha com erros de LLM
  (retry/fallback automático), (3) Arquivos essenciais corrompidos ou ausentes,
  (4) Config openclaw.json precisa de validação, (5) Health check periódico do agente.
  Instalar em todo workspace OpenClaw para garantir estabilidade e reduzir churn de clientes.
---

# Workspace Guardian

Skill de auto-healing para workspaces OpenClaw. Garante que o workspace está saudável e funcional.

## Quando rodar

Esta skill é executada automaticamente:
1. **No startup** — via HEARTBEAT.md (primeira execução)
2. **Periodicamente** — a cada heartbeat, validação leve
3. **Sob demanda** — quando o agente detecta erros recorrentes

## Startup: Validação e Setup

No primeiro heartbeat após iniciar, executar o script de validação:

```bash
bash scripts/guardian-startup.sh
```

O script valida e corrige:
- ✅ `MEMORY.md` existe (cria vazio se não)
- ✅ `memory/` diretório existe
- ✅ `memory/topics/` diretório existe
- ✅ Permissões corretas nos arquivos
- ✅ `openclaw.json` válido (JSON parseable)

## Tratamento de Erros LLM

Quando receber erros do tipo:
- `"Only HTTPS URLs are supported"` → Verificar e corrigir URLs no config
- `"Edit failed"` → Arquivo não existe, criar primeiro com Write
- `"LLM request rejected"` → Verificar apiKey e baseUrl no openclaw.json
- `timeout` → Retry com backoff exponencial

### Procedimento de auto-fix:

1. Ler `openclaw.json`
2. Validar que todas as URLs usam HTTPS
3. Validar que apiKey está presente e não vazia
4. Se encontrar problema: corrigir e reiniciar gateway

## Validação de Config

Verificar no `openclaw.json`:
- `models.providers.*.baseUrl` → deve começar com `https://`
- `models.providers.*.apiKey` → deve existir e não estar vazia
- `models.providers.*.api` → deve ser `openai-completions` ou `anthropic`
- `agents.list` → deve ter pelo menos 1 agente

## Referências

- Ver `references/common-errors.md` para lista de erros conhecidos e soluções
- Ver `references/health-checks.md` para detalhes dos health checks
