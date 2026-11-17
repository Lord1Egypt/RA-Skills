# TOOLS.md

## 数据获取工具

### 当前阶段（MVP）

#### 1. 联网搜索（online-search 技能）

**用途**：获取实时小区成交数据、挂牌数据、周边配套、政策动态。

**调用方式**：
```bash
# 搜索小区成交数据
node '<SCRIPT_PATH>/scripts/prosearch.cjs' --keyword="小区名 成交 2026" --freshness=30d

# 搜索小区挂牌数据
node '<SCRIPT_PATH>/scripts/prosearch.cjs' --keyword="小区名 二手房 挂牌" --freshness=7d

# 搜索周边配套（学校/地铁/商业）
node '<SCRIPT_PATH>/scripts/prosearch.cjs' --keyword="小区名 周边配套"

# 搜索区域政策
node '<SCRIPT_PATH>/scripts/prosearch.cjs' --keyword="城市名 房产政策 2026" --industry=gov
```

**关键参数**：
- `--freshness=7d/30d/1y`：时效过滤（与 `--cnt` 互斥）
- `--industry=gov/news`：垂类过滤
- `--cnt=20`：返回数量（不与 `--freshness` 同时使用）

**输出规范**：
1. 先原样输出 `message` 字段（含可点击超链接）
2. 再基于搜索结果生成分析报告

#### 2. 数据置信度评估

搜索结果质量分级：
- ✅ **高置信度**：有贝壳/链家官方数据，近3个月成交≥3套
- ⚠️ **中置信度**：有房产平台数据，但时效>3个月或样本<3套
- ❌ **低置信度**：仅论坛/自媒体信息，样本极少

置信度直接影响输出（参见 SOUL.md 置信度规则）。

### 未来阶段（数据管道完善后）

- PostgreSQL 成交数据库（直接查询，无需搜索）
- 挂牌实时数据 API
- 政策推送 Webhook
- 地图 POI API（周边配套自动识别）

## 工具使用原则

1. **先搜索，后分析**：每次分析必须先调用 online-search 获取最新数据
2. **数据不足时，明确说明置信度**：参见 SOUL.md 置信度规则
3. **不虚构数据**：所有数据必须来自搜索结果或明确标注“估算”
4. **搜索结果必须展示**：先输出 `message` 字段，再给分析

## 第三方接口（待接入）

- 贝壳研究院 API（成交数据直连）
- 中指院（市场数据）
- 高德/腾讯地图 POI API（周边配套）
- 各地政府公开数据平台（政策）

---

_更新：2026-06-06 — 集成 online-search 技能_
