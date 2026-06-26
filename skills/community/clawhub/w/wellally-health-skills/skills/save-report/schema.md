# 保存医疗检查单 Schema

医疗检查单保存的完整数据结构定义。

## 检查类型

| 类型 | subtype |
|-----|---------|
| 生化检查 | - |
| 影像检查 | B超/CT/MRI/X光/内窥镜/病理/心电图/乳腺钼靶/PET-CT |

## 生化检查字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 唯一标识符 |
| `date` | string | 检查日期 |
| `hospital` | string | 医院名称 |
| `original_image` | string | 原始图片路径 |
| `items[]` | array | 检查项目列表 |
| `items[].name` | string | 项目名称 |
| `items[].value` | string | 检查值 |
| `items[].unit` | string | 单位 |
| `items[].is_abnormal` | boolean | 是否异常 |

## 影像检查字段

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `id` | string | 唯一标识符 |
| `subtype` | enum | 检查子类型 |
| `body_part` | string | 检查部位 |
| `findings.description` | string | 检查所见 |
| `findings.targets[]` | array | 监测目标 |
| `findings.conclusion` | string | 检查结论 |

## 日期确定优先级

1. 用户提供的 exam_date（最高）
2. 图片采样时间
3. 图片送样时间
4. 图片检测时间/报告时间
5. 图片其他日期标识
6. 当前日期（最低）

## 数据存储

- 生化检查: `data/生化检查/YYYY-MM/YYYY-MM-DD_检查类型.json`
- 影像检查: `data/影像检查/YYYY-MM/YYYY-MM-DD_检查类型_检查部位.json`
- 原始图片: 对应目录下的 `images/` 子目录
