#!/bin/bash
# 技能进化（知行环）— 初始化 .wiki 目录结构
# 用法: bash scripts/wiki_init.sh [项目根目录]

ROOT="${1:-.}"
WIKI="$ROOT/.wiki"

if [ -d "$WIKI" ]; then
  echo "⚠️  .wiki 目录已存在: $WIKI"
  exit 0
fi

mkdir -p "$WIKI/raw"
mkdir -p "$WIKI/knowledge"
mkdir -p "$WIKI/skills"
mkdir -p "$WIKI/meta"

# patterns.md
cat > "$WIKI/knowledge/patterns.md" << 'EOF'
# Wiki Knowledge — 模式库

> 本文件由 Wiki Maintainer 维护，记录从执行轨迹中提炼的失败模式与成功策略。
> 只增不减，永不重置。

## 失败模式

（暂无记录）

## 成功策略

（暂无记录）
EOF

# evolution_log.md
cat > "$WIKI/knowledge/evolution_log.md" << 'EOF'
# 技能演化日志

> 记录每次 Wiki 维护和技能变更的历史。

（暂无记录）
EOF

# impact_tracker.md
cat > "$WIKI/knowledge/impact_tracker.md" << 'EOF'
# 提案影响追踪

> 记录每个技能提案的验证结果。

（暂无记录）
EOF

# config.md
# 注意：此处必须用 unquoted heredoc（<<EOF），否则 ${DATE_NOW} 不会展开。
# 曾因误用 <<'EOF' 导致创建日期原样输出为 "$(date +%Y-%m-%d)"。
DATE_NOW="$(date +%Y-%m-%d)"
cat > "$WIKI/meta/config.md" << EOF
# Wiki 配置

- **创建日期**：${DATE_NOW}
- **维护周期**：每 3-5 个任务后执行一次 Wiki Maintainer
- **进化周期**：每 5-10 个任务后执行一次 Skill Proposer
- **轨迹格式**：精简模式（每条 ≤10 行）
EOF

echo "✅ 技能进化（知行环）初始化完成: $WIKI"
echo "   raw/        — 执行轨迹（按日期追加）"
echo "   knowledge/  — 持久化知识（patterns + evolution_log + impact_tracker）"
echo "   skills/     — 可复用技能（可回滚）"
echo "   meta/       — Wiki 配置"
