---
name: themepica-finance-data-public
description: 语势科技金融数据公开API - 主题投资、热点榜单、ETF叙事、指数行情
homepage: https://www.themepica.com
version: 1.0.0
author: 语势科技 (Themepica)
---

# 语势科技金融数据公开API（Public版）

本技能封装了语势科技（Themepica）金融数据API的公开版接口，无需私有权限即可使用。支持主题投资分析、热点榜单、ETF叙事、指数行情等功能。

> 本技能是 `themepica-finance-data-v2` 的公开版子集，包含所有公开API（APPCODE认证），不含私有API。

---

## 关于语势科技（ThemePica）

### 产品定位

语势科技是**面向投资的叙事数据分析平台**，致力于捕获、量化和深度分析那些能够影响资金流向、资产定价、投资者风险偏好的"市场故事"。

> "人类作为一种'讲故事的物种'（homo narrans），本质上是通过叙事来构建认知、理解因果关系并在复杂世界中进行意义建构的。" —— 罗伯特·席勒

**核心价值**：捕捉传统金融数据难以量化的"认知动能"，提前捕捉未来价值迁移信号。

### 叙事数据 vs 舆情数据

| 对比维度 | 舆情数据 | 叙事数据（ThemePica） |
|----------|---------|----------------------|
| 底层问题 | 市场情绪温度是多少？ | **市场正在相信什么底层逻辑？** |
| 时间跨度 | 瞬时、易逝 | 长期、生命周期演进 |
| 技术侧重 | 词频、正负面判定 | 语境理解、因果逻辑构建 |
| 抗噪能力 | 弱，易受噪音干扰 | 强，侧重影响力与逻辑性 |
| 应用场景 | 高频套利因子 | **趋势拐点预判、主题全周期管理** |

### 产品体系架构

| 模块 | 核心能力 | 对应API |
|------|----------|---------|
| **热点数据** | 热点词/热点事件/热点搜索 | `hotspot_*`, `board_hotspots*` |
| **主题数据** | 主题叙事跟踪/股票池/指数池 | `themes`, `theme_*` |
| **策略数据** | 年度/季度/月度/日度策略 | 需私有API |
| **应用场景** | 量化·投研·投顾·营销 | 公开API可覆盖 |

### 核心概念关系

语势科技的叙事数据围绕**三大核心概念**构建，形成从"事件发现→主题跟踪→策略生成"的完整投资闭环：

```
热点（Hotspot）          主题（Theme）            策略（Strategy）
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ 每日热词榜单  │───→│ 主题诊断     │───→│ 季度重点主题  │
│ 热点关联证券  │    │ 热度/情绪/   │    │ 主题热度对比  │
│ 热点关联指数  │    │ 共识度/象限  │    │ 指数机会榜单  │
│ 热点关联主题  │    │ 主题叙事数据  │    │ AIGC异动写作  │
└──────────────┘    └──────────────┘    └──────────────┘
```

- **热点（Hotspot）**：市场事件的实时捕捉，是"输入信号"
- **主题（Theme）**：投资叙事的长期跟踪，是"分析框架"
- **策略（Strategy）**：基于主题叙事数据生成的投资方向，是"输出结果"

### 叙事分析五维度

| 维度 | 说明 | 投资含义 |
|------|------|----------|
| **热度（Heat）** | 市场关注度（0~1） | 高热度=市场聚焦 |
| **情绪（Sentiment）** | 市场情感光谱（0~1） | 积极=利好预期 |
| **共识度（Consensus）** | 观点一致性（0~1） | 高共识=方向明确 |
| **象限（Quadrant）** | 热度+情绪状态 | 蓄力/明星/分歧/沉寂 |
| **信号（Signal）** | 未来演化方向 | 机会/风险/观察 |

### 主题象限模型

```
情绪高 ↑
        │  蓄力（春季）  │  明星（夏季）  │
        │  热度低+情绪高  │  热度高+情绪高  │
        │  → 关注布局     │  → 核心持仓     │
────────┼────────────────┼────────────────
        │  沉寂（冬季）  │  分歧（秋季）  │
        │  热度低+情绪低  │  热度高+情绪低  │
        │  → 等待观察     │  → 警惕风险     │
        └────────────────┴────────────────→ 热度高
```

### 应用场景

| 场景 | 说明 | 典型用法 |
|------|------|----------|
| **量化投资** | 构建叙事驱动因子、策略回测 | 主题热度/情绪作为因子输入 |
| **投研分析** | 理解市场底层逻辑、趋势拐点预判 | 主题诊断+叙事数据时间序列 |
| **投顾支持** | 主题信息推送、投资建议参考 | 热点榜单+指数机会榜 |
| **线上营销** | 热点事件营销、用户搜索推荐 | 推荐热词+ETF异动写作 |

