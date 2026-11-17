# 报价数据规范

## 物料价格表（用户上传）

用户上传的物料价格表可以是 Excel（.xlsx/.xls）或 CSV（.csv），格式灵活，系统通过关键词自动识别字段。

### 支持的原始格式示例

**格式A：标准三列表**
```
产品名称    规格型号    单价
键盘        蓝牙        400
键盘        机械        200
鼠标        无线鼠标    100
```

**格式B：含单位列**
```
物料名称    型号        单位    零售价(元)
六类网线    大华        箱      800
400万摄像枪  常规        台      100
```

**格式C：多行表头**
```
商品报价清单
产品名称    规格        单价
键盘        蓝牙        400
```

### 字段识别关键词映射

系统通过以下关键词（不区分大小写，支持部分匹配）自动识别列：

| 标准字段名 | 匹配关键词（任一命中即可） |
|-----------|--------------------------|
| materialName | 产品名称、品名、物料、物料名称、商品名称、产品、名称、Name |
| specModel | 规格、型号、规格型号、Spec、Model |
| retailPrice | 单价、价格、零售价、金额、单价(元)、价格(元)、零售价(元)、Price、Unit Price |
| unit | 单位、计量单位、Unit |
| remark | 备注、Note、说明 |

> **注意**：原始表头可能有合并单元格，系统会将其展开到每个子单元格后再匹配。

---

## 解析后的标准化物料清单 (materialPrices.json)

经过解析和清洗后的统一格式：

```json
[
  {
    "id": "MAT-001",
    "materialName": "键盘",
    "specModel": "蓝牙",
    "retailPrice": 400.0,
    "unit": "个",
    "remark": ""
  },
  {
    "id": "MAT-002",
    "materialName": "键盘",
    "specModel": "机械",
    "retailPrice": 200.0,
    "unit": "个",
    "remark": ""
  }
]
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 自动生成的唯一标识（MAT-XXX） |
| materialName | string | 是 | 产品名称（清洗后） |
| specModel | string | 是 | 规格/型号（清洗后） |
| retailPrice | number | 是 | 零售价/单价（转数值型） |
| unit | string | 否 | 计量单位，未识别时默认为空 |
| remark | string | 否 | 备注 |

**关键规则**：同一个 `materialName` 可能对应多个 `specModel`，生成报价前必须先向用户确认具体型号。

---

## 模板分析输出 (template_analysis.json)

分析用户上传的任意 Excel 报价模板后的结构化输出：

```json
{
  "schema_version": "1.0",
  "template_id": "template_20250711_001",
  "analyzed_at": "2025-07-11T10:00:00Z",
  "file_info": {
    "original_file": "/path/to/用户模板.xlsx",
    "sheet_name": "Sheet1",
    "total_rows": 50,
    "total_cols": 10
  },
  "regions": {
    "quotation_list": {
      "type": "list",
      "description": "报价明细表",
      "start_row": 8,
      "data_start_row": 9,
      "template_rows": 3,
      "max_rows": 20,
      "columns": {
        "A": {
          "field": "line_no",
          "header_text": "序号",
          "type": "number",
          "has_formula": false
        },
        "B": {
          "field": "product_name",
          "header_text": "产品名称",
          "type": "string",
          "has_formula": false
        },
        "C": {
          "field": "specification",
          "header_text": "规格型号",
          "type": "string",
          "has_formula": false
        },
        "D": {
          "field": "unit",
          "header_text": "单位",
          "type": "string",
          "has_formula": false
        },
        "E": {
          "field": "quantity",
          "header_text": "数量",
          "type": "number",
          "has_formula": false
        },
        "F": {
          "field": "unit_price",
          "header_text": "单价",
          "type": "currency",
          "has_formula": false
        },
        "G": {
          "field": "total_price",
          "header_text": "金额",
          "type": "currency",
          "has_formula": true,
          "formula_template": "=E{row}*F{row}"
        }
      },
      "style_reference_row": 9,
      "summary_row": null,
      "constraints": {
        "auto_expand": false,
        "insert_row_keep_style": false,
        "preserve_formulas": ["G"]
      }
    },
    "customer_info": {
      "type": "single_value",
      "description": "客户信息区",
      "cells": {
        "customer_name": {
          "cell": "C3",
          "type": "string",
          "required": true,
          "current_value": ""
        },
        "quotation_date": {
          "cell": "C4",
          "type": "date",
          "format": "YYYY-MM-DD",
          "required": true,
          "current_value": "2025-07-01"
        },
        "quotation_no": {
          "cell": "H3",
          "type": "string",
          "required": false,
          "current_value": "Q2025001"
        },
        "total_amount": {
          "cell": "G25",
          "type": "currency",
          "has_formula": true,
          "formula_managed": true,
          "current_value": ""
        }
      }
    }
  },
  "warnings": []
}
```

### 单值区域标签识别关键词

| 标准字段名 | 匹配关键词（标签文本中任一命中） |
|-----------|------------------------------|
| customer_name | 客户、甲方、买方、客户名称、客户名、Customer |
| quotation_date | 日期、报价日期、填表日期、Date |
| quotation_no | 单号、报价单号、编号、No、编号 |
| contact_phone | 电话、联系电话、手机、Tel、Phone |
| total_amount | 总计、合计、总金额、总价、Total、Amount |
| remark | 备注、说明、Note、Remarks |

---

## 填充数据 (fill_operations)

由计算步骤生成，供文档生成步骤读取：

```json
{
  "fill_operations": {
    "data": [
      {
        "row": 9,
        "col": "B",
        "value": "键盘",
        "region": "quotation_list"
      },
      {
        "row": 9,
        "col": "C",
        "value": "蓝牙",
        "region": "quotation_list"
      },
      {
        "row": 9,
        "col": "E",
        "value": 1,
        "region": "quotation_list"
      },
      {
        "row": 9,
        "col": "F",
        "value": 400,
        "region": "quotation_list"
      },
      {
        "row": 3,
        "col": "C",
        "value": "张三科技有限公司",
        "region": "customer_info"
      },
      {
        "row": 4,
        "col": "C",
        "value": "2025-07-11",
        "region": "customer_info"
      }
    ]
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| row | int | 行号（从1开始） |
| col | string | 列字母（A, B, C...） |
| value | string/number | 填充值 |
| region | string | 所属区域（quotation_list / customer_info） |

---

## 列字段映射标准（模板分析阶段）

模板分析时，根据表头文本自动映射到标准字段名：

| 表头关键词 | 映射字段名 |
|-----------|-----------|
| 序号 / No. / 编号 | line_no |
| 产品名称 / 品名 / 物料 / 名称 | product_name |
| 规格 / 型号 / 规格型号 / Spec | specification |
| 单位 / Unit / 计量单位 | unit |
| 数量 / Qty / 个数 | quantity |
| 单价 / Price / Amount / 价格 | unit_price |
| 金额 / 小计 / Total / 合计 | total_price |
| 备注 / Note / 说明 | remark |
