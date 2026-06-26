# Web of Science 高级检索指南

## 检索字段代码

| 代码 | 含义 | 示例 |
|------|------|------|
| TS | 主题（标题+摘要+关键词） | TS=(environmental psychology) |
| TI | 标题 | TI=(restorative environment) |
| AU | 作者 | AU=(Kaplan S) |
| SO | 出版物/期刊 | SO=(Journal of Environmental Psychology) |
| PY | 出版年份 | PY=(2020-2024) |
| AB | 摘要 | AB=(nature exposure) |
| KP | 关键词 | KP=(green space) |
| DO | DOI | DO=(10.1016/j.jenvp.2020.101456) |
| WC | Web of Science 类别 | WC=(Psychology Multidisciplinary) |
| AD | 地址/机构 | AD=(University of Michigan) |

## 布尔运算符

- **AND** - 同时包含所有词
- **OR** - 包含任一词语
- **NOT** - 排除特定词
- **NEAR/n** - 两词相距n个词以内
- **SAME** - 同一字段中

## 检索式示例

### 恢复性环境
```
TS=("attention restoration theory" OR "stress recovery theory" OR "restorative environment*") AND TS=(health OR well-being OR wellbeing)
```

### 绿色空间与心理健康（限定年份）
```
TS=("green space" OR "greenspace" OR "urban nature" OR "park access") AND TS=("mental health" OR depression OR anxiety OR stress) AND PY=(2015-2024)
```

### 特定作者的研究
```
AU=(Kaplan R OR Kaplan S) AND TS=(restorative OR nature)
```

### 特定期刊
```
SO=("Journal of Environmental Psychology") AND TS=(restorative)
```

## 通配符

- **\*** - 零个或多个字符（如 `restor*` 匹配 restore, restorative, restoration）
- **?** - 单个字符（如 `wom?n` 匹配 woman, women）
- **$** - 零个或一个字符（如 `colo$r` 匹配 color, colour）

## 短语检索

使用引号进行精确短语匹配：
```
"attention restoration theory"
```

## 导出设置建议

1. **记录内容**: 选择「全记录与引用的参考文献」获取完整信息
2. **文件格式**: 选择「制表符分隔的 UTF-8 格式」便于程序解析
3. **排序**: 按「被引频次（降序）」获取高影响力文献

## 检索结果精炼

在左侧精炼面板中可按以下维度筛选：
- 研究领域
- 文献类型（Article, Review 等）
- 出版年份
- 期刊
- 作者
- 机构
- 开放获取
