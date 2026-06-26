# Safety Checklists

## Before any execution
- Confirme o `ad_account_id`.
- Confirme o objetivo de negocio.
- Confirme se o tracking esta confiavel.
- Confirme se a acao esta dentro do escopo do `brijr/meta-mcp`.
- Classifique a acao: `read-only`, `safe-within-limits`, `approval-required` ou `forbidden`.
- Defina prazo de revisao.

## Before creating anything
- Validou naming?
- Validou UTM?
- Validou pixel ou evento necessario?
- Validou destino da campanha?
- Validou se deve nascer em `PAUSED`?

## Before editing budget
- A mudanca e reducao ou aumento?
- Se aumento, esta abaixo de `10%`?
- O ativo esta estavel?
- Nao ha tracking suspeito?
- Nao houve mudanca estrutural recente?

## Before changing structure
- Existe aprovacao explicita?
- Ha racional escrito?
- A estrutura atual ja foi diagnosticada corretamente?
- Ha plano de rollback?

## After execution
- Registre o que foi mudado.
- Registre a ferramenta usada.
- Registre o resultado esperado.
- Registre a janela de revisao.
- Liste riscos residuais.
