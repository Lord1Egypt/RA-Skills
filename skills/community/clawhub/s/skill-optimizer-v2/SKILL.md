---
name: skill-optimizer
version: 1.0.0
description: ［何时使用］当用户需要评估技能质量时；当用户说"检查这个 skill"时；当创建或修改 skill 后需要验证时；当检测到"skill 优化""skill 评估""技能检查"等关键词时；当批量检查多个技能时
author: 燃冰 + 小蚂蚁
created: 2026-03-20
skill_type: 通用🟡
allowed-tools: [Bash, Read, Write, Exec]
related_skills: [skill-creator, skill-vetter]
tags: [skill 优化，技能评估，标准检查，质量保证，自动化]
---

# 技能优化师 🔍

**基于 SKILL-STANDARD-v3.md**

---

## 📋 功能描述

自动评估技能文件是否符合 SKILL-STANDARD-v3.md 规范，提供优化建议。

**适用场景：**
- 新技能创建后检查
- 技能修改后验证
- 批量技能质量评估
- 标准合规性检查

**边界条件：**
- 不自动修改技能文件（需用户确认）
- 基于最新标准（SKILL-STANDARD-v3.md）
- 提供建议而非强制执行

---

## 🎯 核心功能

### 功能 1：元数据检查

**检查项**：
- [ ] name 字段（必填，唯一标识）
- [ ] version 字段（可选，语义化版本）
- [ ] description 字段（必填，触发说明式）
- [ ] allowed-tools 字段（推荐，限制工具）
- [ ] skill_type 字段（选填，核心/通用/实验）
- [ ] author 字段（选填）
- [ ] created 字段（选填）
- [ ] related_skills 字段（可选）
- [ ] tags 字段（可选）

**触发词验证**：
- description 是否包含 `［何时使用］`
- 是否包含具体触发场景
- 是否包含关键词检测

---

### 功能 2：正文结构检查

**轻量级模板检查**（适用于 80% 技能）：
- [ ] 技能名称标题（# 技能名称）
- [ ] 功能描述章节
- [ ] 适用场景列表
- [ ] 边界条件说明
- [ ] 常见错误章节
- [ ] 使用示例章节
- [ ] 相关资源链接
- [ ] 故障排查章节

**完整级模板检查**（复杂技能）：
- [ ] 核心功能详解
- [ ] 渐进式披露结构
- [ ] references 目录
- [ ] 外部资源链接

---

### 功能 2.5：模板文件校验（MANDATORY）

**检查技能中提到的所有模板/参考文件是否实际存在：**

**校验规则**：
1. 提取 SKILL.md 中提到的所有模板文件（`templates/xxx.md`）
2. 检查文件是否实际存在于 skill 文件夹中
3. 如果提到但不存在 → **直接不通过**

**检查项**：
- [ ] 提取所有 `templates/` 目录引用
- [ ] 验证文件实际存在
- [ ] 检查 templates 目录是否为空（如果提到）

**🚨 不通过标准**：
```
─────────────────────────────────────────
• SKILL.md 中提到 templates/xxx.md 但文件不存在
• SKILL.md 中提到 references/xxx.md 但文件不存在
• SKILL.md 中提到 scripts/xxx.py 但文件不存在
• templates/目录被提到但为空
─────────────────────────────────────────
```

**校验脚本**：
```bash
#!/bin/bash
# 模板文件校验脚本

SKILL_DIR=$1
MISSING_FILES=()

# 提取所有提到的文件
for pattern in "templates/[\w-]+\.md" "references/[\w-]+\.md" "scripts/[\w-]+\.py"; do
  while IFS= read -r file; do
    if [ ! -f "$SKILL_DIR/$file" ]; then
      MISSING_FILES+=("$file")
    fi
  done < <(grep -oP "$pattern" "$SKILL_DIR/SKILL.md")
done

# 输出结果
if [ ${#MISSING_FILES[@]} -gt 0 ]; then
  echo "❌ 缺少文件："
  for f in "${MISSING_FILES[@]}"; do
    echo "   - $f"
  done
  exit 1
else
  echo "✅ 所有提到的文件都存在"
  exit 0
fi
```

**评分影响**：
- 模板文件缺失 → **直接判定为不合格（<60 分）**
- 模板文件完整 → 质量评分 +10 分

