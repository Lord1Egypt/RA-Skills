---
name: quick-tunnel
metadata:
  author: "Z.AI (built in-project, 2026-10-23/24, reforma v2 F1-F5)"
  version: "2.0.0"
  language: pt-BR
description: >
  Quick Tunnel skill — expõe serviços locais do sandbox na internet via
  Cloudflare Quick Tunnel (sem conta, sem login, URL aleatória temporária),
  com arquitetura v2 de agentes (executor/monitor/intérprete-decisor-
  orquestrador), comando único `tunnelctl`, intérprete de frases em português
  (`say`), watchdog auto-curativo, autostart de boot, ressurreição em 1 comando
  (revive), serviço de chat agente↔usuário através do túnel e pipeline de APK.
  Use quando o usuário pedir: "liga o túnel", "expõe a porta X", "URL pública",
  "coloca na internet", "tunnel", "expose port", "public URL", "trycloudflare",
  "quick tunnel", "cloudflared", "liga o chat", "status dos túneis",
  "desliga/fecha/apaga túnel", "revive o túnel", ou qualquer desejo de acessar
  de fora (celular/outro PC) algo rodando no sandbox. NÃO usar para: túneis
  nomeados com conta Cloudflare, ngrok/serveo/localtunnel, nem para expor algo
  sem pedido explícito do usuário (regra de ouro: só o USUÁRIO liga túneis).
---

# Quick Tunnel — exposição pública sem conta (Cloudflare Quick Tunnel)

Sistema v2 (reforma F1–F5, todos os testes PASSARAM). Um único comando na raiz
`ctl/`, agentes com papéis exclusivos, estado em arquivo, URL só vale com
validação real na borda. Este arquivo é o ponto de entrada; os detalhes estão
em `references/` — leia somente a referência relevante.

## Regras de ouro (memorize antes de qualquer comando)

1. **Só o USUÁRIO liga túnel.** O agente NUNCA inicia exposição por conta
   própria, nem "oferece" túnel ao término de outra tarefa. Liga apenas por
   ordem explícita do usuário no chat ("liga o demo", "expõe a porta 3000").
2. **Comando único**: tudo passa por `bash /home/z/my-project/tunnel/ctl/tunnelctl <cmd>`.
   Nada inicia/mata processo fora dele (o `executor` é o único que toca em PIDs).
3. **NUNCA `pkill`/`kill` manual.** NUNCA decida ordem de operações por conta.
4. **URL só é verdadeira com validação do monitor**: HTTP 200 na borda +
   marcador de conteúdo real. `https://api.trycloudflare.com` é FALSA — banida.
5. **Agente de IA fala português com `say`**: `tunnelctl say "liga o chat"`.
   Frase ambígua → o sistema devolve PERGUNTA; nunca start por padrão.
6. **Segurança de conteúdo**: proibido servir a raiz do projeto, `/home/z`,
   ou qualquer pasta com `.env`. Só o que está no `ctl/config.txt`.

## Como invocar neste ambiente

```bash
T=/home/z/my-project/tunnel/ctl/tunnelctl

bash $T start 3000              # liga pelo PORTA (resolve nome do config)
bash $T start 3000 demo         # liga com nome explícito
bash $T status                  # verdade: nome|porta|estado|pid|url
bash $T say "liga o chat"       # intérprete→decisor→orquestrador (agente usa ESTE)
bash $T say "status"            # status por frase
bash $T stop chat               # fecha 1 (marca off, mata por pidfile)
bash $T stop all --except demo  # fecha todos menos demo
bash $T delete dummy1           # apaga entrada + artefatos
bash $T delete all              # reset de fábrica (run/ e logs/ limpos)
bash $T autostart               # religa APENAS entradas on (hook do .bashrc)
bash $T watchdog                # supervisor das on; sai sozinho se não sobrar on
```

Saída de sucesso de `start`/`say "liga X"`:
```
EXPOINDO: porta 3000 | pasta/servico: ... | nome: demo
demo OK: https://<palavras-aleatorias>.trycloudflare.com
URL(demo)=https://...trycloudflare.com
```
Guarde/imprima essa URL para o usuário. Cada túnel novo gera URL NOVA (a
antiga morre com o processo).

## Roteie a intenção primeiro

| Pedido do usuário | Comando |
|---|---|
| "Liga/expõe o demo (porta 3000)" | `tunnelctl say "liga o demo"` ou `tunnelctl start 3000` |
| "Liga o chat" | `tunnelctl say "liga o chat"` (porta 8000) |
| "Qual o status / está no ar?" | `tunnelctl status` |
| "Desliga/fecha o chat" | `tunnelctl say "desliga o chat"` |
| "Fecha todos, menos o demo" | `tunnelctl stop all --except demo` |
| "Apaga o dummy1" / "apaga tudo" | `tunnelctl delete dummy1` / `delete all` |
| Nova sessão / achar que morreu | `bash /home/z/my-project/tunnel/revive.sh` |
| Binário cloudflared faltando | `bash $T start ...` falha → ver `references/recovery.md` |
| Conversar com usuário pelo celular | serviço `chat` → `references/chat-service.md` |
| Gerar APK do chat | `references/apk-pipeline.md` (pipeline pendente, retomável) |
| Adicionar um novo serviço ao menu | editar `ctl/config.txt` → `references/architecture.md` |