### 验证案例

**2026 Q1 重点主题收益**：超额验证（平均+3.11% vs 基准+0.3%）

**2026年度策略**（截至2026/06/30）：十大趋势股票池平均 **+18.80%**（沪深300：+7.55%），超额收益 **+11.25%**

### 主题分类体系

| 类型 | 数量 | 说明 |
|------|------|------|
| 自有主题 | 47 | 语势自建主题体系 |
| 指数主题 | 38 | 对应市场指数 |
| 孵化主题 | 29 | 新兴主题培育 |

**主题调整频率**：季度调整

### 产品特色

- ✅ **标准化**：数据自动化处理，标准统一
- ✅ **实时性**：9万+资讯/日，4000+信源
- ✅ **高智能**：AI全流程语义理解
- ✅ **广覆盖**：86个投资主题，覆盖全行业

---

## 首次使用

### 配置APPCODE

**方式一：配置文件**（推荐用于本地开发）
打开 `mcp_config.json`，将 `YOUR_APPCODE_HERE` 替换为你的真实APPCODE。

**方式二：环境变量**（推荐用于生产/CI/CD）
设置环境变量 `THEMEPICA_APPCODE`：
```bash
export THEMEPICA_APPCODE=你的APPCODE
```

> 环境变量优先级高于配置文件。两者都不配置时会提示错误。

### 获取密钥

联系语势科技商务获取APPCODE，或通过阿里云API网关市场购买。

### 环境要求

需要 Node.js 环境（已内置 `call-node.js`，无需额外依赖）

### ⚠️ 发布前必读

**发布前务必删除 `mcp_config.json` 中的真实APPCODE！**
将值改回 `YOUR_APPCODE_HERE` 占位符，或使用环境变量方式避免密钥泄露。

## 公开API列表（共25个接口）

### 1. 主题分析 (themes) — 7个接口
| 接口名 | 方法 | 路径 | 说明 |
|--------|------|------|------|
| `themes` | GET | /themes | 主题列表（分页） |
| `theme_indices` | GET | /theme/indices | 主题关联指数 |
| `theme_etfs` | GET | /theme/etfs | 主题关联ETF |
| `theme_diagnose` | GET | /theme/diagnose | 主题诊断（热度/情绪/象限/信号） |
| `theme_subs_diagnose` | GET | /theme/subs/diagnose | 子主题诊断 |
| `theme_narratives` | GET | /theme/narratives | 主题叙事数据（热度/情绪时间序列） |
| `theme_contents` | GET | /theme/contents | 主题相关资讯 |

### 2. 榜单 (board) — 4个接口
| 接口名 | 方法 | 路径 | 说明 |
|--------|------|------|------|
| `board_hotspots` | GET | /board/hotspots | 热点榜单（周度） |
| `board_hotspots_detail` | POST | /board/hotspots/detail | 热点榜单详情 |
| `board_hotspots_latest_detail` | GET | /board/hotspots/latest/detail | 最新热点榜单详情 |
| `board_indices` | GET | /board/indices | 指数机会榜单 |

### 3. 热点 (hotspot) — 10个接口
| 接口名 | 方法 | 路径 | 说明 |
|--------|------|------|------|
| `hotspot_heats` | POST | /hotspot/heats | 热点热度 |
| `hotspot_emotions` | POST | /hotspot/emotions | 热点情绪 |
| `hotspot_news` | GET | /hotspot/news | 热点关联资讯 |
| `hotspot_viewpoints` | GET | /hotspot/viewpoints | 热点关联观点 |
| `hotspot_securities` | GET | /hotspot/securities | 热点关联证券 |
| `hotspot_indices` | GET | /hotspot/indices | 热点关联指数 |
| `hotspot_themes` | GET | /hotspot/themes | 热点相关主题 |
| `hotspot_etfs` | GET | /hotspot/etfs | 热点关联ETF |
| `hotspot_policies` | GET | /hotspot/policies | 热点关联政策 |
| `hotspot_funds` | GET | /hotspot/funds | 热点关联基金 |

### 4. 基金 (fund) — 1个接口
| 接口名 | 方法 | 路径 | 说明 |
|--------|------|------|------|
| `fund_narratives` | GET | /v2.1/fund/narratives | 基金叙事数据 |

