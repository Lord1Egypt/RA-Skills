# commands.md — Referência completa do `tunnelctl`

Comando único da raiz `ctl/` (reforma F1). Caminho:
`bash /home/z/my-project/tunnel/ctl/tunnelctl <comando> [args]`

Wrapper equivalente (compatibilidade v1):
`bash /home/z/my-project/skills/quick-tunnel/scripts/tunnel.sh <comando> ...`

## Tabela de comandos

| Comando | Assinatura | Efeito | Confirmação de sucesso |
|---|---|---|---|
| `start` | `start PORTA [nome]` | ÚNICO jeito de ligar. Resolve nome pela porta no config; grava `on` em desired.txt; executor inicia serviço+cloudflared; monitor valida URL | `URL(nome)=https://...trycloudflare.com` |
| `stop` | `stop alvo\|all [--except a,b]` | Marca `off` ANTES de matar; mata cloudflared por pidfile; mata serviço local só se iniciado pelo sistema; para watchdog se não sobrar `on` | `CONFIRMADO: stop <nomes>` |
| `delete` | `delete alvo\|all [--except a,b]` | stop + apaga linha do desired.txt + artefatos (pid/url/svc/log). Lista VAZIA no estado = reset de fábrica | `CONFIRMADO: delete <nomes>` (+ `RESET DE FABRICA` se aplicável) |
| `status` | `status` | Fonte da verdade | cabeçalho `nome\|porta\|estado\|pid\|url` + uma linha por entrada |
| `say` | `say "frase"` | Intérprete→Decisor→Orquestrador (ver say-phrases.md) | varia com o verbo |
| `autostart` | `autostart` | Religa APENAS entradas `on` (para boot) | `AUTOSTART: N entrada(s) on mantidas` ou `NENHUM TUNEL ATIVO` |
| `watchdog` | `watchdog` | Loop 15s: re-executa executor+monitor das `on`; sai sozinho sem `on`; protegido por flock | roda em daemon (pid em `run/watchdog.pid`) |

## Códigos de erro e mensagens

| Mensagem | Causa | Ação do agente |
|---|---|---|
| `FALHA: porta P sem nome e sem config` | porta fora do config e sem nome explícito | passe nome: `start PORTA nome` (mas só se usuário pediu) |
| `FALHA: alvo desconhecido: X` | nome não está no config.txt | ver `tunnelctl status`; corrigir nome |
| `FALHA: excecao desconhecida: X` | `--except` com nome inválido | corrigir lista |
| `FALHA(nome): sem URL validada` | monitor não obteve 200+marcador em 80s | ver recovery.md (verificar serviço local, banner no log) |
| `FALHA: pid sobrou` | kill não derrubou processo | NÃO usar pkill manual; reportar e re-tentar stop |
| `PERGUNTA: ...` | frase ambígua no say | TRANSMITA a pergunta ao usuário; nunca adivinhe |
| `NENHUM TUNEL ATIVO` | autostart/revive sem entradas on | normal; nada a fazer |

## Ordem interna obrigatória (stop/delete) — implementada no tunnelctl

1. Validar alvos e exceções contra config.txt
2. Gravar estado (`off` / remover linha) ANTES de matar qualquer coisa
3. Matar cloudflared por pidfile (`run/<nome>.pid`)
4. Matar serviço local SOMENTE se iniciado por este sistema (`run/<nome>.svc`)
5. Parar watchdog se não sobrar entrada `on`
6. (delete) limpar artefatos; reset de fábrica se desired.txt ficar vazio
7. Imprimir `CONFIRMADO` ou `FALHA` — nunca silêncio

## Exemplos de sessão real

```bash
$ bash $T start 3000
EXPOINDO: porta 3000 | pasta/servico: /home/z/my-project/tunnel/demo | nome: demo
demo OK: https://practice-lip-potter-knit.trycloudflare.com
URL(demo)=https://practice-lip-potter-knit.trycloudflare.com

$ bash $T status
nome|porta|estado|pid|url
demo|3000|on|4123|https://practice-lip-potter-knit.trycloudflare.com
chat|8000|off|-|-

$ bash $T stop all --except demo
CONFIRMADO: stop  chat dummy1 dummy2
```

## Notas

- `start` é idempotente: se o túnel já está vivo, executor devolve
  "ok (ja vivo)" e o monitor só revalida a URL.
- A URL sai do BANNER em `logs/<nome>.log` (regex
  `https://[a-z0-9-]*\.trycloudflare\.com`, exclui `api.`), nunca de suposição.
- Timeout de validação do monitor: 40 tentativas × 2s = 80s máx.
