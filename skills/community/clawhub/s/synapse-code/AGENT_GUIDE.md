# Synapse Code Agent 使用指南

> **版本**: v1.1.0  
> **最后更新**: 2026-04-08  
> **适用对象**: 开发者、产品经理、设计师、数据分析师

---

## 📖 快速开始

### 30 秒上手

```bash
# 1. 初始化项目（首次使用）
/synapse-code init /path/to/your/project

# 2. 运行 Pipeline
/synapse-code run my-project "实现用户登录功能"

# 3. 查看进度
/synapse-code status my-project
```

---

## 🎯 六大场景使用指南

### 1. 💻 代码开发

**适用场景**: 功能开发、Bug 修复、系统设计、重构优化

#### 典型用法

```bash
# 开发新功能
/synapse-code run my-project "实现用户注册功能，需要支持邮箱验证"

# 修复 Bug
/synapse-code run my-project "修复登录页面点击提交后无响应的问题"

# 系统设计
/synapse-code run my-project "设计一个完整的电商系统，包括商品、订单、支付模块"

# 代码重构
/synapse-code run my-project "将用户模块重构为微服务架构"
```

#### 参与 Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| 需求分析师 | 分析功能需求 | 需求文档 |
| 架构师 | 设计技术方案 | 架构图 + 接口定义 |
| 开发工程师 | 编写代码 | 可运行代码 |
| 测试工程师 | 编写测试 | 测试报告 |
| 运维工程师 | 部署清单 | 部署文档 |

#### 输出示例

```
[1/5] 需求分析 → 需求文档.md
[2/5] 架构设计 → 技术方案.md + API 定义.json
[3/5] 代码开发 → src/user/login.py
[4/5] 质量检查 → 测试报告.md (2 passed)
[5/5] 部署准备 → 部署清单.md
```

---

### 2. 📝 文案写作

**适用场景**: 公众号文章、产品新闻稿、技术文档、商务邮件

#### 典型用法

```bash
# 公众号文章
/synapse-code run my-project "写一篇公众号文章，介绍 AI 编程技巧入门"

# 产品新闻稿
/synapse-code run my-project "写产品发布新闻稿，突出 AI 特性"

# 技术文档
/synapse-code run my-project "写 API 使用文档，包含示例代码"

# 商务邮件
/synapse-code run my-project "写一封给投资人的邮件，介绍项目进展"
```

#### 参与 Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| 选题策划 | 分析受众和热点 | 选题策划案 |
| 大纲策划 | 搭建文章结构 | 详细大纲 |
| 文案写作 | 撰写初稿 | 文案初稿 |
| 编辑 | 优化润色 | 终稿 |

#### 输出示例

```
[1/4] 选题策划 → 受众分析 + 选题方向
[2/4] 大纲策划 → 文章结构 (引言 - 正文 - 结尾)
[3/4] 文案写作 → 初稿 (2000 字)
[4/4] 编辑润色 → 终稿 (优化标题 + 金句)
```

---

### 3. 🎨 设计创作

**适用场景**: Logo 设计、UI 界面、海报设计、信息图表

#### 典型用法

```bash
# Logo 设计
/synapse-code run my-project "设计一个简约现代的 logo，科技公司"

# UI 设计
/synapse-code run my-project "设计一个 dashboard 界面，显示销售数据"

# 海报设计
/synapse-code run my-project "做个产品发布海报，科技感风格"

# 信息图表
/synapse-code run my-project "做个销售数据的信息图，展示 Q3 增长"
```

#### 参与 Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| 需求分析师 | 明确设计需求 | 设计需求文档 |
| 竞品调研 | 分析竞品设计 | 竞品分析报告 |
| 设计师 | 创作设计方案 | 设计稿 |
| 审核员 | 质量审核 | 审核报告 |

#### 输出示例

```
[1/4] 需求分析 → 风格定位 (简约、科技感)
[2/4] 竞品调研 → 竞品分析 (5 个参考案例)
[3/4] 设计创作 → 设计方案 (3 个版本)
[4/4] 设计审核 → 审核意见 + 优化建议
```

---

### 4. 📊 数据分析

**适用场景**: 销售分析、用户分析、竞品对比、数据可视化

#### 典型用法

```bash
# 销售分析
/synapse-code run my-project "分析 Q3 销售数据，找出增长点和下滑原因"

# 用户分析
/synapse-code run my-project "做用户行为分析，识别高价值用户特征"

# 竞品对比
/synapse-code run my-project "对比我们和竞品的市场份额和功能差异"

# 数据可视化
/synapse-code run my-project "做个销售数据 dashboard，实时显示关键指标"
```

#### 参与 Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| 数据工程师 | 收集清洗数据 | 干净数据集 |
| 分析师 | 统计分析 | 分析洞察 |
| 可视化专家 | 制作图表 | Dashboard/图表 |
| 报告撰写 | 撰写报告 | 完整分析报告 |

