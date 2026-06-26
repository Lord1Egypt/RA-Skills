# tiodopave - Piadas do Reddit

Busca piadas aleatórias do subreddit r/tiodopave (reddit.com/r/tiodopave).

## Uso

```bash
node ~/.openclaw/workspace/skills/tiodopave/index.mjs
```

## O que faz

1. Busca os posts mais recentes do r/tiodopave (limit: 20)
2. Filtra posts com score > 5
3. Escolhe um aleatoriamente
4. Retorna o título e o conteúdo (selftext)

## Regras

- **NUNCA usar piadas geradas por IA** — só conteúdo real do Reddit
- **Sem repetição** — evitar a última piada enviada (armazenar em /tmp/last-joke.txt)
- **Limpar texto** — remover links, formatação Reddit, emojis excessivos
- **Sem NSFW** — filtrar posts flaired "NSFW" ou que contenham palavras-chave adulto
