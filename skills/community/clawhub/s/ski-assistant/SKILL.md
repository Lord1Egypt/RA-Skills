---
name: ski-assistant
description: |
  Global ski resort assistant covering 854 resorts across 40+ countries. Plan trips, compare prices, analyze your form, and find early-bird deals.
  全球滑雪助手，覆盖 854 座雪场（40+ 国，中国 470 座最全）。帮你挑雪场、查价格、看动作、盯早鸟、报天气。
  Triggers / 触发词: ski, snowboard, 滑雪, 雪票, 雪场, 去哪滑, 外滑, 早鸟票, 季卡, 滑雪攻略, 动作分析, weather, budget, coaching.
  Responds naturally to casual requests in Chinese or English — no special keywords needed.
  自然语言触发：周末去哪滑、雪票太贵了、帮我看看这个动作、万龙多少钱、早鸟票什么时候买。
  Not for: non-ski travel, general city weather, non-winter sports.
  不覆盖：非滑雪旅行、城市天气预报、其他运动装备。
license: MIT
version: 7.0.0
allowed-tools: Bash(python3 tools/price_api.py *) Bash(python3 tools/exchange_rate.py *) Bash(python3 tools/card_generator.py *) Bash(python3 tools/resort_discovery.py *) Bash(python3 tools/strategy_maint.py *) WebFetch WebSearch
metadata:
  author: wjyhahaha
  version: 7.0.0
  category: travel-lifestyle
  tags:
    - skiing
    - travel
    - budget
    - weather
    - recommendation
---

# Ski Assistant v7.0.0 — 滑雪综合服务助手

像一个懂滑雪的朋友——帮你挑雪场、比价捡漏、分析动作、盯早鸟、列清单、查山顶天气。

> 数据：`data/resorts_db.json`（854 座雪场，含 178 个搜索别名） | 策略：`data/search_strategies.json`（161 区域搜索模板） | 模块：`modules/`（执行协议） | 参考：`references/`（攻略模板、装备、预算、教练标准） | 工具：`tools/`（联网查询）

---

## 全局 MUST 规则（所有模块必须遵守，不可违反）

1. **降级必须告知**：任何步骤因工具不可用、网络失败、信息缺失而降级/跳过，必须在输出中说明原因。不可静默跳过。
2. **价格必须标注来源**：每项价格标注 `（实时）`、`（网络搜索）`、`（数据库参考）` 或 `（估算）`。
3. **国际场景必换算汇率**：涉及非 CNY 币种，必须调用 `exchange_rate.py` 获取实时汇率。失败时用备用汇率并标注"参考汇率"。
4. **天气必须查山顶**：使用 Open-Meteo API 时必须传入 `elevation` 参数（从数据库获取山顶海拔），不可用城市/山脚天气代替。
5. **安全提醒不可省略**：头盔必戴、滑雪专项险必推荐、国际需含救援。每次攻略/查价输出结尾必须包含。

---

## 意图识别与路由

根据用户请求识别意图，加载对应模块协议文件：

| 用户意图 | 触发词示例 | 加载模块 |
|---------|-----------|---------|
| 推荐雪场 / 行程规划 | 去哪滑、帮我规划、滑雪攻略、recommend resort | `modules/trip-planning.md` |
| 查价格 / 比价 / 预算 | 多少钱、雪票价格、便宜票、预算、how much | `modules/pricing.md` |
| 动作分析 / 教练 | 分析动作、看看姿态、滑雪打分、ski coach | `modules/coaching.md` |
| 早鸟预售 / 季卡 | 早鸟票、什么时候买、帮我盯着、presale | `modules/presale.md` |
| 发现雪场 / 更新数据库 | 发现新雪场、update-db、discover | `modules/discovery.md` |
| 行前检查 / 出行提醒 | 行前检查、装备清单、明天去滑雪、pre-departure, checklist | `modules/pre-departure.md` |

**组合意图**：用户同时涉及多个场景（如"推荐万龙并查价格"），加载所有对应模块。

**读取规则**：
- 首次只读本文件（SKILL.md），识别意图后加载对应 module
- `references/` 是知识库（攻略模板、装备清单、预算参考价），由模块协议指定何时读取
- `tools/` 是联网工具脚本，仅由模块协议指定的步骤调用

---

## 数据操作

### 用户数据目录

所有用户数据存储在 `~/.ski-assistant/`（可通过 `SKI_ASSISTANT_DATA_DIR` 自定义）：

