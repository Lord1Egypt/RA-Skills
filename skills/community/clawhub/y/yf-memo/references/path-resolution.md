# 📍 技能路径解析指南

## 问题背景

OpenClaw技能可以安装在不同的位置：
1. **系统范围安装**：`~/.openclaw/skills/`
2. **临时/工作区安装**：`~/.openclaw/workspace/skills/`
3. **版本化目录**：技能可能包含版本号（如 `yf-memo-1.0.0`）

使用硬编码的绝对路径会导致在其他用户的机器上无法正常工作。

## 解决方案

### 方案1：动态查找技能目录（推荐）

**核心原理**：在运行时查找技能目录

```bash
# 查找技能目录
SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)

# 验证找到目录
if [ -z "$SKILL_DIR" ]; then
    echo "❌ yf-memo技能未找到"
    exit 1
fi

# 构造脚本路径
MEMO_SCRIPT="$SKILL_DIR/scripts/memo-helper.sh"
DAILY_SCRIPT="$SKILL_DIR/scripts/daily-summary.sh"

# 使用脚本
sh "$MEMO_SCRIPT" add "任务描述"
sh "$DAILY_SCRIPT"
```

### 方案2：使用技能环境变量

**安装时设置**（在 `install.sh` 中）：

```bash
# 在技能安装脚本中
cat >> ~/.bashrc << EOF
# yf-memo技能路径
export YFMEMO_SKILL_DIR="$HOME/.openclaw/workspace/skills/yf-memo"
export YFMEMO_SCRIPT="$YFMEMO_SKILL_DIR/scripts/memo-helper.sh"
export YFMEMO_DAILY_SCRIPT="$YFMEMO_SKILL_DIR/scripts/daily-summary.sh"
EOF
```

**使用时**：
```bash
if [ -n "$YFMEMO_SCRIPT" ]; then
    sh "$YFMEMO_SCRIPT" add "任务描述"
else
    # 回退到动态查找
    SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)
    MEMO_SCRIPT="$SKILL_DIR/scripts/memo-helper.sh"
    sh "$MEMO_SCRIPT" add "任务描述"
fi
```

### 方案3：符号链接到标准位置

**创建标准化路径**：

```bash
# 安装脚本中创建符号链接
mkdir -p ~/.local/bin
ln -sf "$(pwd)/scripts/memo-helper.sh" ~/.local/bin/yf-memo-helper
ln -sf "$(pwd)/scripts/daily-summary.sh" ~/.local/bin/yf-memo-daily

# 使用时
yf-memo-helper add "任务描述"
yf-memo-daily
```

## AI助手使用指南

### 在自然语言交互中

**最佳实践**：
```bash
# 1. 查找脚本
SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)

# 2. 检查是否存在
if [ ! -f "$SKILL_DIR/scripts/memo-helper.sh" ]; then
    echo "❌ yf-memo技能未正确安装"
    exit 1
fi

# 3. 执行操作
MEMO_SCRIPT="$SKILL_DIR/scripts/memo-helper.sh"
sh "$MEMO_SCRIPT" add "$TASK_DESCRIPTION"
```

### 定时任务配置

**正确的定时任务payload**：
```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name 'yf-memo' -type d 2>/dev/null | head -1) && DAILY_SCRIPT=\"$SKILL_DIR/scripts/daily-summary.sh\" && sh \"$DAILY_SCRIPT\""
  }
}
```

## 跨平台兼容性

### Windows支持
如果是跨平台技能，还需要考虑Windows路径：

```bash
# 检查平台
case "$(uname -s)" in
    Darwin|Linux)
        SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)
        ;;
    MINGW*|CYGWIN*|MSYS*)
        # Windows Git Bash/Cygwin
        SKILL_DIR=$(find /c/Users/$USER/.openclaw/skills /c/Users/$USER/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)
        ;;
    *)
        echo "❌ 不支持的操作系统"
        exit 1
        ;;
esac
```

## 测试工具

创建一个测试脚本验证路径查找：

```bash
#!/bin/bash
# test-path-resolution.sh

echo "=== yf-memo技能路径查找测试 ==="

# 方法1：动态查找
SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)

if [ -z "$SKILL_DIR" ]; then
    echo "❌ 错误：未找到yf-memo技能目录"
    exit 1
fi

echo "✅ 找到技能目录: $SKILL_DIR"

# 检查脚本
SCRIPTS=("memo-helper.sh" "daily-summary.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$SKILL_DIR/scripts/$script" ]; then
        echo "✅ $script 存在"
    else
        echo "❌ $script 不存在"
        exit 1
    fi
done

echo "✅ 所有脚本验证通过"
```

## 总结

**关键原则**：
1. **永不硬编码**：避免使用绝对路径
2. **运行时查找**：使用`find`命令动态定位技能
3. **优雅降级**：提供多种查找方法
4. **错误处理**：验证目录和脚本是否存在

这样设计的技能可以在任何OpenClaw安装环境中正常工作。