#!/bin/bash

echo "========================================"
echo "  Vibe Coding Rules - 安装程序"
echo "  Vibe Coding Rules - Installer"
echo "  Version 2.5.0"
echo "========================================"
echo ""

# === 检测 IDE/Agent 类型 ===
SKILL_DIR=""
AGENT_TYPE="unknown"

# 检测 CodeBuddy
if [ -d "$HOME/.codebuddy/skills" ]; then
    SKILL_DIR="$HOME/.codebuddy/skills"
    AGENT_TYPE="codebuddy"
    echo "[DETECT] CodeBuddy environment | CodeBuddy 环境"
fi

# 检测 Cursor
if [ -d ".cursor/rules" ] && [ "$AGENT_TYPE" = "unknown" ]; then
    AGENT_TYPE="cursor"
    echo "[DETECT] Cursor environment | Cursor 环境"
fi

# 默认：通用
if [ "$AGENT_TYPE" = "unknown" ]; then
    echo "[DETECT] No known IDE detected, using generic mode (.ai-pipeline)"
    echo "        未检测到已知 IDE，使用通用模式"
    AGENT_TYPE="generic"
fi

echo "[TARGET] $AGENT_TYPE"
echo ""

# === 安装 Skill ===
if [ "$AGENT_TYPE" = "codebuddy" ]; then
    echo "[INSTALL] Copying skills to CodeBuddy dir... | 复制到 CodeBuddy 目录..."
    
    cp -r coding-principles "$SKILL_DIR/" && echo "  coding-principles       [OK]"
    cp -r safe-terminal-executor "$SKILL_DIR/" && echo "  safe-terminal-executor [OK]"
    cp -r self-check "$SKILL_DIR/" && echo "  self-check             [OK]"
    cp -r web-testing "$SKILL_DIR/" && echo "  web-testing            [OK]"
    cp -r changelog "$SKILL_DIR/" && echo "  changelog              [OK]"
fi

if [ "$AGENT_TYPE" = "generic" ]; then
    echo "[INSTALL] Creating .ai-pipeline dir... | 创建 .ai-pipeline 目录..."
    mkdir -p .ai-pipeline
    
    cp coding-principles/.ai-pipeline/prompt.md .ai-pipeline/01-coding-principles.md
    cp safe-terminal-executor/.ai-pipeline/prompt.md .ai-pipeline/02-safe-terminal-executor.md
    cp self-check/.ai-pipeline/prompt.md .ai-pipeline/03-self-check.md
    cp web-testing/.ai-pipeline/prompt.md .ai-pipeline/04-web-testing.md
    cp changelog/.ai-pipeline/prompt.md .ai-pipeline/05-changelog.md
    cp .ai-pipeline/README.md .ai-pipeline/README.md
    
    echo "  .ai-pipeline/ created [OK] | 创建完成"
fi

echo ""
echo "========================================"
echo "  安装完成！ / Installation Complete!"
echo "========================================"
echo ""
echo "Next steps | 下一步："
echo "  1. Edit pipeline.json with project params"
echo "     编辑 pipeline.json 填入项目参数"
echo "  2. Install optional deps (if needed)："
echo "     npm install playwright"
echo "     npx playwright install chromium"
echo "  3. Start coding, pipeline auto-activates | 开始编程，流水线自动生效"
