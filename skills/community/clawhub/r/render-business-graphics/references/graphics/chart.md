# 图表

## 请求外壳

```json
{
  "kind": "chart",
  "variant": "bar",
  "title": "各部门人员配置",
  "unit": "人",
  "data": [
    {"label": "研发部", "value": 24}
  ]
}
```

`kind`、`variant`、`data` 必填；`title`、`subtitle`、`unit`、`theme`、`page`、`rasterScale` 可选。具体部署是否公开其他字段，以单图 `parameters` 为准。

## 变体选择

| ID | 适用场景 | 关键规则 |
| --- | --- | --- |
| `chart.bar` | 离散分类比较 | 普通数值比较的默认选择 |
| `chart.line` | 时间或阶段趋势 | 只有确有连续趋势时使用 `smooth` |
| `chart.pie` | 单系列、非负构成比例 | 只能有一个系列，且至少一个正数 |
| `chart.radar` | 多维能力或质量画像 | 分类是能力维度，不是时间轴 |
| `chart.comparison` | 分类名称较长的横向对比 | 适合长标签 |
| `chart.funnel` | 转化、筛选、递减阶段 | 阶段应具有单向顺序 |
| `chart.matrix` | 分类 × 系列评分矩阵 | 所有单元格必须完整 |

## 数据规则

单系列：

```json
"data": [
  {"label": "需求分析", "value": 82},
  {"label": "方案设计", "value": 91}
]
```

多系列：

```json
"data": [
  {"label": "需求分析", "series": "流程规范", "value": 82},
  {"label": "需求分析", "series": "技术能力", "value": 76},
  {"label": "方案设计", "series": "流程规范", "value": 91},
  {"label": "方案设计", "series": "技术能力", "value": 89}
]
```

所有行必须统一包含或统一不包含 `series`；不能重复同一 `label + series`，不能把缺失单元随意补成 0。V2 不接受旧 V1 的 `categories`/`values` 平行数组。

## 限制和文字

一般图表最多 200 个分类、12 个系列；矩阵最多 144 行，最多 12 个分类和 12 个系列。分类标签建议 14 个字符以内，单位单独放 `unit`，不要把“24 人”整句放入 `label`。
