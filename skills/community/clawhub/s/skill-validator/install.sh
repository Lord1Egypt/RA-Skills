#!/bin/bash

# 技能检验工具安装脚本

set -e

echo "🔍 安装技能检验工具..."
echo "================================"

# 检查依赖
echo "📦 检查系统依赖..."
for cmd in bash jq find grep sed; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ 缺少依赖: $cmd"
        echo "   请安装: sudo apt-get install $cmd  # Debian/Ubuntu"
        exit 1
    fi
done

echo "✅ 所有依赖已安装"

# 创建配置目录
CONFIG_DIR="$HOME/.openclaw/skill-validator"
RULES_DIR="$CONFIG_DIR/rules"
LOG_DIR="$CONFIG_DIR/logs"

echo "📁 创建配置目录..."
mkdir -p "$RULES_DIR" "$LOG_DIR"

# 复制脚本文件
echo "📋 安装脚本文件..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 使脚本可执行
chmod +x "$SCRIPT_DIR/skill-validator.sh"

# 创建符号链接（可选）
if [ "$1" = "--link" ]; then
    echo "🔗 创建全局符号链接..."
    sudo ln -sf "$SCRIPT_DIR/skill-validator.sh" /usr/local/bin/skill-validator 2>/dev/null || true
    sudo ln -sf "$SCRIPT_DIR/skill-validator.sh" /usr/local/bin/validate-skill 2>/dev/null || true
fi

# 创建验证规则
echo "📝 创建验证规则..."

# 基础规则
cat > "$RULES_DIR/basic-rules.json" << 'EOF'
{
  "required_files": [
    "SKILL.md",
    "install.sh"
  ],
  "recommended_files": [
    "README.md",
    "LICENSE",
    "package.json"
  ],
  "file_permissions": {
    "scripts": "755",
    "configs": "644"
  },
  "skill_metadata": {
    "required_fields": ["name", "description", "author", "version"],
    "openclaw_fields": ["emoji", "requires"]
  },
  "max_sizes": {
    "skill_dir": 104857600,
    "individual_file": 10485760
  }
}
EOF

# 安全检查规则
cat > "$RULES_DIR/security-rules.json" << 'EOF'
{
  "dangerous_patterns": [
    "rm -rf /",
    "chmod 777",
    "password.*=",
    "api_key.*=",
    "secret.*=",
    "curl.*bash",
    "wget.*|.*bash"
  ],
  "safe_directories": [
    "/tmp/",
    "$HOME/.openclaw/",
    "/var/tmp/"
  ],
  "forbidden_commands": [
    "format",
    "dd if=",
    "mkfs",
    "fdisk"
  ],
  "network_checks": {
    "allow_localhost": true,
    "require_https": true,
    "max_redirects": 3
  }
}
EOF

# 创建默认配置
echo "⚙️ 创建默认配置..."
cat > "$CONFIG_DIR/config.json" << 'EOF'
{
  "version": "1.0.0",
  "validation": {
    "check_metadata": true,
    "check_security": true,
    "check_dependencies": true,
    "check_permissions": true,
    "check_syntax": true,
    "max_errors": 10,
    "strict_mode": false
  },
  "output": {
    "format": "human",
    "color": true,
    "verbose": false,
    "report_file": "validation-report.json"
  },
  "rules": {
    "basic": "rules/basic-rules.json",
    "security": "rules/security-rules.json"
  }
}
EOF

# 创建示例技能用于测试
echo "📚 创建示例技能..."
EXAMPLE_DIR="$CONFIG_DIR/examples/valid-skill"
mkdir -p "$EXAMPLE_DIR"

cat > "$EXAMPLE_DIR/SKILL.md" << 'EOF'
---
name: example-skill
description: "示例技能用于测试验证工具"
author: "测试用户"
version: "1.0.0"
license: "MIT"
metadata:
  openclaw:
    emoji: "✅"
    requires:
      bins: ["bash"]
---
# 示例技能

这是一个有效的技能示例。
EOF

cat > "$EXAMPLE_DIR/install.sh" << 'EOF'
#!/bin/bash
echo "安装示例技能..."
echo "✅ 安装完成"
EOF

chmod +x "$EXAMPLE_DIR/install.sh"

echo ""
echo "✅ 安装完成!"
echo ""
echo "📋 安装摘要:"
echo "  - 配置目录: $CONFIG_DIR"
echo "  - 规则目录: $RULES_DIR"
echo "  - 日志目录: $LOG_DIR"
echo "  - 示例技能: $EXAMPLE_DIR"
echo ""
echo "🚀 使用方法:"
echo "  1. 验证单个技能: ./skill-validator.sh /path/to/skill"
echo "  2. 验证目录下所有技能: ./skill-validator.sh --all /skills/dir"
echo "  3. 生成详细报告: ./skill-validator.sh --report /path/to/skill"
echo ""
echo "📚 详细文档请查看 SKILL.md"
echo "================================"