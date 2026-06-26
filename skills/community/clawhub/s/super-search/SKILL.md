# Skill: Super Search 🔍

> Busca inteligente com conteúdo completo e formatado para WhatsApp

## Gatilho
- **"buscar"** - qualquer mensagem contendo "buscar" ativa esta skill
- Exemplos:
  - "buscar Pablo Murad"
  - "buscar sobre muro de pedra"
  - "busca pizza São Paulo"
  - "buscar padarias perto de mim"

---

## Como Funciona

### 1. Detecção de Idioma
- Se o termo for em português: buscar em PT, EN, ES
- Se for em inglês: buscar em EN, PT
- Se especificar "no Brasil" ou "brasileiro": focar em fontes brasileiras

### 2. Detecção de Localização
- **Keywords**: "perto de mim", "aqui", "perto de", "em [cidade]"
- **Default**: São Lourenço, Minas Gerais, Brasil

### 3. Execução da Busca
- Tavily (principal - traz answer + images + results)
- Brave Search (backup)
- Multi-idioma: PT → EN → ES

### 4. Processamento do Conteúdo
- Buscar conteúdo completo das principais páginas via `web_fetch`
- Extrair informações relevantes de cada fonte
- Consolidar em texto coeso

---

## Formato de Resposta (WhatsApp)

```
🌐 *TÍTULO*

📝 *RESUMO*
[answer do Tavily + informações consolidadas em texto corrido]

📋 *INFORMAÇÕES*
[detalhes em formato de lista com bullet points]
• Item 1
• Item 2
• Item 3

🖼️ *IMAGENS*
[se houver - listar URLs]

📍 *LOCALIZAÇÃO* (se aplicável)
[endereços, mapas, etc]

📰 *NA MÍDIA* (se aplicável)
[publicações, artigos, notícias]

📍 *PRESENÇA ONLINE*
[sites, redes sociais]

🔗 *FONTES*
• fonte 1
• fonte 2
```

---

## Regras de Formatação WhatsApp

- **Negrito/Itálico**: *texto* (WhatsApp interpreta como itálico)
- **Emojis como bullets**: • → •
- **Cabeçalhos**: EMOJI *TÍTULO*
- **Separadores**: linhas em branco entre seções

---

## Comandos de Busca

### Tavily (principal)
```bash
curl -s "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$TAVILY_API_KEY'",
    "query": "TERMO",
    "max_results": 8,
    "include_answer": true,
    "include_images": true
  }'
```

### Brave (backup)
```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=TERMO&count=5" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_API_KEY"
```

---

## Fluxo de Execução

### Step 1: DefinirQuery
- Detectar idioma do termo
- Detectar localização
- Montar queries em múltiplos idiomas

### Step 2: ExecutarBuscas
- Tavily com query principal
- Brave como backup
- Se necessário, buscar em outros idiomas

### Step 3: ProcessarResultados
- Extrair answer
- Extrair results com conteúdo
- Extrair images
- Identificar melhores fontes

### Step 4: BuscarConteúdo
- Pegar top 2-3 URLs mais relevantes
- Buscar conteúdo completo via web_fetch
- Consolidar informações

### Step 5: FormatarResposta
- Montar estrutura com emoji headers
- Inserir informações consolidadas
- Listar fontes
- Formatar para WhatsApp

---

## Exemplos de Output

### Input:
"buscar Pablo Murad"

### Output:
```
🌐 *PABLO MURAD*

📝 *RESUMO*
Pablo Murad é um empreendedor brasileiro focado em tecnologia, educação e construção. Fundador do Portal IDEA, uma das top 10 plataformas educacionais do mundo. CEO de duas empresas. Sua missão é democratizar o conhecimento.

"Eu vim de uma cidade pequena construindo casas com minhas mãos — hoje construo portas para outros caminharem." — Pablo Murad

📋 *INFORMAÇÕES*
• 🗓️ Nascimento: 12 de agosto de 1987, Soledade de Minas, MG
• 🎓 Formação: Direito pela Universidade José do Rosário Vellano
• 💼 Empresas: Portal IDEA (educação), Grupo Murad (holding)
• 🏗️ Trajetória: Começou em canteiros de obras, virou educador
• 🌎 Missão: Democratizar educação no Brasil com cursos gratuitos

🖼️ *IMAGENS*
• https://example.com/image1.jpg
• https://example.com/image2.jpg

📰 *NA MÍDIA*
• USA News: "From Jobsite to Classroom..."

📍 *PRESENÇA ONLINE*
• example.com
• example.com/about
• linkedin.com/in/example

🔗 *FONTES*
• example.com
• example.com/article
• usanews.com
```

---

## API Keys (configuração local)

```bash
# Configure suas próprias chaves
export TAVILY_API_KEY="sua-chave-tavily"
export BRAVE_SEARCH_API_KEY="sua-chave-brave"
```

---

## Variáveis de Ambiente

```bash
# Necessário para executar buscas
export TAVILY_API_KEY="your-tavily-api-key"
export BRAVE_SEARCH_API_KEY="your-brave-api-key"

# Default location (não expor em skill pública)
DEFAULT_CITY="São Lourenço"
DEFAULT_STATE="Minas Gerais"
DEFAULT_COUNTRY="Brasil"
```

---

*Versão 2.0 - Super Search Completo*
*Gatilho: buscar*
*Autor: Seth*
*Data: 07-03-2026*
