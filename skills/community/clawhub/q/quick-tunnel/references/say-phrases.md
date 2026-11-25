# say-phrases.md — Gramática do intérprete (`tunnelctl say`)

`say` é a interface em português para AGENTES de IA. Implementado em
`ctl/tunnelctl cmd_say`: normaliza minúsculas → extrai verbo e alvos → executa
na ordem fixa. Frase ambígua devolve `PERGUNTA: ...` (o sistema pergunta em
vez de agir — NUNCA start por padrão).

## Tabela verbo → ação

| Palavras na frase | Ação interna |
|---|---|
| liga, abre, inicia, conecta, expõe/expos | `start` (via cmd_start) |
| desliga, fech*, parar, mata, encerr* | `stop` (do_stop) |
| apag*, delet*, remov* | `delete` (do_delete) |
| status, estado | `status` (cmd_status) |

## Alvos reconhecidos

- Nomes literais: `demo`, `chat`, `dummy1`, `dummy2` (grep `\b<nome>\b`).
- `todos`, `tudo`, `todes` → alvo `all`.
- `menos X` / `exceto X` → vira `--except X` (apenas para stop/delete;
  para start é ignorado e pode gerar PERGUNTA).

## Exemplos (frase → resultado)

| Frase | Resultado |
|---|---|
| `"liga o chat"` | start na porta 8000, URL validada impressa |
| `"abre o demo"` | start na porta 3000 |
| `"desliga o chat"` | stop chat → `CONFIRMADO: stop chat` |
| `"fecha todos menos o demo"` | stop all --except demo |
| `"apaga o dummy1"` | delete dummy1 |
| `"apaga tudo"` | delete all (reset de fábrica se ficar vazio) |
| `"status"` | tabela de status |
| `"liga"` | `PERGUNTA: ligar qual túnel? ...` (nunca adivinha) |
| `"liga o túnel"` | `PERGUNTA: ligar qual túnel? ...` |
| `"fecha o que estiver on exceto demo"` | stop all --except demo |
| `"faz um sanduíche"` | `PERGUNTA: o que faço? (ligar/desligar/apagar/status)` |

## Regras para o agente

1. **Sempre use `say`** quando o usuário falar em linguagem natural; use o
   comando direto (`start/stop/...`) quando já tiver certeza absoluta.
2. Se a saída for `PERGUNTA: ...`, repasse a pergunta ao usuário VERBATIM e
   aguarde. Não tente interpretar por conta própria.
3. `say` não entende nomes fora do config.txt — para serviço novo, adicione
   primeiro ao config (ver architecture.md) e então `say` funcionará.
4. A expansão de vocabulário (novos sinônimos/alvos) é feita editando
   `cmd_say` no tunnelctl — manter a disciplina PERGUNTA-em-dúvida.
