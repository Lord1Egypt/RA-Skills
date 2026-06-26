# Erros Comuns e Soluções

## LLM Request Rejected: Only HTTPS URLs are supported

**Causa:** OpenClaw 2026.3.x adicionou validação que rejeita URLs HTTP.
**Onde:** `models.providers.*.baseUrl` no openclaw.json
**Fix:** Trocar `http://` por `https://` na baseUrl do provider.

```bash
# Verificar
grep -i "http://" /data/.openclaw/openclaw.json

# Corrigir (exemplo)
sed -i 's|http://|https://|g' /data/.openclaw/openclaw.json
openclaw gateway restart
```

## Edit: in ~/.openclaw/workspace/FILE.md failed

**Causa:** O agente tenta editar um arquivo que não existe.
**Fix:** O agente deve usar Write (criar) antes de Edit (modificar).
**Prevenção:** O guardian-startup.sh cria MEMORY.md e outros essenciais.

## Gateway zombie (process defunct)

**Causa:** Gateway crashou mas PID 1 (entrypoint) continua vivo.
**Fix:** Liveness probe com `curl -sf http://127.0.0.1:18789/health`
**Prevenção:** Já implementado via K8s exec-based liveness probe.

## Telegram config perdida após restart

**Causa:** Canal configurado em runtime (via chat) não persiste no openclaw.json.
**Fix:** Configurar canal via `openclaw channels add telegram --bot-token TOKEN`
**Prevenção:** Injetar config de canais no provisioning pipeline.

## Content blocks raw no Telegram ([{"type":"text","text":"..."}])

**Causa:** OpenClaw não converte content blocks (array) pra string antes de enviar.
**Versão afetada:** OpenClaw 2026.3.12
**Fix:** Pinnar versão estável ou aguardar fix upstream.

## Token expirado / 401 Unauthorized

**Causa:** API key do provider expirou ou foi revogada.
**Fix:** Atualizar apiKey no openclaw.json e reiniciar gateway.
