---
name: seth_receitas_ptbr
description: Busca receitas em português do Brasil (pt-BR) via Wikilivros + TheMealDB. Gera receitas originais quando necessário.
---

# seth_receitas_ptbr - Skill de Receitas

## Visão Geral

Esta skill busca receitas completas em português do Brasil usando apenas fontes legais:
- **Wikilivros** (pt.wikibooks.org) - Receitas colaborativas livres
- **TheMealDB** - API pública de receitas internacionais

Se nenhuma fonte retornar resultado satisfatório, a skill pode gerar uma **receita original**.

## Gatilhos (Triggers)

A skill ativa quando a mensagem conter:
- "receita", "modo de preparo", "ingredientes", "como fazer", "passo a passo"
- "vegano/vegana", "vegetariano", "sem glúten", "sem lactose", "low carb", "dieta", "alta proteína"
- "cardápio", "plano alimentar", "lista de compras"
- "o que eu posso cozinhar com <ingredientes>"

## Como Usar

### Buscar receitas
```bash
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py buscar --q "bolo de cenoura"
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py buscar --q "frango" --fonte mealdb --max 10
```

### Obter receita específica
```bash
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py obter --fonte mealdb --id 52772
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py obter --fonte wikibooks --titulo "Bolo_de_cenoura"
```

### Sugerir receita por ingredientes
```bash
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py sugerir --ingredientes "arroz, frango, tomate"
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py sugerir --ingredientes "grão-de-bico" --restricoes vegana
```

### Receita aleatória
```bash
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py random
```

### Verificar nutrição (opcional)
```bash
python3 ~/.openclaw/workspace/skills/seth-receitas-ptbr/src/cli.py nutricao --ingrediente "avena"
```

## Fontes e Licenças

### Wikilivros (pt.wikibooks.org)
- Conteúdo sob licença Creative Commons Attribution-ShareAlike
- URL: https://pt.wikibooks.org/wiki/Categoria:Receitas
- Sempre incluir atribuição quando usar

### TheMealDB
- API gratuita para uso não comercial
- URL: https://www.themealdb.com/
- Attribution required nos termos de uso

## Promise

> "Eu busco receitas nas fontes suportadas (Wikilivros + TheMealDB). Se não encontrar algo bom, posso gerar uma receita original."

## Formato de Resposta

Todas as receitas são retornadas em pt-BR com:
- Título
- Porções/Rendimento
- Tempo de preparo
- Ingredientes (lista)
- Modo de preparo (passos numerados)
- Tags (vegano/vegetariano/sem glúten/etc)
- Fonte + Link/ID
