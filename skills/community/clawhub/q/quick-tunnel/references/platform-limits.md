# platform-limits.md — Limites observados da plataforma (2026-10-23/24)

Válido enquanto o gateway emitir `broken session 403`. Se um dia parar,
ignore este arquivo. Fonte: saga de diagnóstico 2026-10-23/24 (NÃO repita).

## Sintomas observados

- **Gateway quebra a sessão** após ~1–2 tool calls por mensagem
  ("broken session 403").
- **Comandos bash >~300 bytes** ou **>~15s em foreground** podem quebrar a
  sessão no mesmo turno.
- **VM reciclada entre turnos**: processos em background (`setsid nohup ... &`)
  MORREM; filesystem `/home/z/my-project` PERSISTE (binário, skill, estado).
- **Chamada bash longa EM PRIMEIRO PLANO com timeout 600000 funcionou**
  (pipeline de ~8 min passou) — foreground longo é mais confiável que
  background entre turnos.
- **URL de Quick Tunnel morre com o processo**; cada túnel novo = URL nova.

## Disciplina de micro-comandos (quando o ambiente estiver instável)

1. **1 tool call por turno** — não encadeie chamadas.
2. Comandos bash **<300 bytes, <15s**; operações longas: script em disco +
   foreground com `timeout: 600000`.
3. **`Write` como 1ª chamada do turno** para arquivos grandes — é o canal
   mais confiável observado.
4. Arquivos de estado são a memória: depois de cada ação relevante, grave
   resultado em `worklog.md`/`STATUS-ATUAL.md`/`run/*.txt` — o próximo turno
   pode nascer numa VM nova.
5. NUNCA presuma processo vivo: `kill -0 $(cat pidfile)` / curl de saúde.
6. Downloads: sempre `curl -C -` (retomável) e registro de progresso em
   `run/*.txt` (padrão do pipeline APK).

## Padrões que FUNCIONARAM

- Script persistido + foreground com timeout 600000 (8 min OK).
- `setsid nohup` para daemons DENTRO de um turno + watchdog que re-cria no
  turno seguinte (auto-cura via autostart/revive).
- Estado em arquivos simples (`desired.txt`, pidfiles, `.url`) em vez de
  memória volátil de processo.
- Validar toda URL com curl na borda + marcador (falso positivo eliminado).

## Padrões que FALHARAM

- Encadear 3+ tool calls no mesmo turno (403 na 2ª/3ª).
- bash inline >300B (heredoc longo no command).
- Confiar que daemon de turno anterior sobreviveu.
- Considerar banner do cloudflared como URL válida sem curl (api. prefixo).

## Se o ambiente estiver estável (sem 403 recentes)

Pode relaxar parcialmente (2–3 tool calls por turno, comandos maiores), mas
mantenha: validação de URL, pidfiles, estado em arquivo, revive como entrada
de sessão. A disciplina barata evita regressão quando a instabilidade voltar.
