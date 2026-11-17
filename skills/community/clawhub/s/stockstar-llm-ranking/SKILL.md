---
name: StockStar LLM Ranking - 证券之星大模型调用排行榜
description: >
  查询大模型调用排行榜数据，数据来源证券之星科技频道（tech.stockstar.com），
  提供日榜和周榜两个周期，覆盖各主流大模型的调用量（Tokens）排名、
  厂商（模型发布方）、变动百分比、涨跌方向和新上榜标记。
  支持查看完整榜单、前 N 名、按模型/厂商搜索定位。
  触发词：调用排行榜、排行榜、日榜、周榜、大模型、模型调用量、
  Tokens、调用量、模型热度、厂商、模型发布方、DeepSeek、GPT、
  Claude、Gemini、Kimi、GLM、MiniMax、OpenRouter、模型排名、llm ranking
version: 1.0.0
---

# 证券之星 大模型调用排行榜 Skill

```bash
PYTHON=python3.12
RANK=scripts/cli.py
```

通过自然语言查询证券之星科技频道的大模型调用排行榜，榜单原始数据来自 OpenRouter，提供日榜、周榜两个周期。

## 适用场景

用户提到以下内容时触发本 Skill：

- **查看排行榜**："大模型调用排行榜"、"今天哪些模型调用最多"、"本周模型调用量排名"
- **查看日榜/周榜**："今日榜单"、"本周榜单"、"周榜前五"
- **查看前 N 名**："排行榜前10"、"TOP 5"（由 AI 从榜单结果切片呈现，无独立命令）
- **查找某模型**："DeepSeek排第几"、"GPT-5.6在哪里"
- **按厂商筛选**："DeepSeek 的模型排名"、"OpenAI 的模型"（AI 根据厂商字段过滤）

## 核心约束

1. **数据真实性** — 禁止编造排行榜数据，必须从证券之星真实页面返回中提取
2. **数据来源** — 排行榜数据服务端直出（日榜/周榜均内嵌于页面 HTML），无独立 API
3. **请求方式** — 使用 Python 脚本 `scripts/cli.py`（通过 `$PYTHON $RANK` 调用），统一加 `--json` 参数获取 JSON 输出
4. **输出格式** — 脚本输出 JSON，AI 负责组织语言呈现给用户，不直接输出 JSON 原文
5. **周期筛选** — 支持日榜/周榜/全部，`--period day|week|all`（含中英文别名：日/今日/today、周/本周/week）
6. **字段语义** — 趋势由页面箭头颜色判定：红色=上升（up）、绿色=下降（down）；`is_new` 表示新上榜；`vendor` 为模型厂商（JSON 中为页面原始 slug，文本表格中映射为中文展示名：中国厂商中文名、海外厂商英文品牌）；`updated_at` 为榜单数据更新日期（页脚标注，日榜/周榜同一快照日期）

## 脚本命令

```bash
$PYTHON $RANK ranking [--period day|week|all] --json      # 查看调用排行榜（默认双榜）
$PYTHON $RANK search <模型/厂商关键词> --json            # 在日榜/周榜中查找模型（支持中文厂商名）
```

脚本返回 JSON 后，AI 按场景组织语言，不要把整段 JSON 原样输出给用户。

## JSON 输出字段说明

**顶层字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `source` | string | 页面地址（https://tech.stockstar.com/） |
| `data_source` | string | 页面标注的数据来源（如 `数据来源：openrouter`） |
| `updated_at` | string | 榜单数据更新日期（如 `2026-08-20`，页脚标注；日榜/周榜共用同一快照日期） |
| `periods.日榜` / `periods.周榜` | object | 各周期榜单，含 `count` 与 `items` |

> `search` 命令返回结构类似：`{source, data_source, updated_at, keyword, matches[], status}`，
> 其中 `matches[]` 每项含 `period`（周期名）+ 下方条目字段。

**单个榜单条目字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `rank` | int | 排名（从 1 开始） |
| `model` | string | 模型名称 |
| `vendor` | string | 模型厂商（页面原始 slug，如 `deepseek`、`openai`；文本表格中脚本会映射为中文展示名） |
| `tokens` | string | 调用量（如 `11.3T`、`948B`，T=万亿，B=十亿） |
| `change` | string | 变动百分比（如 `20%`），新上榜为空 |
| `trend` | string | 变动方向：`up` 上升 / `down` 下降 / `""` 无箭头 |
| `is_new` | bool | 是否新上榜（页面 "new" 标记） |

