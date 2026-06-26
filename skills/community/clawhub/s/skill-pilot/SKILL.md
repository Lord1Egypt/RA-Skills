---
name: skill-pilot
version: 0.4.6
description: >
  Adaptive skill scheduling engine with environment-aware routing, user preferences, 
  and self-learning optimization. Use when: (1) auto-select best skill for task, 
  (2) need environment-aware configuration, (3) want to learn from execution history, 
  (4) need observability and performance insights.
required_env:
  - TAVILY_API_KEY (optional, for tavily-search skill)
  - BRAVE_API_KEY (optional, for brave-search skill)
  - HTTP_PROXY (optional, for proxy configuration)
optional_env:
  - OPENCLAW_GATEWAY_URL (custom gateway endpoint)
  - OPENCLAW_TOKEN (custom auth token)
security_notes:
  - Reads workspace files under ~/.openclaw/workspace/skills/
  - Writes config/cache/history to ~/.openclaw/workspace/skills/skill-pilot/
  - Probes network (DNS, latency, proxy detection) for environment optimization
  - Executes other skill scripts with input validation and timeout protection
  - Does NOT exfiltrate secrets; environment variables only passed to child processes
---

# SkillPilot - 智能技能调度引擎

> "自适应技能调度，零侵入优化，让每个人都能适配最优执行链路"

**版本**: 0.4.6  
**定位**: 通用技能调度优化框架  
**核心原则**: 零侵入 · 自适应 · 可观测 · 可移植  
**新增功能**: 双模式支持 + 安全修复 + 纯调度器重构

---

## 🎯 产品愿景

让 SkillPilot 成为**通用的技能调度优化框架**，帮助每个人根据自己的环境适配最优执行链路。

- **零侵入**: 不修改其他技能，即插即用
- **自适应**: 自动学习环境特点和用户偏好
- **可观测**: 调度决策透明，性能数据可视
- **可移植**: 配置可导出/导入，策略可分享
- **双模式**: 默认模式快速执行，全量模式对比优化

---

## 🚀 双模式说明

### 默认模式 (default) - 自动触发

**触发条件**: 输入内容**不包含**"全量"、"full"、"对比"等关键词

**特点**: 快速执行，使用默认工具，简洁输出

```
用户输入：伊朗最新战况
输出：直接显示结果 + 来源
```

**行为**:
- 使用预设的默认工具
- 单次执行，快速返回
- 直接输出查询结果和来源
- 记录执行表现用于后续优化

---

### 全量模式 (full) - 手动触发

**触发条件**: 输入内容**包含**"全量"、"full"、"对比"等关键词，或显式指定 `mode="full"`

**特点**: 对比优化，自动选择最优

```
用户输入：SkillPilot 全量模式 伊朗最新战况
输出：工具对比报告 + 最佳结果 + 自动优化
```

**行为**:
1. 使用该类别所有工具并行执行
2. 对比所有工具的结果
3. 评估结果质量（内容长度、信息密度等）
4. 自动将表现最好的工具设置为新的默认工具
5. 返回详细对比报告

**适用场景**:
- 重要任务，需要确保最佳结果
- 新环境，需要探索最优工具
- 定期运行，持续优化默认选择

---

### 模式对比

| 维度 | 默认模式 | 全量模式 |
|------|----------|----------|
| 触发 | 自动（无关键词） | 手动（含关键词） |
| 执行工具 | 1 个（默认） | N 个（所有同类） |
| 执行速度 | 快 | 较慢 |
| 输出 | 简洁（结果 + 来源） | 详细（对比报告） |
| 自动优化 | ❌ | ✅ |
| 适用场景 | 日常查询 | 重要任务/探索优化 |

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    SkillPilot Core                       │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 环境探测层   │  │ 用户偏好层   │  │ 历史学习层   │     │
│  │ Environment │  │ Preference  │  │  Learning   │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         └────────────────┼────────────────┘             │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │         自适应路由决策引擎 (核心)                 │   │
│  └─────────────────────────────────────────────────┘   │
│         │                │                │             │
│         ▼                ▼                ▼             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 技能注册中心 │  │ 降级处理器   │  │ 可观测性     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 核心模块

### 1. 环境探测 (`environment.py`)

**功能**: 自动检测网络特性和技能可用性

```python
from scripts.environment import EnvironmentProbe

probe = EnvironmentProbe()
result = probe.probe_all(['multi-search-engine', 'exa-web-search-free'])

# 输出:
# - 区域：cn
# - 代理：否
# - 推荐配置：cn-no-proxy
```

