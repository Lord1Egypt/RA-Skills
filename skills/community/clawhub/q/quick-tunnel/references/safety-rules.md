# safety-rules.md — Regras de segurança obrigatórias (reforma v2)

Fonte canônica: `tunnel/ctl/regras_seguranca.txt`. Este arquivo expande o
racional. VIOLAÇÃO de qualquer regra = parar a operação e reportar.

## As 7 regras

1. **PROIBIDO servir** `/home/z/my-project` (raiz), `/home/z` ou `/` — só
   diretórios declarados no `ctl/config.txt`.
2. **PROIBIDO expor porta fora de `ctl/allowlist.txt`** (atual: 3000, 8000,
   8101, 8102).
3. **EXPOSIÇÃO de túnel SÓ com confirmação explícita do usuário no chat.**
   "Confirma aí pra mim" não conta; tem que ser o usuário pedindo.
4. **URL só é válida com curl na borda retornando HTTP 200 + marcador de
   conteúdo REAL** (definido por serviço no config.txt).
5. **`api.trycloudflare.com` é URL FALSA** — aparece em banner de erro;
   banido de qualquer regex/relatório.
6. **pkill NUNCA sem filtro** — e mesmo com filtro, prefira NUNCA usar:
   kill por pidfile via executor é o caminho.
7. **Autostart sobe orquestrador com desired = TUDO DESLIGADO** — boot nunca
   cria túnel; só mantém o que o usuário explicitamente deixou on.

## Racional (por que cada regra existe)

- **Regra 1/2**: servir a raiz do projeto publicaria `.env`, chaves,
  worklog, backups e todo o código — o túnel é PÚBLICO (URL aleatória, mas
  sem senha). Allowlist impede que um `start 22` ou `start 5432` exponha
  infraestrutura.
- **Regra 3**: o agente nunca decide expor por conveniência ("já que
  terminei o app, vou te dar uma URL"). A SKILL.md proíbe oferta automática
  de túnel ao término de tarefas.
- **Regra 4**: URL no banner não garante que o serviço certo está atrás
  dela (pode estar morto, pode ser outra porta, pode ser página de erro).
  O marcador de conteúdo prova que o CONTEÚDO certo está na borda.
- **Regra 5**: `https://api.trycloudflare.com` aparece em banners de falha
  e parece URL válida; já causou falso positivo. Sempre filtrar.
- **Regra 6**: `pkill cloudflared` mataria túneis de outros serviços;
  `pkill -f "tunnel --url http://localhost:PORTA"` é o único filtro aceito,
  mas o design v2 torna isso desnecessário (pidfiles).
- **Regra 7**: boot com tudo desligado evita "túnel fantasma" — URL pública
  no ar sem ninguém lembrando dela.

## Checklist antes de informar URL ao usuário

- [ ] A ordem veio do USUÁRIO?
- [ ] Porta está na allowlist? Conteúdo está no config.txt (não é raiz)?
- [ ] Monitor validou (200 + marcador)? `run/<nome>.url` existe?
- [ ] A URL NÃO é `api.trycloudflare.com`?
- [ ] Status mostra `estado=on` e `pid` vivo?

## Disclosure

Quick Tunnel é anônimo e efêmero: qualquer pessoa com a URL acessa. Não
coloque conteúdo sensível no túnel; para acesso restrito, seria preciso
Cloudflare Access (conta) — fora de escopo desta skill.
