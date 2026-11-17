# 双向细目表（蓝图）格式与校验规则（元题 yotta-item）

## 一、蓝图（JSON，必填）

```json
{
  "schema_version": "1.0",
  "title": "七年级上数学 第一单元测试",
  "total_points": 60,
  "time_limit_minutes": 60,
  "coverage": ["K3"],
  "sections": [
    {
      "id": "S1",
      "title": "选择题",
      "type": "single_choice",
      "count": 10,
      "points_each": 3,
      "difficulty": {"easy": 5, "medium": 3, "hard": 2},
      "knowledge": ["K1"]
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `schema_version` | string | 是 | 固定 `1.0` |
| `title` | string | 是 | 卷名（进入试卷与报告标题） |
| `total_points` | number | 是 | 全卷总分，必须等于 Σ（`count` × `points_each`） |
| `time_limit_minutes` | number | 是 | 限时（分钟），大于 0 |
| `coverage` | string[] | 否 | 全卷必考考点，不允许重复 |
| `sections[].id` | string | 是 | 分节 id，全卷唯一 |
| `sections[].title` | string | 否 | 分节名称（默认用 id） |
| `sections[].type` | string | 是 | 题型键，必须与题库题目 `type` 一致 |
| `sections[].count` | int | 是 | 该节题量，正整数 |
| `sections[].points_each` | number | 是 | 该节每题分值，大于 0 |
| `sections[].difficulty` | object | 是 | 难度配额（档位 → 题数），各档之和必须等于 `count` |
| `sections[].knowledge` | string[] | 否 | 该节必覆盖考点 |

## 二、校验规则（`blueprint validate`）

命中任一条即退出码 3：

1. `schema_version` 不是 `1.0`；
2. 缺少 `title`；
3. `total_points` 与 `sections` 合计不一致（报错同时给出两个数字）；
4. `sections` 不是非空数组，或分节 id 重复；
5. `count` 不是正整数；
6. `points_each` 不是正数；
7. `difficulty` 不是非空对象，或难度配额之和 ≠ `count`；
8. 难度档不在可用档位内（与题库 `difficulty_levels` 对齐检查时启用）；
9. `coverage` 存在重复考点；
10. `time_limit_minutes` 不是正数。

## 三、怎么把「双向细目表」写成蓝图

1. 先定**题型与题量**：每节写 `type` / `count` / `points_each`；
2. 再定**难度配额**：把该节题量分配到 `difficulty` 各档（各档之和必须等于 `count`）；
3. 再定**必考考点**：分节必考写在该节 `knowledge`，全卷必考写在顶层 `coverage`；
4. 最后核对**总分**：`total_points` 必须等于所有分节题的分数合计。

建议：

- 分节必考考点尽量分散到不同分节，避免同一考点反复占用题量；
- `coverage` 里的考点若在当前分节类型中没有对应题目，组卷会如实报告覆盖缺口；
- 配额过紧（例如某档只有 1 道题却要求 3 道）时会报缺口，不会用其它难度的题顶替。

## 四、组卷与校验的确定性

- `assemble` 使用 `--seed`（默认 0）；同一题库 + 同一蓝图 + 同一 seed = 同一份试卷；
- `check` 不使用随机性：同一试卷、题库与蓝图，得到同一份缺口清单。
