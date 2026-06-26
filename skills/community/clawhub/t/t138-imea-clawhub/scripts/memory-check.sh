#!/bin/bash

# memory-check.sh - 行動前記憶檢查腳本
# 版本：v1.0
# 創建時間：2026-04-04 17:30
# CEO 要求：行動前必須搜索記憶

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

cd "$WORKSPACE_DIR"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 用法
usage() {
    echo -e "${BLUE}用法：$0 <關鍵詞>${NC}"
    echo ""
    echo "行動前記憶檢查 - 搜索記憶、SESSION-STATE、.learnings/"
    echo ""
    echo "示例:"
    echo "  $0 ClawHub"
    echo "  $0 上架"
    echo "  $0 重複錯誤"
    exit 1
}

# 檢查參數
if [ -z "$1" ]; then
    usage
fi

KEYWORD="$1"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}🔍 行動前記憶檢查：$KEYWORD${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 計數
FOUND_COUNT=0

# 1. 搜索記憶文件
echo -e "${YELLOW}1️⃣  搜索記憶文件 (memory/)${NC}"
echo "-----------------------------------"
if grep -ri "$KEYWORD" memory/*.md 2>/dev/null; then
    echo -e "${GREEN}✅ 找到記憶記錄${NC}"
    FOUND_COUNT=$((FOUND_COUNT + 1))
else
    echo -e "${RED}❌ 無記憶記錄${NC}"
fi
echo ""

# 2. 檢查 SESSION-STATE.md
echo -e "${YELLOW}2️⃣  檢查 SESSION-STATE.md${NC}"
echo "-----------------------------------"
if [ -f SESSION-STATE.md ]; then
    if grep -i "$KEYWORD" SESSION-STATE.md 2>/dev/null; then
        echo -e "${GREEN}✅ 找到 WAL 記錄${NC}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    else
        echo -e "${RED}❌ 無 WAL 記錄${NC}"
    fi
else
    echo -e "${RED}❌ SESSION-STATE.md 不存在${NC}"
fi
echo ""

# 3. 檢查錯誤記錄
echo -e "${YELLOW}3️⃣  檢查錯誤記錄 (.learnings/ERRORS.md)${NC}"
echo "-----------------------------------"
if [ -f .learnings/ERRORS.md ]; then
    if grep -i "$KEYWORD" .learnings/ERRORS.md 2>/dev/null; then
        echo -e "${GREEN}✅ 找到錯誤記錄${NC}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    else
        echo -e "${GREEN}✅ 無類似錯誤${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .learnings/ERRORS.md 不存在${NC}"
fi
echo ""

# 4. 檢查學習記錄
echo -e "${YELLOW}4️⃣  檢查學習記錄 (.learnings/LEARNINGS.md)${NC}"
echo "-----------------------------------"
if [ -f .learnings/LEARNINGS.md ]; then
    RESULT=$(grep -i "$KEYWORD" .learnings/LEARNINGS.md 2>/dev/null || echo "")
    if [ -n "$RESULT" ]; then
        echo "$RESULT"
        echo -e "${GREEN}✅ 找到學習記錄${NC}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    else
        echo -e "${GREEN}✅ 無相關學習${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .learnings/LEARNINGS.md 不存在${NC}"
fi
echo ""

# 5. 檢查重複錯誤
echo -e "${YELLOW}5️⃣  檢查重複錯誤 (Recurrence-Count)${NC}"
echo "-----------------------------------"
if [ -f .learnings/LEARNINGS.md ]; then
    HIGH_RECURRENCE=$(grep -B5 "Recurrence-Count: [3-9]" .learnings/LEARNINGS.md 2>/dev/null | grep -i "$KEYWORD" || echo "")
    if [ -n "$HIGH_RECURRENCE" ]; then
        echo -e "${RED}🚨 發現高重複錯誤（Recurrence-Count ≥3）:${NC}"
        echo "$HIGH_RECURRENCE"
        echo ""
        echo -e "${RED}⚠️  熔斷機制觸發！需要 CEO 決策！${NC}"
    else
        echo -e "${GREEN}✅ 無高重複錯誤${NC}"
    fi
fi
echo ""

# 總結
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}📊 檢查總結${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

if [ $FOUND_COUNT -gt 0 ]; then
    echo -e "${GREEN}✅ 找到 $FOUND_COUNT 個相關記錄${NC}"
    echo ""
    echo -e "${YELLOW}建議：${NC}"
    echo "1. 詳細閱讀相關記錄"
    echo "2. 確認是否有衝突或重複"
    echo "3. 如有疑問，報告 CEO"
else
    echo -e "${RED}❌ 無相關記錄${NC}"
    echo ""
    echo -e "${YELLOW}建議：${NC}"
    echo "1. 確認關鍵詞是否正確"
    echo "2. 嘗試其他相關關鍵詞"
    echo "3. 如確認無記錄，可以行動但需記錄 WAL"
fi
echo ""

# 返回狀態
if [ $FOUND_COUNT -gt 0 ]; then
    exit 0
else
    exit 1
fi
