# recovery.md — Ressurreição e checklist de chat novo

O filesystem `/home/z/my-project` PERSISTE entre sessões; processos em
background NÃO (a VM é reciclada). Portanto: nunca presuma que o túnel está
vivo; sempre verifique/reviva.

## Sequência de boot de chat novo (nesta ordem)

```bash
# 1. Leia o contexto (barato e evita retrabalho):
#    /home/z/my-project/worklog.md e /home/z/my-project/STATUS-ATUAL.md

# 2. Ressurreição em 1 comando (imprime URLs validadas ou "NENHUM TUNEL ATIVO"):
bash /home/z/my-project/tunnel/revive.sh
```

Saídas possíveis do revive:
- `NENHUM TUNEL ATIVO` → estado coerente, nada on. Se o usuário quer túnel,
  ele precisa PEDIR (`tunnelctl start ...`).
- `URL(nome)=https://...` → túnel(s) revalidado(s) no ar; informe o usuário.
- `nome FALHA: sem URL validada` → executor+watchdog estão tentando; aguarde
  e rode `tunnelctl status`; se persistir, siga para "Diagnóstico" abaixo.

## Se `ctl/` ou binário sumiram (VM recriada do zero)

```bash
# ctl/ inteiro restaurado do backup (inclui tunnelctl, agents, config):
bash /home/z/my-project/tunnel/restore.sh

# Binário cloudflared faltando (baixa em background e instala):
bash /home/z/my-project/skills/quick-tunnel/scripts/install.sh

# Verificação rápida:
bash /home/z/my-project/tunnel/ctl/tunnelctl status
```

Backup principal (com binário, 39MB): `tunnel/quick-tunnel-backup-final.tar`.
Backups secundários: `tunnel/ctl-backup.tar`,
`download/quick-tunnel-reforma-v2.tar`, `download/quick-tunnel-backup.tar`.

## Diagnóstico de túnel que não sobe

Ordem fixa de verificação (cada passo é um micro-comando <300B):

1. `bash $T status` → a entrada existe? estado on?
2. Serviço local vivo? `curl -s -m 3 http://127.0.0.1:PORTA` deve responder
   (para chat: `curl -s http://127.0.0.1:8000/health` contém `"ok": true`).
3. Banner no log? `tail -5 /home/z/my-project/tunnel/ctl/logs/<nome>.log`
   deve conter `https://xxx.trycloudflare.com`.
4. Sem banner → cloudflared morreu na subida (rede/limite): re-run
   `tunnelctl stop <nome>` e depois `tunnelctl start PORTA`.
5. Banner existe mas borda não dá 200 → serviço local caiu; volte ao passo 2.
6. NUNCA confie em `api.trycloudflare.com` (URL falsa do banner de erro).

## Watchdog e autostart — quem mantém o quê

- `tunnelctl watchdog`: daemon (flock), loop 15s, re-executa executor+monitor
  das entradas `on`; sai sozinho quando não sobra nenhuma `on`.
- `tunnelctl autostart`: chamado 1x no boot (hook `~/.bashrc` →
  `skills/quick-tunnel/scripts/autostart.sh`); religa APENAS entradas on.
- `revive.sh`: para uso MANUAL/por agente — sobe watchdog se preciso e
  imprime as URLs validadas. É a porta de entrada de qualquer sessão nova.

## Histórico de túneis validados (referência)

- kernel-fountain-reason-swap (morto)
- approved-col-started-aerospace (morto)
- practice-lip-potter-knit (ativo em 2026-10-23, porta 3000/demo)

Cada start gera URL nova; o histórico serve só para reconhecer URLs antigas
em screenshots/mensagens do usuário.