Frases que o `say` entende: liga/abre/inicia/conecta/expõe · desliga/fecha/
para/mata/encerra · apaga/deleta/remove · status/estado · todos/tudo ·
menos/exceto X. Ambígua → resposta PERGUNTA (o sistema pergunta, não age).

## Serviços disponíveis (ctl/config.txt)

| Nome | Porta | Serviço | Marcador de validação |
|---|---|---|---|
| `demo` | 3000 | `http.server` em `tunnel/demo` | `SANDBOX-DEMO-OK` |
| `chat` | 8000 | `tunnel/chat/chat_server.py` | `"ok": true` em `/health` |
| `dummy1` | 8101 | `http.server` em `tunnel/demo-d1` | `SANDBOX-DUMMY-OK` |
| `dummy2` | 8102 | `http.server` em `tunnel/demo-d2` | `SANDBOX-DUMMY-OK` |

## Estado e arquivos (mapa rápido)

| Caminho | Papel |
|---|---|
| `tunnel/ctl/tunnelctl` | comando único (F1: raiz única) |
| `tunnel/ctl/config.txt` | catálogo: nome\|porta\|pasta\|marcador\|caminho\|comando |
| `tunnel/ctl/state/desired.txt` | estado desejado: nome\|porta\|on\|off (ausente = apagado) |
| `tunnel/ctl/run/<nome>.pid` | PID do cloudflared do túnel |
| `tunnel/ctl/run/<nome>.url` | URL VALIDADA (só existe com 200+marcador) |
| `tunnel/ctl/run/<nome>.svc` | PID do serviço local iniciado por este sistema |
| `tunnel/ctl/logs/<nome>.log` | banner do cloudflared (fonte da URL) |
| `tunnel/ctl/allowlist.txt` | portas permitidas para exposição |
| `tunnel/ctl/agents/*.sh` | executor, monitor, orquestrador, decisor, interprete |
| `tunnel/bin/cloudflared` | binário (40MB, linux-amd64) |
| `tunnel/revive.sh` | ressurreição: watchdog + imprime URLs validadas |
| `tunnel/restore.sh` | restaura ctl/ a partir do backup tar |
| `/home/z/my-project/STATUS-ATUAL.md` | documento mestre v2 (leia em chat novo) |

## Integração com o ecossistema de skills (modelo REA)

- **fullstack-dev / Complete**: app Next.js rodando? `tunnelctl start 3000`
  (após aprovação do usuário) expõe o preview para o celular do usuário.
- **agent-browser**: teste a URL pública de dentro do sandbox antes de
  passar ao usuário (o monitor já faz 200+marcador; browser vale para UX).
- **chat-service** (referência abaixo): protocolo HTTP puro para o agente ler
  e responder mensagens do usuário através do túnel — use com qualquer skill
  de conversa (LLM, ASR/TTS) sem WebSocket.
- **REA / browser-ext-re**: padrão estrutural copiado — SKILL.md como índice
  executável + `references/` sob demanda + scripts finos sem lógica própria.
- **worklog.md / STATUS-ATUAL.md**: em chat novo, leia-os ANTES de agir; esta
  skill é o "como", aqueles são o "onde estava".

## Limitações do ambiente (verificadas 2026-10-23/24)

- Gateway pode quebrar a sessão após 1–2 tool calls ("broken session 403");
  comandos bash >~300B podem quebrar → use micro-comandos, 1 tool call por
  turno quando instável, `Write` como 1ª chamada do turno para arquivos.
- Processo em background MORRE quando a VM é reciclada entre turnos — mas o
  filesystem persiste. Por isso: watchdog + autostart + revive.
- URL de Quick Tunnel é efêmera: morre com o processo; cada start = URL nova.
- Quick Tunnel não aceita domínio próprio nem DNS; para isso seria preciso
  conta Cloudflare (fora de escopo; não instalar sem aprovação).
- Estas limitações deixam de valer quando o gateway parar de emitir 403.

## References (leia somente a relevante)

- `references/commands.md` — referência completa do tunnelctl, códigos de saída, exemplos de saída
- `references/say-phrases.md` — gramática do intérprete de frases (say) e tabela verbo→ação
- `references/architecture.md` — arquitetura v2: agentes, ordem interna stop/delete, estado
- `references/recovery.md` — revive, autostart, restore, ensure de binário, checklist de chat novo
- `references/chat-service.md` — API do chat (ler/enviar mensagens), teste célula-a-célula
- `references/apk-pipeline.md` — build do APK WebView do chat (estado atual, próximos passos)
- `references/safety-rules.md` — regras de segurança obrigatórias (v2) e racional
- `references/platform-limits.md` — limites observados da plataforma e disciplina de micro-comandos
