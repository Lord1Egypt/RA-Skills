# 题库格式与校验规则（元题 yotta-item）

## 一、题库（JSON，必填）

```json
{
  "schema_version": "1.0",
  "subject": "数学",
  "grade": "七年级上",
  "difficulty_levels": ["easy", "medium", "hard"],
  "items": [
    {
      "id": "SC-01",
      "type": "single_choice",
      "points": 3,
      "difficulty": "easy",
      "knowledge": ["一元一次方程的定义"],
      "minutes": 2,
      "source": "校本题库A"
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `schema_version` | string | 是 | 固定 `1.0` |
| `subject` / `grade` | string | 否 | 学科 / 年级，进入报告信息区 |
| `difficulty_levels` | string[] | 否 | 难度档位（2-5 档，不重复）；默认 `easy` / `medium` / `hard` |
| `items` | object[] | 是 | 题目数组，不能为空 |
| `items[].id` | string | 是 | 题目 id，全库唯一（组卷与校验都靠它引用） |
| `items[].type` | string | 是 | 题型键（如 `single_choice` / `fill_blank`），与蓝图 `type` 对应 |
| `items[].points` | number | 是 | 分值，必须大于 0 |
| `items[].difficulty` | string | 是 | 难度档，必须在 `difficulty_levels` 内 |
| `items[].knowledge` | string[] | 是 | 考点 / 知识点，不能为空 |
| `items[].minutes` | number | 否 | 预计作答分钟（用于时间预算），不小于 0 |
| `items[].source` | string | 否 | 来源标注（如「校本题库A」），进入报告 |

## 二、校验规则（`bank validate`）

命中任一条即退出码 3，并给出中文原因：

1. `schema_version` 不是 `1.0`；
2. `items` 不是非空数组，或元素不是对象；
3. `id` 为空或重复；
4. 缺少 `type` 或 `type` 为空；
5. `points` 不是数字，或小于等于 0；
6. `difficulty` 不在题库档位内；
7. `knowledge` 不是字符串数组或为空数组；
8. `minutes` 为负数；
9. `source` 存在但不是非空字符串；
10. `difficulty_levels` 少于 2 档、多于 5 档或存在重复。

## 三、写作建议（不影响校验，影响报告可读性）

- **id 用稳定前缀**：如 `SC-`（选择题）/ `FB-`（填空题）/ `SA-`（简答题），便于人工复核；
- **同一考点至少留 2-3 道同类型题**：组卷需要足够余量，否则容易出现缺口；
- **难度标注写成相对口径**：题库标注是组卷约束，不等于考后实测难度；
- **`minutes` 尽量填**：不填则该题按 0 分钟计入时间预算，预算会偏乐观。
