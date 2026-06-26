# seth_receitas_ptbr

Skill do OpenClaw para buscar receitas em português do Brasil (pt-BR).

## Fontes

### Wikilivros (pt.wikibooks.org)
- **Tipo:** API MediaWiki pública
- **Conteúdo:** Receitas colaborativas em português
- **Licença:** Creative Commons Attribution-ShareAlike 3.0
- **URL:** https://pt.wikibooks.org/wiki/Categoria:Receitas
- **API:** https://pt.wikibooks.org/w/api.php

### TheMealDB
- **Tipo:** API REST pública
- **Conteúdo:** Receitas internacionais com tradução
- **Licença:** Atribuição necessária (uso não comercial)
- **URL:** https://www.themealdb.com/
- **API:** https://www.themealdb.com/api/json/v1/1/

### OpenFoodFacts (Opcional)
- **Tipo:** API pública
- **Uso:** Apenas para informações nutricionais quando solicitado
- **URL:** https://world.openfoodfacts.org/

## Instalação

A skill já está instalada em:
```
~/.openclaw/workspace/skills/seth-receitas-ptbr/
```

## Uso via CLI

### 1. Buscar receitas
```bash
# Buscar por termo
python3 src/cli.py buscar --q "bolo de cenoura"

# Buscar em fonte específica
python3 src/cli.py buscar --q "pão" --fonte mealdb

# Com limite de resultados
python3 src/cli.py buscar --q "salada" --max 10
```

### 2. Obter receita completa
```bash
# Via TheMealDB (por ID)
python3 src/cli.py obter --fonte mealdb --id 52772

# Via Wikilivros (por título)
python3 src/cli.py obter --fonte wikibooks --titulo "Bolo_de_cenoura"
```

### 3. Sugerir por ingredientes
```bash
# Com ingredientes
python3 src/cli.py sugerir --ingredientes "arroz, frango, tomate"

# Com restrições dietéticas
python3 src/cli.py sugerir --ingredientes "grão-de-bico" --restricoes vegana

# Com tempo máximo
python3 src/cli.py sugerir --ingredientes "massa" --tempo-max 30
```

### 4. Receita aleatória
```bash
python3 src/cli.py random
```

### 5. Nutrição (opcional)
```bash
python3 src/cli.py nutricao --ingrediente "aveia"
```

## Exemplos de Uso

### Exemplo 1: Buscar bolo de cenoura
```
$ python3 src/cli.py buscar --q "bolo de cenoura"

🔍 Resultados para "bolo de cenoura":

1. Bolo de Cenoura Tradicional
   Fonte: TheMealDB | ID: 52771
   Tags: Dessert, Brazilian

2. Bolo de Cenoura com Chocolate
   Fonte: Wikilivros | Categoria: Bolos
```

### Exemplo 2: Obter receita específica
```
$ python3 src/cli.py obter --fonte mealdb --id 52771

🍽️ Bolo de Cenoura (Brazilian Carrot Cake)

📊 Porções: 8 porções
⏱️ Tempo: 60 minutos

📝 Ingredientes:
- 3 cenouras médias raladas
- 4 ovos
- 1 xícara de óleo
- 2 xícaras de açúcar
- 2 xícaras de farinha de trigo
- 1 colher de fermento

👨‍🍳 Modo de preparo:
1. Preaqueça o forno a 180°C.
2. Bata no liquidificador as cenouras, os ovos e o óleo.
3. Em uma tigela, misture o açúcar e a farinha.
4. Adicione a mistura do liquidificador e mexa bem.
5. Acrescente o fermento e misture delicadamente.
6. Asse por aproximadamente 40 minutos.

🏷️ Tags: doce, bolo, brunch

📦 Fonte: TheMealDB (https://www.themealdb.com/meal/52771)
```

## Promise

> "Eu busco receitas nas fontes suportadas (Wikilivros + TheMealDB). Se não encontrar algo bom, gero uma receita original."

## Limitações

- Wikilivros: Nem todas as receitas têm formato estruturado
- TheMealDB: Traduções podem variar em qualidade
- OpenFoodFacts: Nem todos os ingredientes têm dados nutricionais

## Cache

A skill implementa cache local:
- Wikilivros: 24h TTL
- TheMealDB: 6h TTL

Cache armazenado em: `state/cache.json`

## Desenvolvimento

### Estrutura dos Módulos
```
src/
├── cli.py              # Interface de linha de comando
├── wikibooks_client.py # Cliente MediaWiki
├── mealdb_client.py   # Cliente TheMealDB
├── recipe_extract.py   # Extrator de receitas HTML
├── normalize.py        # Normalização de texto
├── nutrition_off_client.py  # Cliente OpenFoodFacts (opcional)
└── cache.py           # Sistema de cache
```

### Dependências
- Python 3.7+ (stdlib only - apenas html.parser da stdlib)
- Sem dependências externas necessárias!