#### 输出示例

```
[1/4] 数据收集 → CSV/Excel 数据集
[2/4] 分析建模 → 关键发现 (3-5 个洞察)
[3/4] 可视化 → 图表 5 个 + Dashboard
[4/4] 报告撰写 → 分析报告 (含建议)
```

---

### 5. 🌐 翻译本地化

**适用场景**: 文档翻译、论文翻译、UI 本地化、多语言支持

#### 典型用法

```bash
# 文档翻译
/synapse-code run my-project "翻译技术文档到英文，保持专业术语准确"

# 论文翻译
/synapse-code run my-project "翻译这篇论文到中文，保留公式和图表"

# UI 本地化
/synapse-code run my-project "本地化 App 的 UI 文案到日文和韩文"
```

#### 参与 Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| 术语专家 | 整理术语表 | 双语术语表 |
| 翻译员 | 初稿翻译 | 翻译初稿 |
| 校对员 | 校对润色 | 校对报告 |
| 本地化专家 | 文化适配 | 本地化终稿 |

#### 输出示例

```
[1/4] 术语整理 → 术语表 (50+ 词条)
[2/4] 初稿翻译 → 翻译完成
[3/4] 校对润色 → 修改建议 (10 处)
[4/4] 本地化 → 文化适配检查通过
```

---

### 6. 📚 学习研究

**适用场景**: 技术调研、竞品分析、文献综述、研究报告

#### 典型用法

```bash
# 技术调研
/synapse-code run my-project "调研 RAG 技术的最新进展和应用场景"

# 竞品分析
/synapse-code run my-project "分析 AI 编程助手市场格局和主要玩家"

# 文献综述
/synapse-code run my-project "整理 Transformer 模型的研究现状"

# 研究报告
/synapse-code run my-project "写一份行业分析报告，预测 AI 趋势"
```

#### 参与 Agent

| Agent | 职责 | 输出 |
|-------|------|------|
| 文献研究员 | 搜集文献 | 文献综述 |
| 阅读分析师 | 深度阅读 | 分析报告 |
| 知识整理师 | 知识结构 | 知识图谱 |
| 报告撰写 | 撰写报告 | 研究报告 |

#### 输出示例

```
[1/4] 文献搜集 → 20 篇核心文献
[2/4] 阅读分析 → 关键发现整理
[3/4] 知识整理 → 知识图谱/结构图
[4/4] 报告撰写 → 研究报告 (5000 字)
```

---

## 🚀 三种模式选择

### 独立模式 (Standalone)

**无需配置，立即可用**

```bash
# 适合：快速原型、简单功能
/synapse-code run my-project "加个深色模式切换按钮"
```

**流程**: 直接分析需求 → 生成代码 → 完成

---

### 轻量模式 (Lite) ⭐ 推荐

**3-4 阶段简化流程**

```bash
# 适合：日常功能开发
/synapse-code run my-project "实现用户登录功能" --mode lite
```

**流程**: 需求分析 → 代码开发 → 质量检查

---

### 完整模式 (Full)

**6 阶段 SOP 企业级流程**

```bash
# 适合：大型项目、企业级应用
/synapse-code run my-project "开发完整的电商系统" --mode full
```

**流程**: 需求 → 架构 → 开发 → 集成 → 质检 → 部署

---

## 📋 命令参考

### 核心命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `init` | 项目初始化 | `/synapse-code init /path/to/project` |
| `run` | 运行 Pipeline | `/synapse-code run project "需求"` |
| `status` | 查看状态 | `/synapse-code status project` |
| `log` | 查看记录 | `/synapse-code log project` |
| `query` | 查询记忆 | `/synapse-code query project --task-type bugfix` |

### 常用参数

```bash
# 指定场景
--scenario writing | design | analytics | translation | research

# 指定模式
--mode standalone | lite | full

# 查询参数
--task-type bugfix | feature | refactor | debug
--limit 5
--contains "关键词"
```

---

## 💡 最佳实践

### 1. 需求描述要具体

❌ 不推荐：
```bash
/synapse-code run my-project "做个功能"
```

✅ 推荐：
```bash
/synapse-code run my-project "实现用户登录功能，使用 JWT 认证，支持邮箱和密码登录"
```

### 2. 选择合适模式

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 简单修改 | standalone | 快速交付 |
| 日常功能 | lite | 平衡效率和质量 |
| 大型项目 | full | 严格质量把控 |

### 3. 善用查询功能

```bash
# 查看历史 bug 修复记录
/synapse-code query my-project --task-type bugfix --limit 5

# 搜索特定功能实现
/synapse-code query my-project --contains "登录"
```

### 4. 定期检查状态

```bash
# 查看当前项目进度
/synapse-code status my-project
```

---

## 🔧 故障排查

详见 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 相关文档

- [TESTING.md](TESTING.md) - 测试指南
- [ROADMAP.md](ROADMAP.md) - 开发路线图
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查指南
