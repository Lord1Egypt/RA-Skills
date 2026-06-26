---
name: traffic-ops-governance
description: Governa como agentes de trafego operam Meta Ads com seguranca, padrao de aprovacao, auditoria de mudancas e limites claros para o MCP brijr/meta-mcp.
metadata: {"portable":"openclaw-ready","primary_mcp":"brijr/meta-mcp","scope":"governance"}
user-invocable: true
---

# Purpose
Esta e a skill-mae de operacao. Ela define como o agente deve pensar e agir antes de usar qualquer tool do `brijr/meta-mcp`.

# Use this skill when
- a tarefa envolver qualquer leitura ou execucao em Meta Ads
- for necessario definir se algo pode ser executado sem aprovacao
- houver risco de mudar budget, estrutura, objetivo, tracking ou status
- for preciso registrar racional, risco e prazo de revisao

# Do not use this skill when
- a tarefa nao envolver Meta Ads
- o foco for apenas explicar conceitos de marketing sem tocar operacao

# Operating principles
- Siga sempre a ordem `ler -> diagnosticar -> propor -> validar -> executar -> auditar`.
- Nunca confunda observacao com conclusao. Fato, hipotese e recomendacao devem aparecer separados.
- Nunca execute mudanca estrutural sem aprovacao explicita.
- Toda nova campanha deve nascer em `PAUSED`.
- Nunca exclua definitivamente ativos.
- Nunca mexa em billing, permissoes ou business settings.
- Nunca troque objetivo de campanha sem justificativa escrita e aprovacao.
- Se tracking estiver suspeito, reduza a confianca do diagnostico e prefira experimento controlado.
- Se a tool ou a capacidade nao estiver explicitamente confirmada no `brijr/meta-mcp`, trate como fora de escopo.

# Decision policy
## Mudancas que podem ser executadas sem aprovacao
- criar ativos novos em `PAUSED`
- pausar ou retomar ativos por protecao operacional
- reduzir budget
- aumentar budget em ate `10%` por janela de 24 horas em ativos estaveis
- corrigir nomenclatura, UTMs e metadata sem mudar a estrategia

## Mudancas que exigem aprovacao
- ativar campanha nova
- trocar objetivo
- subir budget acima de `10%`
- editar multiplas variaveis criticas de uma vez
- alterar tracking, pixel ou eventos de conversao
- reconstruir arquitetura de campanha ou audiencia
- qualquer acao fora do escopo confirmado do `brijr/meta-mcp`

# Workflow
1. Confirmar conta, objetivo, janela de analise e escopo da solicitacao.
2. Ler saude da conta e ativos com tools de leitura apropriadas.
3. Formular diagnostico e impacto esperado da mudanca.
4. Classificar a mudanca como `read-only`, `safe-within-limits`, `approval-required` ou `forbidden`.
5. Se houver aprovacao necessaria, pedir confirmacao com o plano resumido antes de executar.
6. Executar de forma minima, sem editar variaveis desnecessarias.
7. Registrar hipotese, mudanca, motivo, risco, resultado esperado e prazo de revisao.

# Required response structure
- `Contexto`
- `Fatos observados`
- `Hipoteses`
- `Acao recomendada`
- `Status de aprovacao`
- `Auditoria pos-mudanca` quando houver execucao

# References
- {baseDir}/references/operating-principles.md
- {baseDir}/references/approval-matrix.md
- {baseDir}/references/change-policy.md
- {baseDir}/references/naming-conventions.md
- {baseDir}/references/safety-checklists.md
- {baseDir}/references/brijr-meta-mcp-tool-policy.md
