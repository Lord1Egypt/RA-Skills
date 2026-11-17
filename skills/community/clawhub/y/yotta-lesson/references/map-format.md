# 映射包与结构配置（元案 yotta-lesson）

## 一、课标映射包（JSON，必填）

```json
{
  "schema_version": "1.0",
  "subject": "数学",
  "grade": "七年级上",
  "lessons": [
    {
      "id": "L1",
      "title": "认识一元一次方程",
      "unit": "一元一次方程",
      "periods": 1,
      "knowledge": ["一元一次方程的定义", "方程的解"],
      "key_points": ["一元一次方程的定义"],
      "difficulties": ["由实际问题抽象出方程"],
      "misconceptions": ["把含未知数的式子都当方程"],
      "standard": "义务教育数学课程标准（2022 年版）· 方程与不等式"
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 是 | 课题 id，不可重复；`plan` / `check` 用它定位课题 |
| `title` | string | 是 | 课题名称（进入教案标题） |
| `unit` | string | 否 | 所属单元 |
| `periods` | int | 否 | 课时数，默认 1；可用 `--periods` 覆盖 |
| `knowledge` | string[] | 是 | 知识点（进入学习目标，`check` 逐条核对是否出现在教案中） |
| `key_points` | string[] | 否 | 教学重点 |
| `difficulties` | string[] | 否 | 教学难点 |
| `misconceptions` | string[] | 否 | 易错点（缺省会在备课时提示补充） |
| `standard` | string | 是 | 课标来源标识（可追溯性必需；请填写可核对的条目标识） |

顶层 `subject` / `grade` 会写入骨架信息区，便于同一映射包跨班复用。

## 二、结构配置（JSON，可选）

```json
{
  "schema_version": "1.0",
  "minutes_per_period": 45,
  "stages": [
    {"id": "lead_in", "name": "导入", "ratio": 0.10},
    {"id": "explore", "name": "新知探究", "ratio": 0.30},
    {"id": "explain", "name": "例题精讲", "ratio": 0.25},
    {"id": "practice", "name": "练习巩固", "ratio": 0.25},
    {"id": "summary", "name": "小结与作业", "ratio": 0.10}
  ],
  "required_stages": ["lead_in", "explore", "practice", "summary"],
  "check_keywords": {
    "practice": ["练习", "巩固", "变式"],
    "summary": ["小结", "作业", "总结"]
  }
}
```

| 字段 | 说明 |
|---|---|
| `minutes_per_period` | 每课时分钟数（不小于 5，默认 45） |
| `stages` | 环节定义：`id` / `name` / `ratio`（比例为相对权重，不必和为 1） |
| `required_stages` | 必填环节（`check` 会逐项核对关键词是否出现在教案中） |
| `check_keywords` | 环节 → 关键词数组；命中任一即认为该环节存在 |

时间分配采用**最大余数法**：按比例取整后，把剩余分钟按小数部分从大到小补齐，保证
各环节分钟合计精确等于 `课时 × 每课时分钟`。

## 三、常见报错对照

| 提示 | 原因 | 处理 |
|---|---|---|
| `schema_version 必须是 1.0` | 版本不匹配 | 按模板修正 |
| `课题 id 重复：L1` | 同一 id 出现两次 | 合并或改名 |
| `缺少 standard` | 未填课标来源 | 补条目标识（可追溯性必需） |
| `knowledge 必须是字符串数组` | 类型写错 | 改成数组 |
| `periods 必须是不小于 1 的整数` | 课时数非法 | 填正整数 |
| `环节 id 重复` | 结构配置里重复 | 合并环节 |
| `required_stages 引用了未声明的环节` | 必填环节不在 `stages` 中 | 先声明再引用 |
| `映射包中不存在课题：L9` | `--lesson` 写错 | 用 `map list` 查看可用 id |

## 四、使用建议

- 一个映射包对应一个学科一个学期；单元与课题按教材顺序排列；
- 课标来源建议写「课标名称（版本）· 条目或主题」这种可核对的形式；
- 结构配置按学校 / 教研组统一维护，教案口径才可比。