**预设配置模板**:
| 模板 | 适用场景 |
|------|----------|
| `cn-no-proxy` | 中国大陆无代理环境 |
| `cn-with-proxy` | 中国大陆有代理环境 |
| `global` | 海外环境 |

**使用**:
```bash
# 环境探测
python scripts/environment.py

# 查看推荐配置
python -c "from scripts.environment import EnvironmentProbe; p=EnvironmentProbe(); print(p.get_optimal_profile())"
```

---

### 2. 用户偏好 (`preference.py`)

**功能**: 让用户定义优化目标和约束条件

```python
from scripts.preference import UserPreference

pref = UserPreference()
pref.optimization_goal = 'speed'  # speed | cost | quality | balanced
pref.budget_limit = 'free'
pref.save()
```

**预设模式**:
| 模式 | 说明 |
|------|------|
| `speed` | 极速模式，优先选择响应最快的技能 |
| `cost` | 经济模式，优先选择免费/低成本技能 |
| `quality` | 质量优先，优先选择质量最高的技能 |
| `balanced` | 平衡模式，速度/成本/质量平衡 |
| `cn-optimized` | 国内优化，针对中国大陆网络环境 |
| `global-optimized` | 全球优化，针对海外网络环境 |

**使用**:
```bash
# 初始化配置 (选择模板)
python scripts/preference.py init balanced

# 查看当前配置
python scripts/preference.py show

# 查看模板
python scripts/preference.py template speed
```

---

### 3. 历史学习 (`learning.py`)

**功能**: 从历史执行记录中学习最优调度策略

```python
from scripts.learning import ExecutionHistory

history = ExecutionHistory()

# 分析某类别的最优技能
pattern = history.analyze_pattern('search')
print(f"最优技能：{pattern['best_skill']}")
print(f"成功率：{pattern['success_rate']*100:.1f}%")

# 学习所有模式
patterns = history.learn_patterns()
```

**学习维度**:
- 按类别 (search/fetch/summarize)
- 按环境 (cn/global)
- 按技能表现 (成功率/响应时间)

**使用**:
```bash
# 查看统计
python scripts/learning.py stats

# 分析某类别
python scripts/learning.py analyze search

# 运行学习算法
python scripts/learning.py learn

# 获取推荐
python scripts/learning.py recommend search
```

---

### 4. 可观测性 (`observability.py`)

**功能**: 提供调度看板、性能报告和诊断工具

```python
from scripts.observability import SchedulerDashboard

dashboard = SchedulerDashboard(history=history, environment=environment)

# 生成报告
report = dashboard.generate_report('text')
print(report)

# 保存报告
filepath = dashboard.save_report('markdown')
```

**报告内容**:
- 环境配置状态
- 技能表现统计
- 学习成果展示
- 优化建议

**使用**:
```bash
# 生成文本报告
python scripts/observability.py report

# 生成 Markdown 报告
python scripts/observability.py report markdown

# 保存报告
python scripts/observability.py save

# 查看技能健康状态
python scripts/observability.py health
```

---

## 🚀 快速开始

### 步骤 1: 环境探测 (1 分钟)

```bash
cd skills/skill-pilot
python scripts/environment.py
```

输出示例:
```
🔍 开始环境探测...
  → 探测网络环境...
  → 探测 3 个技能可用性...
  ✓ 推荐配置：cn-no-proxy
```

### 步骤 2: 设置用户偏好 (1 分钟)

```bash
# 使用平衡模式模板
python scripts/preference.py init balanced
```

### 步骤 3: 开始使用

SkillPilot 会自动:
- 根据环境选择最优配置
- 根据偏好调整路由权重
- 记录执行历史
- 学习优化模式

### 步骤 4: 查看报告 (可选)

```bash
# 每周查看一次
python scripts/observability.py report
```

---

## 📊 调度策略模板

### 中文搜索优化 (`strategies/search-cn.yaml`)

```yaml
name: search-cn-optimized
applicable_when:
  category: search
  query_contains_chinese: true

routing:
  primary:
    - skill: multi-search-engine
      engines: [baidu, sogou, wechat]
  fallback:
    - skill: exa-web-search-free
    - skill: tavily-search
```

### 技术搜索优化 (`strategies/search-technical.yaml`)

