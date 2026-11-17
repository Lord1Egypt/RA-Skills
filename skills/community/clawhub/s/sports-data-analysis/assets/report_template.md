# 单场分析报告输入模板（match.json）

本文件说明 `match.json` 的字段结构与填写方法。把下面内容复制为 `match.json`，填好你的赛事信息，再用：

```bash
python scripts/analytics.py report --input match.json --output report.html
```

> **报告长什么样（体育赛事风格）**：顶部深色英雄区（队徽 SVG + 联赛/时间）→ **「赛事信息要点」面板**：把本场可讨论的信息要点结构化呈现；其余 section（天气 / 球员 / 状态 / 情报 / 专家 / 分析逻辑 / 结论与风险）沿用全维度结构，信息始终是视觉焦点。本工具**只做信息整理与可视化，不做赛果判断、**。

---

## 最小可用示例

```json
{
  "match": "曼城 vs 阿森纳",
  "sport": "football",
  "league": "英超",
  "country": "英格兰",
  "venue": "伊蒂哈德球场",
  "city": "曼彻斯特",
  "kickoff_local": "2026-08-15 23:30",
  "kickoff_actual": "2026-08-16 03:30",
  "updated_at": "2026-08-15",
  "weather": {
    "temp": "18℃", "humidity": "65%", "condition": "多云", "wind": "3级", "rain": "10%",
    "impact": "体感偏凉，对技术流传导影响有限。"
  },
  "teams": [
    {"name": "曼城", "status_note": ""},
    {"name": "阿森纳", "status_note": ""}
  ],
  "formations": ["4-3-3", "4-2-3-1"],
  "players": [
    {"name": "哈兰德", "team": "曼城", "key": true, "status": "首发", "role": "中锋", "note": "禁区终结效率高", "gender": "male", "number": "9"},
    {"name": "萨卡", "team": "阿森纳", "key": true, "status": "首发", "role": "右边锋", "note": "反击爆点", "gender": "male", "number": "7"}
  ],
  "key_players": [
    {"name": "哈兰德", "team": "曼城", "role": "中锋", "gender": "male", "number": "9"},
    {"name": "萨卡", "team": "阿森纳", "role": "右边锋", "gender": "male", "number": "7"}
  ],
  "form_last5": {
    "曼城": ["胜", "胜", "平", "胜", "胜"],
    "阿森纳": ["胜", "平", "胜", "胜", "平"]
  },
  "h2h_last5": ["胜", "平", "负", "胜", "平"],
  "intel": [
    {"tier": "官方", "text": "曼城赛前发布会确认德布劳内复出进入大名单。"},
    {"tier": "未证实传闻", "text": "网传阿森纳后防有轻伤隐患，待官方名单确认。"}
  ],
  "experts": [
    {"tier": "权威专家", "name": "赛事研究中心", "source": "官方赛事数据网",
     "view": "曼城近况与主场均占优，阿森纳防守硬度不容小觑，本场更看双方中场控制权。"}
  ],
  "info_points": [
    "曼城主场控球与高位压迫是其惯性打法，阿森纳需在中场绞杀中寻找反击空间。",
    "双方近期状态均稳定，阿森纳客场防守韧性是关键变量。"
  ],
  "analysis": "曼城控球与射门转化占优，阿森纳反击犀利。本场核心看点在中场控制权与边路一对一，信息层面曼城略占结构优势，但最终走向仍取决于临场发挥与判罚等偶然因素。",
  "confidence": "中高",
  "risk": "足球含平局与意外，任何单场都不存在确定结果；本报告只做信息整理，请以理性观赛心态看待。"
}
```

---

## 完整字段说明

