#!/bin/bash
# Script para buscar piadas aleatórias do r/tiodopave

# Busca as piadas via Reddit API
CONTENT=$(curl -s "https://www.reddit.com/r/tiodopave/hot.json?limit=30" -H "User-Agent: OpenClaw/1.0" 2>/dev/null)

if [ -z "$CONTENT" ]; then
    echo "Erro ao buscar piadas. Tente novamente."
    exit 1
fi

# Salva em temp file e processa com python
echo "$CONTENT" > /tmp/reddit_tiodopave.json

PIADA=$(python3 << 'PYEOF'
import json, random

try:
    with open('/tmp/reddit_tiodopave.json', 'r') as f:
        data = json.load(f)
    
    posts = [p['data'] for p in data['data']['children'] 
             if p['data'].get('is_self') and p['data'].get('selftext')]
    
    if posts:
        p = random.choice(posts)
        title = p.get('title', '')
        text = p.get('selftext', '')[:500]
        
        if text:
            print(f'{title}\n\n{text}')
        else:
            print(title)
    else:
        print('Nenhuma piada encontrada')
        
except Exception as e:
    # Fallback: só títulos
    try:
        data = json.loads(open('/tmp/reddit_tiodopave.json').read())
        posts = [p['data']['title'] for p in data['data']['children'][:20]]
        if posts:
            print(random.choice(posts))
        else:
            print('Nenhuma piada encontrada')
    except:
        print(f'Erro: {e}')
PYEOF
)

echo "$PIADA"
