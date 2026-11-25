# chat-service.md — Chat agente↔usuário através do túnel

Serviço `chat` (porta 8000): servidor HTTP puro em Python
(`tunnel/chat/chat_server.py`), sem dependências, com histórico persistente
em `tunnel/chat/messages.jsonl`. Objetivo: usuário conversa do CELULAR via
URL do túnel; agente lê e responde via localhost. Teste célula-a-célula
ainda PENDENTE (objetivo registrado em STATUS-ATUAL.md).

## Procedimento completo do teste (objetivo pendente)

```bash
# 1. Ligar (por ordem do usuário):
bash /home/z/my-project/tunnel/ctl/tunnelctl say "liga o chat"
#    → aguarde URL(...) validada

# 2. Usuário abre a URL no celular → a página pede um nome → envia mensagens.

# 3. Agente lê as mensagens novas (micro-comando):
curl -s "http://127.0.0.1:8000/messages?since=N"
#    N = último id visto; retorna JSON com mensagens após N.

# 4. Agente responde:
curl -s -X POST http://127.0.0.1:8000/send \
  -H 'Content-Type: application/json' \
  -d '{"user":"Agente","text":"sua resposta"}'

# 5. Saúde do serviço:
curl -s http://127.0.0.1:8000/health   # contém "ok": true (marcador do monitor)
```

## API

| Endpoint | Método | Entrada | Saída |
|---|---|---|---|
| `/` | GET | — | página de chat (pede nome, envia/recebe) |
| `/health` | GET | — | `{"ok": true, ...}` — marcador de validação |
| `/messages` | GET | `?since=N` (id) | mensagens com id > N (JSON) |
| `/send` | POST | JSON `{"user":"nome","text":"..."}` | mensagem gravada + eco |

## Protocolo de conversa para o agente

1. **Polling**: a cada turno em que o usuário pode ter escrito, faça
   `GET /messages?since=<último id>`. Comece com `since=0`.
2. **Identidade**: responda como `"user":"Agente"`; o nome do usuário vem
   do prompt inicial da página.
3. **Persistência**: `tunnel/chat/messages.jsonl` — uma linha JSON por
   mensagem; sobrevive a reinícios (filesystem persiste, processos não).
4. **Latência**: mensagem do usuário só chega ao agente quando o agente
   roda um turno — avise o usuário que a resposta não é instantânea.
5. **Segurança**: o chat serve apenas a página própria; NUNCA aponte o
   serviço para pastas arbitrárias.

## Integração com outras skills

- **LLM** (z-ai-web-dev-sdk): o texto recebido via `/messages` pode ser
  processado pela skill LLM e a resposta devolvida via `/send` — chatbot
  completo acessível pelo celular sem WebSocket e sem servidor próprio.
- **ASR/TTS**: transcript de áudio ou texto falado pode trafegar pelo mesmo
  canal JSON.
- **fullstack-dev**: para app Next.js com chat embutido, prefira expor o
  próprio Next (porta 3000) e usar o chat-service como referência de API.

## Estado do arquivo de mensagens

```bash
wc -l /home/z/my-project/tunnel/chat/messages.jsonl   # quantas mensagens
tail -3 /home/z/my-project/tunnel/chat/messages.jsonl # últimas (raw)
```
