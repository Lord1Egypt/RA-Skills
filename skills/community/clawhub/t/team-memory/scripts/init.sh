#!/usr/bin/env bash

# Team Memory v2.4.0 - 初始化脚本
# 用法: bash scripts/init.sh

set -euo pipefail

SKILL_DIR="${TEAM_MEMORY_DIR:-$HOME/.config/opencode/skills/team-memory}"

echo "Team Memory v2.4.0 初始化"
echo "目录: $SKILL_DIR"

mkdir -p "$SKILL_DIR/data/members"
mkdir -p "$SKILL_DIR/data/upward"
mkdir -p "$SKILL_DIR/data/company"
mkdir -p "$SKILL_DIR/data/insights"
mkdir -p "$SKILL_DIR/data/templates"
mkdir -p "$SKILL_DIR/data/archive"
mkdir -p "$SKILL_DIR/data/.backup"
mkdir -p "$SKILL_DIR/data/manager-journal/tracker/pending"
mkdir -p "$SKILL_DIR/data/manager-journal/tracker/completed"
mkdir -p "$SKILL_DIR/data/manager-journal/tracker/summary"

touch "$SKILL_DIR/data/members/.gitkeep"
touch "$SKILL_DIR/data/upward/.gitkeep"
touch "$SKILL_DIR/data/company/.gitkeep"
touch "$SKILL_DIR/data/insights/.gitkeep"
touch "$SKILL_DIR/data/templates/.gitkeep"
touch "$SKILL_DIR/data/archive/.gitkeep"

if [ ! -f "$SKILL_DIR/skill-config.yaml" ]; then
  if [ -f "$SKILL_DIR/skill-config.example.yaml" ]; then
    cp "$SKILL_DIR/skill-config.example.yaml" "$SKILL_DIR/skill-config.yaml"
    echo "已从 skill-config.example.yaml 创建 skill-config.yaml"
  else
    echo "未找到 skill-config.yaml。请复制 skill-config.example.yaml 后配置成员。"
  fi
fi

if [ ! -f "$SKILL_DIR/data/upward/expectations.md" ]; then
  cat > "$SKILL_DIR/data/upward/expectations.md" <<'EOF'
# 上级期望与向上管理

## 当前期望

### 本季度
- [ ] 

## 向上沟通记录

### YYYY-MM-DD
**议题**: 
**上级反馈**: 
**我的行动**: 
**关联成员**: 
EOF
fi

if [ ! -f "$SKILL_DIR/data/company/strategy.md" ]; then
  cat > "$SKILL_DIR/data/company/strategy.md" <<'EOF'
# 公司战略与业务方向

## 年度战略

### YYYY
**战略主题**: 

## 业务变化

### YYYY-MM
**变化**: 
**影响**: 
**团队应对**: 
EOF
fi

echo "初始化完成。下一步：编辑 skill-config.yaml，或运行 scripts/new-member.sh 创建成员。"