### 5. 指数 (index) — 2个接口
| 接口名 | 方法 | 路径 | 说明 |
|--------|------|------|------|
| `index_detail` | GET | /index/detail | 指数详情 |
| `index_daily` | GET | /index/daily | 指数历史日行情 |

### 6. ETF — 1个接口
| 接口名 | 方法 | 路径 | 说明 |
|--------|------|------|------|
| `etf_narratives` | GET | /etf/narratives | ETF叙事数据 |

## 使用方法

### 命令行调用

```bash
node call-node.js <apiName> <paramsJSON> [--list]

# 示例
node call-node.js themes '{"pageNum": 1, "pageSize": 10}'
node call-node.js theme_diagnose '{"themeId": "1477062244"}'
node call-node.js board_hotspots '{"pageNum": "1", "pageSize": "5"}'
node call-node.js hotspot_heats '{"keywords": ["英伟达"], "startTime": "2026-08-03 00:00:00", "endTime": "2026-08-12 12:34:32"}'

# 列出所有可用API
node call-node.js --list
```

### 在代码中调用

```javascript
const { call } = require('./call-node.js');

// 调用公开API
const result = await call('themes', { pageNum: 1, pageSize: 10 });
const diagnose = await call('theme_diagnose', { themeId: '1477062244' });
const hotspots = await call('board_hotspots', { pageNum: '1', pageSize: '10' });
```

## 服务地址

- **生产环境**: https://data.api.themepica.com
- **UAT环境**: https://uat.data.api.themepica.com/uat

## 认证方式

所有请求需要在Header中传入APPCODE：

```
Authorization: APPCODE your_appcode_here
```

## 核心概念

### 主题叙事体系

**主题热度**：市场关注度的量化指标
- 高热：热度归一值 ≥ 0.8
- 热：0.6 ≤ 热度归一值 < 0.8
- 温：0.4 ≤ 热度归一值 < 0.6
- 冷：热度归一值 < 0.4

**主题情绪**：市场参与者的情感光谱
- 积极：情绪归一值 ≥ 0.6
- 中性：0.5 ≤ 情绪归一值 < 0.6
- 消极：情绪归一值 < 0.5

**主题象限**：基于热度和情绪的状态判定
- 蓄力主题（春季）：热度<0.6且情绪≥0.6
- 明星主题（夏季）：热度≥0.6且情绪≥0.6
- 分歧主题（秋季）：热度≥0.4但情绪<0.6
- 沉寂主题（冬季）：热度<0.4且情绪<0.6

**主题信号**：未来演化方向预测
- 机会：较高概率向积极方向演化
- 风险：较高概率向消极方向演化
- 观察：未触发机会/风险信号

### 热点叙事体系

**热点热度**：
- 高热：热度 > 200
- 热：20 < 热度 ≤ 200
- 低热：热度 ≤ 20

**热点情绪**：
- 积极：情绪 > 0.2
- 消极：情绪 < -0.05
- 中性：其他情况

## 参考文档

详细的API参数和返回格式请参考 `references/` 目录下的文档：
- [主题API](references/themes.md) — 7个公开接口
- [榜单API](references/board.md) — 4个公开接口
- [热点API](references/hotspot.md) — 10个公开接口
- [基金API](references/fund.md) — 1个公开接口
- [指数API](references/index.md) — 2个公开接口
- [ETF API](references/etf.md) — 1个公开接口

## 注意事项

1. **APPCODE不要硬编码到代码中**，应通过配置文件或环境变量传入
2. 部分接口需要传入日期参数，格式为 `YYYY-MM-DD`
3. 时间格式：热点相关接口的时间格式为 `YYYY-MM-DD HH:mm:ss`
4. 分页接口默认返回前10条数据，可通过 `pageSize` 参数调整
5. POST请求的接口参数需要放在请求体中（JSON格式）
6. **`theme_contents` 接口必须同时传 `startDate`、`endDate`、`newsCategory` 三个参数**，缺一不可，否则返回 HTTP 400

## 错误处理

API返回的错误码说明：
- `0` - 成功
- `101` - 查询关键词为空
- `102` - 查询关键词过长
- `103` - 查询对象不存在
- `201` - startTime为空
- `301` - endTime为空
- `302` - endTime晚于当天
- `401` - start为负
- `501` - end为负
- `1001` - startTime晚于endTime
- `1002` - 查询时间区间过长
- `2001` - end小于start
- `2002` - 返回条数大于100条

HTTP状态码说明：
- `403` - 流控限制、配额用完、欠费等
- `400` - 请求参数错误
- `500` - 服务器内部错误
- `503` - 服务不可用
- `504` - 后端服务超时