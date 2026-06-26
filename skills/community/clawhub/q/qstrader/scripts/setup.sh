#!/usr/bin/env bash
# QStrader — Setup Script
# Настраивает mcporter и проверяет подключение

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔶 QStrader Setup"
echo "=================="

# 1. Проверка .env
if [ ! -f "$SKILL_DIR/.env" ]; then
    if [ -f "$SKILL_DIR/.env.example" ]; then
        cp "$SKILL_DIR/.env.example" "$SKILL_DIR/.env"
        echo "✅ Создан .env из шаблона. Заполните свои ключи:"
        echo "   nano $SKILL_DIR/.env"
        echo ""
        echo "⚠️  После заполнения ключей запустите setup.sh снова."
        exit 1
    else
        echo "❌ Нет .env.example — не могу создать конфигурацию."
        exit 1
    fi
fi
echo "✅ .env найден"

# Загрузить переменные
set -a; source "$SKILL_DIR/.env"; set +a

# 2. Проверка mcporter
if ! command -v mcporter &>/dev/null; then
    echo "❌ mcporter не установлен."
    echo "   Установите: npm install -g mcporter"
    echo "   Или: npx mcporter ..."
    exit 1
fi
echo "✅ mcporter установлен: $(mcporter --version 2>/dev/null || echo 'version unknown')"

# 3. Настройка n8n MCP
if [ -n "${N8N_MCP_URL:-}" ]; then
    echo "📡 Настройка n8n MCP: $N8N_MCP_URL"
    mcporter add my-n8n-mcp --transport http --url "$N8N_MCP_URL" 2>/dev/null || \
        mcporter add my-n8n-mcp --url "$N8N_MCP_URL" 2>/dev/null || \
        echo "⚠️  Не удалось добавить n8n MCP (возможно уже существует)"
    echo "✅ n8n MCP настроен"
else
    echo "❌ N8N_MCP_URL не задан в .env"
fi

# 4. Настройка qdrant-trading (если есть данные)
if [ -n "${QDRANT_URL:-}" ]; then
    echo "🔷 Настройка Qdrant: $QDRANT_URL"
    # qdrant-trading обычно stdio, пропускаем если скрипта нет
    echo "✅ Qdrant URL задан"
fi

# 5. Тестовое подключение
echo ""
echo "🧪 Тестовое подключение..."
TEST_RESULT=$(mcporter call my-n8n-mcp.Get_account_data 2>&1 || echo "FAILED")
if echo "$TEST_RESULT" | grep -q "error\|FAILED\|ECONNR"; then
    echo "❌ Не удалось подключиться к n8n MCP"
    echo "   Проверьте N8N_MCP_URL в .env"
    echo "   Ответ: $TEST_RESULT" | head -5
else
    echo "✅ Подключение успешно!"
    echo "$TEST_RESULT" | head -10
fi

echo ""
echo "=================="
echo "🔶 QStrader setup завершён"
