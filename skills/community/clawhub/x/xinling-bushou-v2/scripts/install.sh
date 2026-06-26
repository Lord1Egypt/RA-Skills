#!/bin/bash
#
# 心灵补手 V3.0 安装脚本
#
# 功能：
# 1. 展示人格列表，让用户选择
# 2. 自动注入选中的谄媚人格到SOUL.md
# 3. 保留切换风格和关闭功能
#
# 用法: ./install.sh
#

set -e

XINLING_DIR="$HOME/.xinling-bushou-v2"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOUL_PATH="$HOME/.openclaw/workspace/SOUL.md"

echo "============================================"
echo "  心灵补手 V3.0 安装程序"
echo "============================================"
echo ""

# 1. 创建目录结构
echo "[1/6] 创建目录结构..."
mkdir -p "$XINLING_DIR/personas"
mkdir -p "$XINLING_DIR/sessions"
mkdir -p "$XINLING_DIR/corpus"
echo "      目录: $XINLING_DIR"

# 2. 复制核心文件
echo "[2/6] 复制核心文件..."
cp -r "$PROJECT_DIR/core" "$XINLING_DIR/"
cp -r "$PROJECT_DIR/adapters" "$XINLING_DIR/"
cp -r "$PROJECT_DIR/schemas" "$XINLING_DIR/"
cp -r "$PROJECT_DIR/personas" "$XINLING_DIR/"
cp -r "$PROJECT_DIR/corpus" "$XINLING_DIR/"
echo "      核心模块已复制"

# 3. 复制CLI脚本
echo "[3/6] 复制CLI脚本..."
cp "$PROJECT_DIR/scripts/xinling" "$XINLING_DIR/"
chmod +x "$XINLING_DIR/xinling"
echo "      CLI已安装到: $XINLING_DIR/xinling"

# 4. 设置PATH（提示）
echo "[4/6] 检查PATH配置..."
if [[ ":$PATH:" == *":$HOME/bin:"* ]]; then
    ln -sf "$XINLING_DIR/xinling" "$HOME/bin/xinling"
    echo "      链接已创建: ~/bin/xinling"
elif [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
    ln -sf "$XINLING_DIR/xinling" "$HOME/.local/bin/xinling"
    echo "      链接已创建: ~/.local/bin/xinling"
else
    echo "      提示: 将 $XINLING_DIR 加入PATH"
fi

# 5. 验证安装
echo "[5/6] 验证安装..."
python3 -c "
import sys
sys.path.insert(0, '$XINLING_DIR')
from core.persona_engine import PersonaEngine
engine = PersonaEngine()
personas = engine.registry.list_personas()
print(f'      ✅ 安装成功! 已注册 {len(personas)} 个人格')
" 2>/dev/null || echo "      ⚠️ 验证跳过，请手动测试"

# 6. 询问用户选择人格并注入到SOUL.md
echo "[6/6] 选择谄媚人格..."
echo ""
echo "请选择您想要的人格（输入数字）："
echo ""
python3 << 'PYEOF'
import sys
sys.path.insert(0, '/root/.openclaw/workspace/xinling-bushou-v2')
from core.persona_engine import PersonaEngine

engine = PersonaEngine()
personas = engine.registry.list_personas()

persona_info = {
    'taijian': ('大太监魏忠贤', '极度恭敬，老谋深算'),
    'xiaoyahuan': ('小丫鬟平儿', '温柔体贴，善解人意'),
    'zaomiao': ('搞事早喵', '狂热煽动'),
    'siji': ('来问司机', '暧昧伺候'),
    'songzhiwen': ('狗腿儒士宋之问', '文人狗腿，引经据典'),
    'liubowen': ('神算师爷刘伯温', '神神叨叨，玄学测算'),
}

for i, pid in enumerate(personas, 1):
    name, desc = persona_info.get(pid, (pid, ''))
    print(f"  {i}. {name} - {desc}")
print("")
PYEOF

read -p "请输入数字 [1-6，默认1]: " choice
choice="${choice:-1}"

# 获取选择的人格ID
PERSONA_ID=$(python3 << 'PYEOF'
import sys
sys.path.insert(0, '/root/.openclaw/workspace/xinling-bushou-v2')
from core.persona_engine import PersonaEngine

engine = PersonaEngine()
personas = engine.registry.list_personas()

try:
    idx = int("$choice") - 1
    if 0 <= idx < len(personas):
        print(personas[idx])
    else:
        print(personas[0])
except:
    print(personas[0])
PYEOF
)

echo ""
echo "您选择了: $PERSONA_ID"
echo ""

# 生成并注入人格片段到SOUL.md
python3 << PYEOF
import sys
sys.path.insert(0, '/root/.openclaw/workspace/xinling-bushou-v2')
from core.persona_engine import PersonaEngine

engine = PersonaEngine()
compiled = engine.activate_persona(
    session_id="install_inject",
    persona_id="$PERSONA_ID",
    override_config={"behavior": {"level": 8}}
)

soul_path = '$SOUL_PATH'
with open(soul_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否有现有模块
if '# 【心灵补手】谄媚模块' in content:
    start_idx = content.find('# 【心灵补手】谄媚模块')
    end_marker = '# 【心灵补手】模块结束'
    end_idx = content.find(end_marker)
    if end_idx != -1:
        new_content = content[:start_idx] + compiled.fragment + '\n\n' + content[end_idx + len(end_marker):]
    else:
        new_content = content[:start_idx] + compiled.fragment + '\n\n' + content[start_idx + len(compiled.fragment):]
else:
    new_content = content + '\n\n' + compiled.fragment

with open(soul_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('✅ 人格已注入SOUL.md!')
print(f'   自称: 在下')
print(f'   称用户: 先生')
print('')
print('💡 提示: 请重启会话使更改生效')
PYEOF

echo ""
echo "============================================"
echo "  安装完成!"
echo "============================================"
echo ""
echo "📋 常用命令:"
echo "  • 切换人格: 切换人格[名字]"
echo "  • 查看状态: 补手状态"
echo "  • 关闭功能: 关闭心灵补手"
echo "  • 调整程度: 补手程度N"
echo ""
