# Health Checks

## Startup Check (obrigatório)

Executar `bash scripts/guardian-startup.sh` no primeiro heartbeat.

### O que valida:
1. **Diretórios:** memory/, memory/topics/
2. **Arquivos:** MEMORY.md, memory/YYYY-MM-DD.md (diário)
3. **Config:** openclaw.json é JSON válido
4. **URLs:** Todos os providers usam HTTPS
5. **API Keys:** Todos os providers têm apiKey configurada
6. **Permissões:** Arquivos .md são legíveis

### Resultado:
- Exit code 0 = tudo OK
- Exit code 1 = problemas encontrados (ver output)

## Heartbeat Check (periódico)

A cada heartbeat, validação leve:
- Gateway respondendo? (`curl -sf http://127.0.0.1:18789/health`)
- Último LLM request teve sucesso? (verificar logs)
- Disco não está cheio? (`df -h /data`)

## Métricas para monitoramento:
- **Uptime do Gateway:** tempo desde último restart
- **Erros LLM nas últimas 24h:** count de failures
- **Uso de disco:** % do volume /data
- **Sessões ativas:** count via sessions.list
- **Tokens consumidos:** total in+out últimas 24h
