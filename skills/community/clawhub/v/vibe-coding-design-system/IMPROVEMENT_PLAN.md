# 📋 DESIGN.md 模板改进计划

## 🎯 改进目标

将所有 58 个模板提升到**专业级质量标准**，确保每个模板都包含：
- ✅ 完整的 9 个部分
- ✅ 详细的组件样式代码
- ✅ 可用的 React 组件模板
- ✅ 完整的 AI Agent 指令
- ✅ 详细的设计规范

---

## 📊 当前质量分析

### ✅ 完整版模板（5个）- 作为参考标准

| 模板 | 行数 | 大小 | 质量 |
|------|------|------|------|
| 小红书 | 928行 | 18KB | ⭐⭐⭐⭐⭐ |
| 飞书 | 800行 | 15KB | ⭐⭐⭐⭐⭐ |
| Linear | 745行 | 17KB | ⭐⭐⭐⭐⭐ |
| Stripe | 719行 | 16KB | ⭐⭐⭐⭐⭐ |
| 微博 | 607行 | 12KB | ⭐⭐⭐⭐⭐ |

**这些模板已经符合专业标准，可作为改进参考**

### ⭐ 简化版模板（6个）- 需要扩展

| 模板 | 行数 | 需要补充的内容 |
|------|------|---------------|
| Claude | 261行 | 详细组件代码、AI指令 |
| Supabase | 259行 | 完整样式代码、使用指南 |
| Vercel | 259行 | 组件模板、响应式设计 |
| 微信 | 256行 | 组件样式、布局系统 |
| 京东 | 79行 | **需要大幅扩展** |

### ❌ 不完整模板（47个）- 需要重建

这些模板需要从参考模板扩展，补充：
1. 完整的 9 个部分
2. 详细的组件样式代码（500+ 行CSS）
3. 可用的 React 组件模板
4. 完整的 AI Agent 指令
5. 响应式设计说明

---

## 🔧 改进方法

### 方式1：使用模板生成器（推荐）

```bash
cd ~/.openclaw/skills/pixel-perfect-design/scripts

# 编辑 design_data.json 配置文件
# 然后运行生成器
python3 template_generator.py
```

### 方式2：从参考模板扩展

1. **选择参考模板**：小红书/飞书/Linear/Stripe/微博
2. **复制参考模板**：`cp xiaohongshu.md new-template.md`
3. **替换关键信息**：
   - 主色调
   - 字体系统
   - 设计哲学
   - 品牌个性
4. **调整组件样式**：根据品牌特点调整按钮、卡片等

### 方式3：手动完善

按照以下顺序完善每个部分：

#### 第1部分：Visual Theme & Atmosphere（100+ 行）
```markdown
**Design Philosophy**: [品牌设计哲学]
**Mood**: [整体氛围]
**Density**: [信息密度]
**Design Language**: [设计语言]
**Target Audience**: [目标用户]
**Brand Personality**: [品牌个性]

### Design Principles
1. [原则1]
2. [原则2]
3. [原则3]

### Visual Metaphors
- [隐喻1]
- [隐喻2]
- [隐喻3]
```

#### 第2部分：Color Palette & Roles（80+ 行）
```markdown
### Primary Colors
[颜色表格，包含HEX、RGB]

### Semantic Colors
[语义色表格]

### Accessibility
[无障碍说明]
```

#### 第3部分：Typography Rules（100+ 行）
```markdown
### Font Families
[CSS代码]

### Type Scale
[字体层级表]

### Typography Usage
[使用说明]
```

#### 第4部分：Component Stylings（200+ 行）
```markdown
### Buttons
[完整CSS代码，包含所有状态]

### Inputs
[完整CSS代码]

### Cards
[完整CSS代码]

### Navigation
[导航样式]
```

#### 第5部分：Layout Principles（80+ 行）
```markdown
### Spacing Scale
[间距表格]

### Grid System
[网格说明]

### Breakpoints
[断点定义]

### Whitespace Philosophy
[留白哲学]
```

#### 第6部分：Depth & Elevation（60+ 行）
```markdown
### Shadow System
[阴影CSS]

### Z-Index Scale
[z-index表格]
```

#### 第7部分：Do's and Don'ts（80+ 行）
```markdown
### ✅ Do
[8-10条最佳实践]

### ❌ Don't
[8-10条反模式]

### Common Mistakes
[5个常见错误]
```

