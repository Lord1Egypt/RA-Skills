# architecture.md — Arquitetura v2 (reforma F1–F5)

Princípio central: **um comando na raiz, agentes com papéis exclusivos,
estado em arquivo, verdade validada na borda.** Todos os testes F1, F2, F3,
T1–T7 e F5 PASSARAM (log: `ctl/logs/fases.log`).

## Diagrama de papéis

```
usuário ──ordem──> AGENTE IA ──say──┐
                                    v
                          ctl/tunnelctl (comando único, F1)
                          ├── cmd_start ──> agents/executor.sh ──> cloudflared + serviço
                          │                (ÚNICO que inicia/mata, por pidfile)
                          │            └──> agents/monitor.sh (ÚNICA fonte da verdade:
                          │                  URL só com HTTP 200 na borda + marcador)
                          ├── do_stop/do_delete (ordem fixa a–g, gravar antes de matar)
                          ├── cmd_say (intérprete→decisor→orquestrador embutidos)
                          ├── cmd_autostart (religa só entradas on)
                          └── cmd_watchdog (supervisor das on, flock, loop 15s)
```

- **executor.sh** `iniciar|matar NOME`: sobe serviço local (se porta 127.0.0.1
  não responde) com `setsid nohup`, grava `run/N.svc`; sobe cloudflared
  `tunnel --url http://localhost:PORTA --no-autoupdate`, grava `run/N.pid`,
  log em `logs/N.log`.
- **monitor.sh** `validar|estado NOME`: extrai URL do banner do log (regex,
  exclui `api.trycloudflare.com`), faz curl na borda até 80s esperando
  HTTP 200 + marcador de conteúdo; só então escreve `run/N.url`. Em `estado`,
  apaga `.url` de processo morto.
- **Intérprete/Decisor/Orquestrador**: embutidos no `cmd_say` do tunnelctl
  (frase → verbo+alvo → plano → execução na ordem fixa). Os arquivos
  `agents/orquestrador.sh`, `decisor.sh`, `interprete.sh` são a variante
  daemon do orquestrador (período v2 intermediário; manter por histórico).
- **Wrappers finos** (zero lógica): `tunnel/watchdog.sh`, `tunnel/revive.sh`,
  `skills/quick-tunnel/scripts/{tunnel,autostart}.sh` — todos `exec` para o
  tunnelctl.

## Fluxo de um `start PORTA`

1. Resolve `nome` pela porta no `config.txt` (ou usa nome explícito)
2. `upsert nome porta on` em `state/desired.txt`
3. `executor.sh iniciar nome` → serviço + cloudflared (pidfiles)
4. `monitor.sh validar nome` → valida na borda → escreve `run/nome.url`
5. Imprime `URL(nome)=...` ou `FALHA(nome): sem URL validada`

## Ordem interna stop/delete (a–g) — por que existe

Gravar estado ANTES de matar garante que um crash no meio da operação deixe
o sistema coerente (desired diz off, processo morto; watchdog não religa).
Matar serviço local só se `run/N.svc` existe evita matar processos alheios
(ex.: um dev-server que o usuário subiu manualmente na mesma porta).

## Estado (fontes de verdade)

| Arquivo | Formato | Semântica |
|---|---|---|
| `state/desired.txt` | `nome\|porta\|on\|off` | estado DESEJADO; ausente = apagado |
| `run/<nome>.pid` | PID | cloudflared vivo deste túnel |
| `run/<nome>.url` | URL | URL VALIDADA (200+marcador); não existe = não vale |
| `run/<nome>.svc` | PID | serviço local iniciado POR ESTE sistema |
| `run/watchdog.pid` | PID | watchdog em execução (flock em `run/.wd.lock`) |
| `state/report/*.jsonl` | linhas de eventos | relatórios por agente (auditoria) |
| `state/global.json` | JSON | visão global publicada pelo orquestrador daemon |

## config.txt — catálogo de serviços

Formato: `nome|porta|pasta|marcador|caminho|comando_servico`

```
demo|3000|/home/z/my-project/tunnel/demo|SANDBOX-DEMO-OK|/|python3 -m http.server 3000 --directory /home/z/my-project/tunnel/demo
chat|8000|/home/z/my-project/tunnel/chat|"ok": true|/health|python3 /home/z/my-project/tunnel/chat/chat_server.py
dummy1|8101|...|SANDBOX-DUMMY-OK|/|python3 -m http.server 8101 --directory ...
dummy2|8102|...|SANDBOX-DUMMY-OK|/|python3 -m http.server 8102 --directory ...
```

Para ADICIONAR um serviço: (1) coloque o conteúdo em pasta própria fora da
raiz do projeto, (2) escolha porta em `ctl/allowlist.txt`, (3) defina um
marcador de conteúdo que prove que a página certa está no ar, (4) acrescente
a linha, (5) teste com `tunnelctl start PORTA`. O marcador é OBRIGATÓRIO — é
o que impede URL "válida" apontando para conteúdo errado.

## allowlist.txt

Portas que o sistema aceita expor. Fora dela = não expõe (regra 2 de
safety-rules.md). Conteúdo atual: 3000, 8000, 8101, 8102.

## Backups

- `tunnel/quick-tunnel-backup-final.tar` (39MB, COM binário) — restaura com
  `bash tunnel/restore.sh`
- `tunnel/ctl-backup.tar` (ctl/ sem logs/run)
- `download/quick-tunnel-reforma-v2.tar` + `download/QUICK-TUNNEL-RESTORE.md`