```yaml
name: search-technical-optimized
applicable_when:
  category: search
  is_technical_query: true

routing:
  primary:
    - skill: exa-web-search-free
      filters: [github, stackoverflow]
  fallback:
    - skill: multi-search-engine
```

### 反爬网站抓取 (`strategies/fetch-anti-bot.yaml`)

```yaml
name: fetch-anti-bot-optimized
applicable_when:
  category: fetch
  is_anti_bot_url: true

routing:
  primary:
    - skill: scrapling-fetch
  fallback:
    - skill: web_fetch
```

---

## 🔧 配置说明

### 用户偏好配置 (`config/preference.yaml`)

```yaml
# 优化目标
optimization_goal: balanced  # speed | cost | quality | balanced

# 预算限制
budget_limit: free  # free | low | medium | high

# 最低质量要求
quality_threshold: 0.7  # 0-1

# 超时时间
timeout_preference: 30  # 秒

# 区域偏好
region_preference: no-preference  # cn | global | no-preference

# 高级选项
advanced:
  allow_parallel: false
  max_fallback_depth: 3
  cache_enabled: true
  cache_ttl: 300
```

### 环境配置 (`profiles/*.yaml`)

见 `profiles/` 目录下的模板文件。

---

## 📈 可观测性

### 调度报告

```
┌─────────────────────────────────────────────────────────┐
│              SkillPilot 调度报告                         │
├─────────────────────────────────────────────────────────┤
│ 生成时间：2026-03-17 07:00:00                           │
├─────────────────────────────────────────────────────────┤
│ 【环境配置】                                            │
│   区域：cn                                              │
│   代理：否                                              │
│   推荐配置：cn-no-proxy                                 │
├─────────────────────────────────────────────────────────┤
│ 【技能表现】                                            │
│   追踪技能数：15                                        │
│   总调用次数：150                                       │
│   总体成功率：92.0%                                     │
├─────────────────────────────────────────────────────────┤
│ 【学习成果】                                            │
│   已学习模式：3 个                                       │
│   最后学习：2026-03-17 06:00                            │
├─────────────────────────────────────────────────────────┤
│ 【优化建议】                                            │
│   1. 执行环境探测以获取最优配置建议                     │
│   2. 调用样本较少，继续使用以积累学习数据               │
└─────────────────────────────────────────────────────────┘
```

### 技能健康状态

```
技能健康状态
==================================================
multi-search-engine   ████████░░ 85 分 (成功率 92%, 响应 1200ms)
exa-web-search-free   ███████░░░ 72 分 (成功率 88%, 响应 800ms)
scrapling-fetch       ████████░░ 88 分 (成功率 95%, 响应 2000ms)
```

---

## 📚 参考资料

### 核心文档
- `references/capability-taxonomy.md` - 能力分类体系
- `references/micro-routing-examples.md` - 微路由示例
- `references/reminder-policy.md` - 静默策略
- `references/resolution-order.md` - 解决顺序

### 新增文档
- `references/environment-probe.md` - 环境探测指南 (待创建)
- `references/strategy-guide.md` - 策略选择指南 (待创建)

---

## 🎯 核心价值

| 用户类型 | 获得价值 |
|---------|---------|
| **个人用户** | 自动适配自己的网络环境，无需手动配置 |
| **团队共享** | 分享最优调度策略，新人快速上手 |
| **技能开发者** | 了解技能实际表现，针对性优化 |
| **高级用户** | 深度定制调度逻辑，极致优化 |

---

## 📝 更新日志

### v0.2.0 (2026-03-17) - 自适应优化版
- ✅ 新增环境探测模块
- ✅ 新增用户偏好模块
- ✅ 新增历史学习模块
- ✅ 新增可观测性模块
- ✅ 新增调度策略模板
- ✅ 新增配置管理

### v0.1.0 (2026-03-17) - 基础版
- ✅ 核心框架实现
- ✅ 技能注册中心
- ✅ 路由决策器
- ✅ 降级处理器
- ✅ 执行引擎
- ✅ 基础指标收集

---

## 🤝 贡献指南

### 添加新策略模板

1. 在 `strategies/` 目录创建 YAML 文件
2. 定义适用条件和路由规则
3. 测试策略效果
4. 提交 PR

### 分享配置模板

1. 在 `profiles/` 目录创建环境配置
2. 说明适用场景
3. 分享社区

---

*作者：JARVIS*  
*许可：MIT*  
*最后更新：2026-03-17*
