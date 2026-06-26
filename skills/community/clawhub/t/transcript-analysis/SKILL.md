---
name: transcript-analysis
description: |
  从 Stock Analysis 或 QVeris API 抓取 earnings call transcript，进行主题信号挖掘，输出 evidence_ledger + theme_timeseries + summary_report。
  触发词：分析业绩会、earnings call 分析、transcript 信号、逐字稿分析、业绩会信号。
triggers:
  - 分析业绩会
  - earnings call 分析
  - transcript 信号
  - 逐字稿分析
  - 业绩会信号
  - Run transcript analysis
allowed-tools:
  - Read
  - Write
  - Bash
---

# Transcript Analysis Skill

从财报电话会逐字稿中挖掘主题信号，支持跨季度对比分析。

---

## 工作流程（Step 1-5）

### Step 1: 确认分析参数

**输入**：
- 股票代码（如 LMT, PM）
- 季度列表（如 2025Q4, 2025Q3）
- 数据源模式（web 免费 / api QVeris）

**输出**：参数配置确认

**✅ 检查点**：股票代码与季度格式正确

---

### Step 2: 🔍 参数确认检查点

**输入**：
- 用户提供的分析请求
- 当前日期（用于默认输出目录命名）

```
Transcript 分析配置：
- 股票代码：LMT
- 季度：2025Q4, 2025Q3, 2025Q2
- 数据源：web（免费）
- 输出目录：./transcript_LMT_20260527/

确认继续？[Y/n/调整]
```

**输出**：用户确认的配置参数

**✅ 检查点**：用户明确确认后执行

---

### Step 3: 执行分析脚本

**输入**：
- 确认后的配置参数
- transcript_analyzer.py脚本路径

```bash
# 默认 web 模式（免费）
python transcript_analyzer.py --symbol LMT --quarters 2025Q4 --mode web

# 多季度对比
python transcript_analyzer.py --symbol LMT --quarters 2025Q4,2025Q3,2025Q2 --mode web

# API fallback
python transcript_analyzer.py --symbol PM --quarters 2025Q4 --mode api
```

**输出**：
- 脚本执行状态
- 生成的CSV和Markdown文件

**✅ 检查点**：验证输出文件已生成

---

### Step 4: 边界条件处理

**输入**：
- 脚本执行结果
- 错误信息（如有）

| 场景 | 触发条件 | 处理动作 |
|------|---------|---------|
| 脚本不存在 | transcript_analyzer.py 未找到 | 提示检查路径或重新创建 |
| Stock Analysis 页面结构变化 | 解析失败 | 更新解析逻辑或切换 api 模式 |
| QVeris 配额不足 | API 返回 402 | 切换 web 模式或提示充值 |
| 无该季度 transcript | 网页 404 | 跳过该季度，继续其他 |
| 网络超时 | 请求 > 30s | 重试 3 次后切换数据源 |

**输出**：处理后的结果或错误提示

**✅ 检查点**：所有错误已妥善处理

---

### Step 5: 输出文件

**输入**：
- 脚本生成的输出文件

| 文件 | 说明 |
|------|------|
| `{symbol}_evidence_ledger.csv` | 核心：每条信号追踪到原文片段、说话人、分段、语境 |
| `{symbol}_theme_timeseries.csv` | 跨季度主题热度（提及次数 + 每千词提及率） |
| `{symbol}_summary_report.md` | 可读报告：主题排名 + 关键信号清单 |

**输出**：文件路径确认

**✅ 检查点**：用户确认输出文件位置

---

## 数据源优先级

| 优先级 | 数据源 | 成本 | 覆盖范围 |
|--------|--------|------|---------|
| 1 | Stock Analysis (stockanalysis.com) | 免费 | 多数美股 |
| 2 | QVeris API (Alpha Vantage) | 2 credits/次 | 更广覆盖 |

---

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--symbol` | ✅ | 股票代码，如 LMT, PM |
| `--quarters` | ✅ | 季度列表逗号分隔，如 2025Q4,2025Q3 |
| `--mode` | 否 | 数据源: web(默认免费) / api(QVeris) |
| `--output-dir` | 否 | 输出目录，默认当前目录 |

---

## 主题词库（24 个主题）

**消费/烟草（PM 等）**:
无烟转型 / 尼古丁袋 / 电子烟 / 定价 / 销量份额 / 利润率 / 监管税收 / 创新 / 汇率 / 股东回报 / 成本重组 / 业绩指引 / 区域表现 / 竞争格局

**军工/Defense（LMT 等）**:
积压订单 / 战斗机F-35 / 导弹弹药 / 太空业务 / 国防预算 / 多年期合同 / AI自主技术 / 金穹导弹防御 / 供应链产能 / 国际销售

---

## 输出目录惯例

```
./transcript_{symbol}_YYYYMMDD/
```

---

## 脚本位置

本技能捆绑 `transcript_analyzer.py` 脚本,安装后位于 skill 目录内。