**厂商 slug → 展示名参考表：**

> 规则：中国厂商显示中文名，海外厂商保留英文品牌。脚本文本表格与 `config.py` 的 `VENDOR_NAMES` 一致；未知 slug 回退原文。JSON 中 `vendor` 保持原始 slug，AI 转述时可用此表翻译。

| slug | 展示名 |
|------|------|
| `deepseek` | 深度求索 |
| `tencent` | 腾讯 |
| `openai` | OpenAI |
| `anthropic` | Anthropic |
| `google` | Google |
| `xiaomi` | 小米 |
| `z-ai` | 智谱（Z.ai） |
| `nvidia` | NVIDIA |
| `poolside` | Poolside |
| `minimax` | MiniMax |
| `moonshotai` | 月之暗面（Kimi） |
| `stepfun` | 阶跃星辰 |

## 工作流

### 流程 1：查看调用排行榜（核心场景）

**步骤：**
1. 调用 `$PYTHON $RANK ranking --json` 获取日榜+周榜
2. 用户指定周期时加 `--period day`（日榜）或 `--period week`（周榜）
3. 解析 JSON，用中文向用户总结榜单

**输出示例：**
```
📊 大模型调用排行榜（更新：2026-08-20）

### 周榜（20 条）
| 排名 | 模型 | 厂商 | Tokens | 变动 |
|------|------|------|--------|------|
| 1 | DeepSeek V4 Flash 0731 | 深度求索 | 11.3T | ↑20% |
| 2 | Hy3 | 腾讯 | 9.7T | ↑9% |
| 4 | MiMo-V2.5 | 小米 | 4.99T | ↓6% |
| 18 | DeepSeek V4 Pro 0813 | 深度求索 | 796B | new |

### 日榜（20 条）
...
> 榜单由证券之星科技频道整理，数据来源：openrouter
```

### 流程 2：查看前 N 名

用户要求"前几个/TOP N"时，**无需独立命令**：调用 `ranking --period <周期> --json` 后，AI 直接取 `items` 前 N 条用表格呈现即可。

**步骤：**
1. 调用 `$PYTHON $RANK ranking --period <day|week> --json`（按用户指定周期；未指定时用双榜）
2. 取 `periods.<周期>.items` 前 N 条
3. 以表格形式呈现前 N 名

### 流程 3：查找某个模型 / 按厂商筛选

**步骤：**
1. 用户问"某模型排名"→ 调用 `$PYTHON $RANK search <模型关键词> --json`，返回模型在日榜/周榜中的排名和关键数据
2. 用户按厂商问"某厂商的模型"（如"搜小米的模型"）→ `search` 同时匹配模型名、厂商 slug 与中文展示名，直接调用 `search <厂商名> --json` 即可（英文 slug 或中文名均可）
3. 用中文呈现（厂商展示名参考上面的参考表，AI 转述与脚本文本表格保持一致）

### 流程 4：文本摘要呈现

AI 应根据榜单组织语言，例如：
- 榜首及变化：**周榜第一为 DeepSeek V4 Flash 0731，厂商深度求索，Tokens 11.3T，环比上升 20%**
- 新上榜提示：**DeepSeek V4 Pro 0813 本周新上榜，排第 18**
- 下降提示：**MiMo-V2.5 周榜下降 6%**
- 涨跌幅过百提示：**日榜榜首 MiMo-V2.5 单日 Tokens 大涨 225%**
- 厂商分布提示：**周榜前 10 中深度求索占 3 席，OpenAI 占 2 席**

## 异常处理

| 异常 | 处理方式 |
|------|---------|
| 网络请求失败 | 提示用户稍后重试 |
| 页面结构变化导致无数据 | 提示"未获取到排行榜数据"，建议稍后重试 |
| 搜索无匹配 | 提示未找到该模型，建议更换关键词 |
| 无效周期参数 | 自动回退为全部（all），无需提示 |