| 字段 | 含义 | 说明 |
| --- | --- | --- |
| `match` | 对阵 | 如 `"曼城 vs 阿森纳"`；也支持 `A vs B` 自动拆解主客队 |
| `sport` | 运动类型 | `football` / `basketball` / `volleyball` / `tennis` / `beach_volleyball` / `table_tennis` / `badminton` / `ice_hockey` / `handball` / `water_polo` / `field_hockey` / `rugby` / `baseball` |
| `league` | 联赛 / 赛事 | 用于自动标注赛事风格特征（见 `LEAGUES`） |
| `country` | 国家 / 地区 | 驱动国旗 SVG |
| `venue` / `city` | 场馆 / 城市 | 展示用 |
| `kickoff_local` / `kickoff_actual` | 开赛时间 | 当地 / 北京时间双显（时差比赛必填） |
| `updated_at` | 数据更新时间 | 用于新鲜度自查 |
| `weather` | 天气 | `temp`/`humidity`/`condition`/`wind`/`rain`/`impact` |
| `teams[]` | 主客队 | `name` + `status_note` |
| `formations` | 阵型 | 如 `["4-3-3","4-2-3-1"]`，渲染站位动画 |
| `players[]` | 球员状态 | `name`/`team`/`key`(是否核心)/`status`/`role`/`note`/`gender`(male\|female，驱动头像男女)/`number`(球衣号，显示在胸前)/`region`(亚洲\|欧美\|非洲，驱动头像肤色发色；缺省按球队/联赛关键词推断)/`star`(可选 1~5，按统一公开成就分级标准指定的焦点星级)/`achievement`(职业生涯最高成就，显示为重点卡右侧金色竖条) |
| `key_players[]` | 重点球员 | `name`/`team`/`role`/`gender`/`number`/`region`/`star`/`achievement`，驱动聚焦卡 |
| `form_last5` | 近5场状态 | `{队名: ["胜","平","负",...]}`，渲染彩色 chip |
| `h2h_last5` | 交锋近5次 | `["胜","平","负",...]`（主队视角） |
| `intel[]` | 赛前情报 | `tier`(官方/权威媒体/未证实传闻) + `text`，分级呈现 |
| `experts[]` | 专家观点 | `tier`/`name`/`source`/`view`，分级 + 可信度标注 |
| `info_points[]` | 赛事信息要点 | 本场可讨论的信息要点（纯描述） |
| `analysis` | 分析逻辑 | 综合叙述文字（描述信息层面的结构与变量） |
| `confidence` | 综合信心 | 自由文本，如 `中高`；仅表示信息充分度，非赛果判断 |
| `risk` | 结论与风险 | 风险提示文字 |

> 报告段顺序：阵型变化动画（首屏卡片）→ 一、赛事信息要点 → 二、赛事概况与天气 → 三、球员状态（含⭐主力）→ 四、近期状态与交锋 → 五、赛前情报（分级）→ 六、专家观点（权威/非权威）→ 七、分析逻辑 → 八、结论与风险提示。
> 报告仅做信息整理与可视化，不含任何赛果倾向或结论性建议。

---

## 每日总览（day.json）

把**足球 + 篮球 + 其它球类**放进同一份 JSON，用 `daily` / `focus` 命令生成聚合总览：

```json
{
  "date": "2026-08-16",
  "title": "今日体育赛事总览",
  "matches": [
    { "/* 单场 match 结构 */": "...", "key": true, "key_players": [{"name":"哈兰德","team":"曼城","role":"中锋"}] },
    { "/* 另一场 */": "..." }
  ]
}
```

报告顶部是"总汇总"仪表盘（每张卡片标出本场看点提示），**点击任意卡片平滑跳转到该场详细单元**（`#match-N` 锚点），前置引导模块 + 今日重点速览。`daily` 出全部赛事，`focus` 仅保留 `key=true` 或含 `key_players` 的重点场次。

---

## 采集方法（详见 references/data_sources.md）

天气 / 球员 / 状态 / 情报 / 专家等字段，调用本 Skill 的模型应依 `analytics.py gather` 给出的检索清单，用联网搜索逐项采集，并按 `tier` 分级；未证实信息必须标 `未证实传闻`，仅作视野补充，不可作为依据。
