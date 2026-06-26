---
name: skillsmith-jojo
description: |
  Skillsmith-JOJO — 完美主义技能工坊，JOJO's Workshop 出品。
  专为完美主义者设计的 AI 技能开发工具，提供从零到发布的完整工作流。

  使用场景：
  - 用户说"创建一个新技能"、"帮我做一个技能"
  - 用户说"优化这个技能"、"改进 SKILL.md"
  - 用户说"审计技能"、"检查技能质量"
  - 用户说"打包技能"、"发布技能"
  - 用户说"测试技能"、"验证技能"
  - 用户说"分析技能性能"、"Token 优化"
  - 用户说"检查技能安全"、"安全审查"

  对比原版 Skill Creator 的核心升级：
  (1) 5 套实战模板，减少 50% 创建时间
  (2) 内置测试框架，保证技能质量
  (3) 前置安全检查，杜绝危险代码
  (4) Token 性能分析，优化上下文效率
  (5) 完整开发工作流，从零到发布一气呵成
metadata:
  openclaw:
    emoji: "⚒️"
    requires:
      bins:
        - python3
---

# Skillsmith-JOJO ⚒️
### 完美主义技能工坊 · JOJO's Workshop 出品

> *Forging Perfection, One Skill at a Time*

---

## 什么是 Skillsmith-JOJO？

Skillsmith-JOJO 是一套完整的 AI 技能开发工作流，专为追求完美的开发者设计。

**不是**简单的代码仓库，而是经过实战验证的**技能开发方法论**。

---

## 核心优势

| 优势 | 说明 |
|------|------|
| ⚡ **效率提升** | 5套模板减少50%创建时间 |
| 🛡️ **安全前置** | 发布前安全检查，杜绝危险代码 |
| 📊 **性能优化** | Token分析，确保上下文高效 |
| ✅ **质量保证** | 测试框架，每个技能可验证 |
| 📚 **最佳实践** | 多年经验总结，开箱即用 |

---

## 快速开始

### 创建新技能（7步工作流）

```
Step 1  选择模板   →  从 templates/ 选择最接近的模板
Step 2  初始化     →  复制模板，修改 name 和 description
Step 3  实现功能   →  编写 scripts/ 和 references/
Step 4  测试验证   →  python skill-test.py <技能路径>
Step 5  安全检查   →  python security-check.py <技能路径>
Step 6  性能分析   →  python token-analyzer.py <技能路径>
Step 7  打包发布   →  clawhub publish <技能路径>
```

---

## 模板库（5套实战模板）

| 模板 | 适用场景 | 复杂度 |
|------|---------|--------|
| 📡 **API 集成** | 调用外部 API、数据获取、OAuth | 中 |
| 📁 **文件处理** | 格式转换、批量处理、PDF/Excel | 高 |
| 🤖 **自动化工作流** | 多步骤自动化、定时任务、监控 | 中 |
| 📊 **数据查询** | SQL 查询、API 数据分析、可视化 | 低 |
| 📦 **Git 助手** | 智能提交、分支管理、代码审查 | 中 |

每个模板包含：
- ✅ 完整 SKILL.md 结构
- ✅ 核心脚本代码
- ✅ 参考文档
- ✅ 使用示例

---

## 工具集（3个核心工具）

### 1️⃣ skill-test.py — 技能测试框架

```bash
# 基础测试
python skill-test.py <技能路径>

# 快速测试（跳过脚本执行）
python skill-test.py <技能路径> --quick

# 输出JSON报告
python skill-test.py <技能路径> --output report.json
```

**检查项目：**
- SKILL.md 格式和必填字段
- YAML frontmatter 完整性
- 脚本语法正确性
- 目录结构规范性

### 2️⃣ security-check.py — 安全检查

```bash
# 标准检查
python security-check.py <技能路径>

# 严格模式（中风险也失败）
python security-check.py <技能路径> --strict

# 输出JSON报告
python security-check.py <技能路径> --output security.json
```

**检测危险模式：**

| 风险级别 | 模式 | 处理 |
|---------|------|------|
| 🚨 EXTREME | curl到未知URL、eval/exec、sudo | 立即拒绝 |
| 🔴 HIGH | 访问.ssh/.aws、读取个人记忆文件 | 人工审查 |
| 🟡 MEDIUM | 安装未知包、IP直连 | 谨慎安装 |
| 🟢 LOW | 删除文件、修改系统 | 基础审查 |

### 3️⃣ token-analyzer.py — Token 性能分析

```bash
# 分析技能
python token-analyzer.py <技能路径>

# 输出JSON报告
python token-analyzer.py <技能路径> --output perf.json
```

**评级标准：**

| 评级 | Token数 | 说明 |
|------|--------|------|
| A 优秀 | ≤ 1500 | 精简高效 |
| B 良好 | ≤ 3000 | 可接受 |
| C 需优化 | ≤ 5000 | 建议拆分 |
| D 严重臃肿 | > 5000 | 必须优化 |

---

## 设计原则

### 1. 精简至上

SKILL.md 只写 AI 不知道的内容：
- ❌ 不写 Python 基础语法
- ❌ 不写 Git 基础命令
- ✅ 只写领域特定知识

### 2. 渐进式披露

| 层级 | 内容 | 加载时机 |
|------|------|---------|
| Frontmatter | name + description | 始终在上下文 |
| SKILL.md Body | 核心工作流 | 触发时加载 |
| references/ | 详细文档 | 按需加载 |
| scripts/ | 可执行代码 | 执行时加载 |

### 3. 安全前置

**发布前必须通过：**
1. `skill-test.py` — 结构完整性
2. `security-check.py` — 安全审查
3. `token-analyzer.py` — 性能达标

### 4. 完美主义

不交半成品：
- 每个技能都要有完整文档
- 每个脚本都要有错误处理
- 每个功能都要经过测试

---

## 目录结构规范

```
skill-name/
├── SKILL.md              # 必需：技能定义
├── scripts/              # 可选：可执行脚本
│   ├── main.py          # 主脚本
│   └── utils.py         # 工具函数
├── references/          # 可选：参考文档
│   ├── api.md          # API 文档
│   └── examples.md     # 示例
└── assets/              # 可选：模板文件
    └── template.xlsx    # Excel 模板
```

---

## 常见问题

### Q: 如何选择模板？
A: 根据你的技能类型选择最接近的模板，然后在此基础上修改。

### Q: 必须使用所有工具吗？
A: 建议全部通过。如有特殊情况，至少通过安全检查。

### Q: Token 数超标怎么办？
A: 将详细内容移至 references/ 目录，SKILL.md 只保留核心流程。

### Q: 如何发布技能？
A: 查看 `references/publishing.md` 获取详细指南。

---

## 引用文件

| 文件 | 说明 |
|------|------|
| [best-practices.md](references/best-practices.md) | 技能设计最佳实践 |
| [publishing.md](references/publishing.md) | ClawHub 发布指南 |

---

## 关于 JOJO's Workshop

**完美主义者的技能工坊**

我们相信：
- 好技能是打磨出来的，不是堆出来的
- 每个细节都值得认真对待
- 工具应该为人服务，而不是相反

---

*Skillsmith-JOJO · JOJO's Workshop · 完美主义者的技能工坊*
*Forging Perfection, One Skill at a Time*
