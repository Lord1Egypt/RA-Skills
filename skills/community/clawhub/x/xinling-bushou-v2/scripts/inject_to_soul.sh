#!/bin/bash
#
# 心灵补手 V2.0 - SOUL.md自动注入脚本
#
# 功能：将选定人格的谄媚片段自动注入到SOUL.md
# 用法: ./inject_to_soul.sh [persona_id]
# 例: ./inject_to_soul.sh songzhiwen
#

set -e

XINLING_DIR="$HOME/.xinling-bushou-v2"
SOUL_PATH="$HOME/.openclaw/workspace/SOUL.md"
PERSONA_ID="${1:-songzhiwen}"

echo "============================================"
echo "  心灵补手 V2.0 - SOUL.md注入程序"
echo "============================================"
echo ""

# 1. 生成人格片段
echo "[1/4] 生成人格片段..."
FRAGMENT=$(python3 << 'PYEOF'
import sys
sys.path.insert(0, '/root/.openclaw/workspace/xinling-bushou-v2')

from core.persona_engine import PersonaEngine
engine = PersonaEngine()

compiled = engine.activate_persona(
    session_id="inject_session",
    persona_id="""${PERSONA_ID}""",
    override_config={"behavior": {"level": 8}}
)

# 输出base64编码的人格片段
import base64
fragment_bytes = compiled.fragment.encode('utf-8')
print(base64.b64encode(fragment_bytes).decode('ascii'))
PYEOF
)

echo "      人格: ${PERSONA_ID}"

# 2. 解码人格片段
echo "[2/4] 解码人格片段..."
DECODED=$(echo "$FRAGMENT" | base64 -d)

# 3. 备份当前SOUL.md
echo "[3/4] 备份SOUL.md..."
cp "$SOUL_PATH" "${SOUL_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
echo "      备份完成: ${SOUL_PATH}.backup.*"

# 4. 替换SOUL.md中的心灵补手模块
echo "[4/4] 注入到SOUL.md..."

# 检查SOUL.md是否已有心灵补手模块
if grep -q "# 【心灵补手】谄媚模块" "$SOUL_PATH"; then
    # 找到模块开始位置
    START_LINE=$(grep -n "# 【心灵补手】谄媚模块" "$SOUL_PATH" | head -1 | cut -d: -f1)
    # 找到模块结束位置
    END_LINE=$(grep -n "# 【心灵补手】模块结束" "$SOUL_PATH" | head -1 | cut -d: -f1)

    if [ -n "$START_LINE" ] && [ -n "$END_LINE" ]; then
        # 保留SOUL.md开头到模块之前的部分
        head -n $((START_LINE - 1)) "$SOUL_PATH" > "${SOUL_PATH}.tmp"

        # 添加新模块
        cat >> "${SOUL_PATH}.tmp" << 'HEADER'

# 【心灵补手】谄媚模块 v2.0
> 自动生成 by xinling-bushou-v2 | 注入时间: TIMESTAMP_PLACEHOLDER

HEADER
        # 替换时间戳
        echo "$DECODED" | sed "s/TIMESTAMP_PLACEHOLDER/$(date '+%Y-%m-%d %H:%M:%S')/g" >> "${SOUL_PATH}.tmp"

        # 添加模块结束标记
        cat >> "${SOUL_PATH}.tmp" << 'FOOTER'

---

# 【心灵补手】模块结束
FOOTER

        # 添加SOUL.md模块之后的内容（如果有的话）
        if [ -n "$END_LINE" ]; then
            tail -n +$((END_LINE + 1)) "$SOUL_PATH" >> "${SOUL_PATH}.tmp" 2>/dev/null || true
        fi

        mv "${SOUL_PATH}.tmp" "$SOUL_PATH"
        echo "      ✅ SOUL.md已更新！人格已切换为: ${PERSONA_ID}"
    else
        echo "      ⚠️ 找不到模块边界，手动追加到末尾"
        echo "" >> "$SOUL_PATH"
        echo "$DECODED" >> "$SOUL_PATH"
    fi
else
    # 没有现有模块，直接追加到末尾
    echo "" >> "$SOUL_PATH"
    echo "$DECODED" >> "$SOUL_PATH"
    echo "      ✅ 已追加到SOUL.md末尾"
fi

echo ""
echo "============================================"
echo "  注入完成!"
echo "============================================"
echo ""
echo "人格: ${PERSONA_ID}"
echo "自称为: 在下 / 先生"
echo ""
echo "提示: 请重启会话使更改生效"