#### 第8部分：Responsive Behavior（60+ 行）
```markdown
### Breakpoints
[断点表格]

### Touch Targets
[触摸目标说明]

### Responsive Patterns
[响应式CSS代码]
```

#### 第9部分：Agent Prompt Guide（120+ 行）
```markdown
### Quick Reference
[CSS变量快速参考]

### Common Prompts
[3-5个常用提示词]

### Code Templates
[React组件模板]

### AI Agent Instructions
[10条AI指令]

### Component Checklist
[10项检查清单]
```

---

## 📝 改进清单

### 中文站点模板（12个）

#### 已完成 ✅
- [x] 小红书 - 928行，完整
- [x] 飞书 - 800行，完整
- [x] 微博 - 607行，完整
- [x] 微信 - 256行，需扩展到 600+ 行

#### 待改进 ⏳
- [ ] 抖音 - 从 98行扩展到 700+ 行
- [ ] 淘宝 - 从 42行扩展到 700+ 行
- [ ] 知乎 - 从 42行扩展到 700+ 行
- [ ] B站 - 从 42行扩展到 700+ 行
- [ ] 京东 - 从 79行扩展到 700+ 行
- [ ] 拼多多 - 从 29行扩展到 700+ 行
- [ ] 美团 - 从 29行扩展到 700+ 行
- [ ] 钉钉 - 从 29行扩展到 700+ 行

### 国际站点模板（46个）

#### 已完成 ✅
- [x] Linear - 745行，完整
- [x] Stripe - 719行，完整
- [x] Notion - 674行，完整
- [x] Supabase - 259行，需扩展
- [x] Vercel - 259行，需扩展
- [x] Claude - 261行，需扩展

#### 待改进 ⏳（剩余40个）
所有其他模板都需要从 29-49行扩展到 700+ 行

---

## 🎯 改进优先级

### P0 - 立即改进（顶级中文站点）
1. 抖音 - 短视频标杆
2. 淘宝 - 电商标杆
3. 知乎 - 知识社区标杆
4. 微信 - 超级应用标杆（扩展）

### P1 - 高优先级（顶级国际站点）
1. Apple - 设计系统标杆
2. Airbnb - 旅行平台标杆
3. Spotify - 音乐平台标杆
4. Tesla - 电动汽车标杆
5. Figma - 设计工具标杆

### P2 - 中优先级（其他重要站点）
- 其他 Developer Tools
- Infrastructure 站点
- Fintech 站点

### P3 - 低优先级（补充站点）
- 其他 Car Brands
- 其他 Enterprise 站点

---

## 💡 快速改进脚本

创建一个批量改进脚本：

```bash
#!/bin/bash
# improve_templates.sh

# 从参考模板扩展
TEMPLATE_DIR=~/.openclaw/skills/pixel-perfect-design/templates
REFERENCE=$TEMPLATE_DIR/xiaohongshu.md

# 待改进模板列表
IMPROVE_LIST=(
  "douyin.md"
  "taobao.md"
  "zhihu.md"
  "bilibili.md"
)

for template in "${IMPROVE_LIST[@]}"; do
  echo "改进 $template ..."
  # 1. 备份原文件
  cp $TEMPLATE_DIR/$template $TEMPLATE_DIR/${template}.bak
  
  # 2. 从参考模板创建新文件
  # cp $REFERENCE $TEMPLATE_DIR/$template
  
  # 3. 手动编辑替换关键信息
  # vim $TEMPLATE_DIR/$template
  
  echo "完成 $template 改进"
done
```

---

## 📦 最终目标

### 行数目标
- **完整版模板**：每个 700-1000 行
- **简化版模板**：扩展到 600+ 行
- **不完整模板**：重建到 700+ 行

### 质量目标
- ✅ 所有模板都包含完整 9 部分
- ✅ 所有模板都有详细组件代码
- ✅ 所有模板都有 React 组件模板
- ✅ 所有模板都有完整 AI 指令
- ✅ 所有模板都支持中英文

### 最终成果
- **总行数**: 40,000+ 行
- **总大小**: 1MB+
- **模板数量**: 58 个专业级模板

---

## 🚀 下一步行动

1. **立即**：使用模板生成器创建 P0 优先级模板
2. **短期**：改进所有中文站点模板（12个）
3. **中期**：改进所有国际顶级站点（15个）
4. **长期**：完成剩余模板改进（31个）

---

**这个改进计划将确保所有58个模板都达到专业级质量标准！** 🚀
