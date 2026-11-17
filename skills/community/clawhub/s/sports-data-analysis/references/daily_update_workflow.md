# 每日信息更新工作流（refresh）

> 本 Skill 不只是"出一次报告"，而是能**随时刷新**比赛信息、补充分级情报，并自我体检、自我修复。本工作流聚焦于**信息更新**，不涉及任何赛前信息或相关追踪。

---

## 一、为什么需要更新

比赛信息（官方名单、伤停、天气、情报）在赛前数天到开赛会持续变化。一份昨天出的报告，今天可能"过期"。本工作流让报告具备"时效戳"，并支持增量补充。

---

## 二、refresh 命令

```bash
# 1) 基础刷新：写 updated_at、重生成报告（默认回写 JSON）
python scripts/analytics.py refresh --input match.json

# 2) 合并增量补丁（任意字段递归合并：比赛信息/天气/伤停/战意/情报/专家…）
python scripts/analytics.py refresh --input match.json --patch patch.json

# 3) 不回写（只看结果）
python scripts/analytics.py refresh --input match.json --no-write
```

- `refresh` 会刷新 `updated_at` 时间戳，并重生成 HTML 报告；默认回写输入 JSON。
- `--patch` 接收一个补丁 JSON，按字段递归合并进原数据（如新增一条 `intel`、更新 `weather`）。
- `--no-write` 关闭回写，适合只想预览更新效果。

---

## 三、可更新 / 补充的维度（字段见 `assets/report_template.md`）

| 维度 | 字段 | 说明 |
| --- | --- | --- |
| 时效 | `updated_at` | 数据更新时间，用于新鲜度自查 |
| 天气 | `weather` | 比赛日温度/湿度/风力/降水及影响 |
| 伤停 / 状态 | `players[]` | 主力伤缺/复出/阵容 |
| 情报 | `intel[]` | 新增官方/权威/未证实信息（须分级） |
| 专家观点 | `experts[]` | 新增分级观点 |
| 信息要点 | `info_points[]` | 补充本场可讨论要点 |
| 分析逻辑 | `analysis` | 随信息更新调整叙述 |

> 所有新增信息必须标注来源与分级；未证实传闻仅作视野补充，不可作为依据。

---

## 四、自查自修复（audit.py）

每次生成或更新报告，建议跑一遍质量闸门：

```bash
python scripts/audit.py match.json
python scripts/audit.py match.json --strict
```

检查项：信息完整性、数据新鲜度、专家 tier 有效性、权威观点冲突、重复观点去重、头像质量（仅当携带照片头像时）。

---

## 五、合规红线

- 本工作流只更新**公开可核查的信息**，不做赛前信息变化追踪、不出现任何敏感类表述。
- 赛前信息更新只是"公开信息在如何变化"的线索，**不预示结果**；报告明确警示"请勿据此盲跟"。
- 本 Skill 不做结果判断、不做任何赛果判断。