---

### 功能 3：质量评分

**评分维度**：

| 维度 | 权重 | 检查项 |
|------|------|--------|
| 元数据完整 | 20% | 必填字段、格式规范 |
| 触发清晰度 | 25% | description 质量、关键词覆盖 |
| 结构完整 | 25% | 必需章节、渐进披露 |
| 内容质量 | 20% | 示例、错误、故障排查 |
| 规范性 | 10% | 命名、格式、链接 |

**模板文件校验（一票否决）**：
- 模板文件完整 → 质量评分 +10 分
- 模板文件缺失 → **直接判定为不合格（<60 分）**

**评级标准**：
- ≥90 分：优秀（符合标准）
- ≥75 分：良好（少量优化）
- ≥60 分：合格（需要优化）
- <60 分：需改进（大量问题）
- **模板文件缺失 → 直接不通过**

---

### 功能 4：优化建议生成

**建议类型**：
1. **必须修复**（影响触发或使用）
2. **建议优化**（提升质量）
3. **可选改进**（锦上添花）

**建议格式**：
```markdown
### 🔴 必须修复

**问题**：description 缺少触发词

**当前**：`description: 身份认同习惯`

**建议**：`description: ［何时使用］当用户想培养习惯时；当用户说"我想成为 XX"时`

**原因**：没有触发词，技能无法被正确触发
```

---

## ⚠️ 常见错误

**错误 1：description 过于简略**
```
问题：
• 只写功能名称，没有触发场景
• 缺少关键词检测

解决：
✓ 使用［何时使用］格式
✓ 列出具体触发场景
✓ 包含关键词检测
```

**错误 2：缺少 allowed-tools**
```
问题：
• 未限制可用工具
• 可能存在安全隐患

解决：
✓ 明确指定 allowed-tools
✓ 遵循最小权限原则
```

**错误 3：缺少故障排查**
```
问题：
• 用户遇到问题无法解决
• 增加支持成本

解决：
✓ 添加故障排查章节
✓ 列出常见问题和解决方案
```

**错误 4：文件过长无渐进披露**
```
问题：
• SKILL.md 超过 300 行
• 启动时加载过多内容

解决：
✓ 创建 references 目录
✓ 主文件保持 100-150 行
✓ 使用链接引用外部资源
```

**错误 5：模板文件缺失**
```
问题：
• SKILL.md 中提到 templates/xxx.md 但文件不存在
• 提到参考文件但没有实际创建

解决：
✓ 创建所有提到的模板文件
✓ 或者删除对不存在文件的引用
✓ 使用模板校验脚本检查
```

---

## 🧪 使用示例

**输入**：
```bash
# 检查单个技能
python3 skill-optimizer/scripts/optimize-skill.py value-analyzer

# 批量检查
python3 skill-optimizer/scripts/optimize-skill.py --batch investment-framework-skill

# 检查并生成报告
python3 skill-optimizer/scripts/optimize-skill.py stock-picker --report
```

**预期输出**：
```
🔍 技能优化师：stock-picker
==================================================

📊 元数据检查
✅ name: stock-picker
✅ version: 2.0.0
✅ description: ［何时使用］当用户需要选股时...
⚠️  allowed-tools: 缺失

📋 正文结构检查
✅ 功能描述
✅ 常见错误
⚠️  故障排查：缺失

📈 质量评分
总分：78/100（良好）

💡 优化建议
🔴 必须修复：补充 allowed-tools
🟡 建议优化：添加故障排查章节
```

---

## 🔗 相关资源

- `references/checklist.md` - 完整检查清单
- `references/examples.md` - 评估示例
- `references/scoring.md` - 评分标准详解
- `scripts/optimize-skill.py` - 评估脚本

---

## 🔧 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 不触发 | description 是否包含触发词？ | 将关键词加入 description |
| 评分异常 | 标准文件存在吗？ | 检查 SKILL-STANDARD-v3.md |
| 脚本报错 | 有执行权限吗？ | `chmod +x scripts/*.py` |
| 批量失败 | 目录路径正确吗？ | 使用绝对路径 |
| 模板文件缺失 | SKILL.md 中提到的文件存在吗？ | 创建缺失的模板文件或删除引用 |

---

*基于 SKILL-STANDARD-v3.md*  
*最后更新：2026-03-20*
