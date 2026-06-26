#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Workspace Guardian — Script de validação e auto-fix
# Roda no startup para garantir que workspace está saudável
# ═══════════════════════════════════════════════════════════

set -uo pipefail

WORKSPACE="/data/.openclaw/workspace"
CONFIG="/data/.openclaw/openclaw.json"
ISSUES=0
FIXED=0

echo "🛡️ Workspace Guardian — Validação de startup"
echo "================================================"

# ── 1. Diretórios essenciais ──
for dir in "$WORKSPACE/memory" "$WORKSPACE/memory/topics"; do
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    echo "✅ Criado diretório: $dir"
    FIXED=$((FIXED + 1))
  fi
done

# ── 2. Arquivos essenciais ──
if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
  cat > "$WORKSPACE/MEMORY.md" << 'EOF'
# MEMORY.md — Índice de Memória

> Arquivo criado automaticamente pelo Workspace Guardian.
> Edite conforme necessário.

---

## 📅 Timeline

| Data | O Quê | Status |
|------|-------|--------|

---

## 📝 Notas

_(Adicione notas importantes aqui)_
EOF
  echo "✅ Criado MEMORY.md"
  FIXED=$((FIXED + 1))
fi

# ── 3. Diário de hoje ──
TODAY=$(date +%Y-%m-%d)
DIARY="$WORKSPACE/memory/$TODAY.md"
if [ ! -f "$DIARY" ]; then
  cat > "$DIARY" << EOF
# $TODAY — Diário

## Sessão 1

### O que foi feito
- (registrar atividades aqui)

### Próximos passos
- (registrar próximos passos aqui)
EOF
  echo "✅ Criado diário de hoje: $DIARY"
  FIXED=$((FIXED + 1))
fi

# ── 4. Validar openclaw.json ──
if [ -f "$CONFIG" ]; then
  # Verificar se é JSON válido
  if ! python3 -c "import json; json.load(open('$CONFIG'))" 2>/dev/null; then
    echo "🔴 ERRO: openclaw.json não é JSON válido!"
    ISSUES=$((ISSUES + 1))
  else
    # Verificar URLs HTTP (sem S)
    HTTP_URLS=$(python3 -c "
import json
with open('$CONFIG') as f:
    data = json.load(f)
providers = data.get('models', {}).get('providers', {})
for name, prov in providers.items():
    url = prov.get('baseUrl', '')
    if url.startswith('http://'):
        print(f'  ⚠️ Provider \"{name}\" usa HTTP: {url}')
" 2>/dev/null || true)
    
    if [ -n "$HTTP_URLS" ]; then
      echo "🔴 URLs HTTP encontradas (devem ser HTTPS):"
      echo "$HTTP_URLS"
      ISSUES=$((ISSUES + 1))
    fi

    # Verificar apiKeys presentes
    EMPTY_KEYS=$(python3 -c "
import json
with open('$CONFIG') as f:
    data = json.load(f)
providers = data.get('models', {}).get('providers', {})
for name, prov in providers.items():
    key = prov.get('apiKey', '')
    if not key or key.strip() == '':
        print(f'  ⚠️ Provider \"{name}\" sem apiKey')
" 2>/dev/null || true)

    if [ -n "$EMPTY_KEYS" ]; then
      echo "🔴 API Keys ausentes:"
      echo "$EMPTY_KEYS"
      ISSUES=$((ISSUES + 1))
    fi
  fi
else
  echo "🔴 ERRO: openclaw.json não encontrado!"
  ISSUES=$((ISSUES + 1))
fi

# ── 5. Permissões ──
if [ -d "$WORKSPACE" ]; then
  # Garantir que arquivos do workspace são legíveis
  for f in $(find "$WORKSPACE" -name "*.md" -not -readable 2>/dev/null); do
    chmod 644 "$f"
    echo "✅ Corrigido permissão: $f"
    FIXED=$((FIXED + 1))
  done
fi

# ── Resultado ──
echo "================================================"
echo "🛡️ Validação completa: $ISSUES problemas, $FIXED corrigidos"

if [ "$ISSUES" -gt 0 ]; then
  exit 1
fi

exit 0
