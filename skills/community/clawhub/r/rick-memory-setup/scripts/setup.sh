#!/bin/bash
# Rick Memory Setup - 安装脚本

WORKSPACE=~/.openclaw/workspace
SKILL_DIR=~/.openclaw/skills/rick-memory-setup

echo "============================================================"
echo "Rick Memory Setup - 结构化记忆系统安装"
echo "============================================================"
echo ""

# 1. 复制模板文件
echo "[1/4] 复制模板文件..."
cp -n "$SKILL_DIR/templates/AGENTS.md" "$WORKSPACE/AGENTS.md" 2>/dev/null && echo "  ✅ AGENTS.md" || echo "  ⚠️ AGENTS.md 已存在，跳过"
cp -n "$SKILL_DIR/templates/HEARTBEAT.md" "$WORKSPACE/HEARTBEAT.md" 2>/dev/null && echo "  ✅ HEARTBEAT.md" || echo "  ⚠️ HEARTBEAT.md 已存在，跳过"
cp -n "$SKILL_DIR/templates/USER.md" "$WORKSPACE/USER.md" 2>/dev/null && echo "  ✅ USER.md" || echo "  ⚠️ USER.md 已存在，跳过"
echo ""

# 2. 创建memory目录
echo "[2/4] 创建memory目录..."
mkdir -p "$WORKSPACE/memory"
echo "  ✅ $WORKSPACE/memory/"
echo ""

# 3. 创建MEMORY.md模板
echo "[3/4] 创建MEMORY.md模板..."
if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
    cat > "$WORKSPACE/MEMORY.md" << 'EOF'
# MEMORY.md - 项目长期记忆

> 结构化分层记忆系统
> - 核心配置：永久规则、用户偏好、项目定位
> - 按项目分类：每个项目独立章节，包含定位、状态、关键结论
> - 时间线：最新进展放在项目章节内，历史沉淀保留关键结论

---

## 🎯 核心配置

### 用户信息
- **用户名**: 
- **项目**: 
- **偏好**: 

### 记忆规则（自动执行）
1. **会话重启后**：必须先用 `memory_search` 搜索相关内容，再回答问题
2. **关键决策/结论**：必须写入 MEMORY.md 或当日 `memory/YYYY-MM-DD.md`
3. **日常进展**：写入当日日志，每周整理提炼到 MEMORY.md
4. **过期信息**：定期清理过时结论，保留最新决策

---

## 📊 项目一：XXX

### 🎯 项目定位
（描述项目目标和定位）

### 🏷️ 当前状态
- **阶段**: 
- **完成度**: 

### 🔑 关键结论（沉淀）

#### 1. XXX教训
- **[YYYY-MM-DD] 问题**: （来源：XXX）
- **[YYYY-MM-DD] 解决**: （来源：XXX）

---

## 🔄 记忆治理

### 最后整理时间
YYYY-MM-DD

---

*本文件遵循 OpenClaw 原生三层架构 + 结构化项目分类 + Heartbeat 自动化维护*
*最后更新：YYYY-MM-DD*
EOF
    echo "  ✅ MEMORY.md 模板已创建"
else
    echo "  ⚠️ MEMORY.md 已存在，跳过"
fi
echo ""

# 4. 创建TOOLS.md模板
echo "[4/4] 创建TOOLS.md模板..."
if [ ! -f "$WORKSPACE/TOOLS.md" ]; then
    cat > "$WORKSPACE/TOOLS.md" << 'EOF'
# TOOLS.md - 本地配置

此文件存储环境特定的配置信息。

## API Keys
- Tushare: （填入你的token）
- 其他API: 

## 路径配置
- 项目路径: 
- 数据路径: 

## 设备信息
- 设备名称: 
- 操作系统: 
EOF
    echo "  ✅ TOOLS.md 模板已创建"
else
    echo "  ⚠️ TOOLS.md 已存在，跳过"
fi
echo ""

echo "============================================================"
echo "✅ 安装完成！"
echo ""
echo "下一步操作："
echo "  1. 编辑 USER.md 填写你的个人信息"
echo "  2. 编辑 MEMORY.md 添加你的项目和偏好"
echo "  3. 编辑 TOOLS.md 添加环境配置"
echo "============================================================"