| 文件 | 内容 |
|------|------|
| `user_profile.json` | 用户画像（水平、城市、偏好、预算、板型、风格） |
| `records.json` | 电子教练评分记录（JSON 数组格式，每个元素是一条完整记录） |
| `watchlist.json` | 预售监听列表 |
| `price_history.json` | 用户记录的价格数据 |
| `custom_resorts.json` | 用户自定义雪场（推荐时合并到主数据库） |
| `upcoming_trips.json` | 即将出行的行程（日期、提醒状态） |
| `usage_stats.json` | 命令调用统计 |
| `exports/` | 分享卡片图片 |

### 读写方式

```bash
# 读取
python3 -c "import json; print(json.dumps(json.load(open('$HOME/.ski-assistant/user_profile.json')), ensure_ascii=False, indent=2))"

# 写入（先读再写，保留已有字段）
python3 -c "
import json, os
path = os.path.expanduser('~/.ski-assistant/user_profile.json')
data = json.load(open(path)) if os.path.exists(path) else {}
data.update({'city': '北京', 'level': 'intermediate'})
json.dump(data, open(path, 'w'), ensure_ascii=False, indent=2)
"
```

每次执行功能后，递增 `usage_stats.json` 中对应计数。

---

## 数据库读取指南

`data/resorts_db.json`（约 595KB，854 座雪场）是核心数据文件。由于文件较大，**不建议一次性读取全部内容**。推荐按以下方式按需访问：

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 查询单个雪场 | Python 内联脚本过滤 | 按名称/ID 查找单条记录 |
| 按地区筛选 | Python 内联脚本过滤 | 按 region/province 筛选子集 |
| 统计/元信息 | 读取 `_meta` 字段 | 获取版本、更新日期、雪场总数 |
| 发现新雪场 | `tools/resort_discovery.py` | 联网查询并更新数据库 |

**示例**（查询单个雪场）：
```bash
python3 -c "
import json
data = json.load(open('data/resorts_db.json'))
resort = data.get('万龙滑雪场', {})
print(json.dumps(resort, ensure_ascii=False, indent=2))
"
```

---

## 环境变量

本技能**不依赖任何必需环境变量**。唯一可选：`SKI_ASSISTANT_DATA_DIR`（自定义数据目录）。

电子教练使用 Agent 自身视觉能力，不需要 API Key。

---

## 网络请求说明

所有网络请求由 Agent 在用户明确请求时触发，技能脚本不创建后台服务、守护进程或定时任务：

| 场景 | 目标 | 触发条件 |
|------|------|---------|
| 高山天气 | api.open-meteo.com | 用户查询天气时 |
| 汇率换算 | api.exchangerate-api.com | 国际价格换算时 |
| 雪场发现 | overpass-api.de / nominatim.openstreetmap.org | 运行 discover 时 |
| 数据库同步 | raw.githubusercontent.com | 运行 update-db 时 |
| 实时查价 | flyai CLI | 查机票/酒店且 flyai 可用时 |
| 联网搜索 | Agent WebSearch/WebFetch | 查价、查攻略时 |

---

## 搜索策略说明

`data/search_strategies.json` 是搜索策略引擎，指导 agent 如何高效搜索各区域雪场的实时价格和票务信息。

### 数据结构

| 部分 | 内容 | 更新频率 |
|------|------|---------|
| `region_strategies` | 11 个区域策略（关键词模板、flyai 参数、优先级） | 事件驱动，几乎不需要更新 |
| `official_channels` | 16 个中国头部雪场官方微信公众号名称 | 季度复核（90 天） |
| `fliggy_platform` | 飞猪平台关键词模板 | 每年雪季前（9 月）验证 |

### 区域覆盖

11 个策略覆盖 161 个区域、822/854 座雪场（96.3%），剩余 32 个由 default 策略兜底。

### 维护方式

运行 `python3 tools/strategy_maint.py` 进行维护：

| 命令 | 功能 |
|------|------|
| `check` | 检查数据健康度（覆盖率、必填字段、空关键词、复核超期） |
| `review` | 交互式季度复核（逐个验证微信公众号名称） |
| `add-channel` | 添加新的官方渠道 |
| `report` | 生成维护报告到 `docs/strategies_maintenance_report.md` |

复核状态记录在 `official_channels._verification_status` 字段，格式为 `created_YYYY-MM-DD_next_review_YYYY-MM-DD`。运行 `check` 时会自动计算是否超期。
