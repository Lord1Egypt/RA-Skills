# 示例2：报销单模板匹配与填充

## 场景
用户提供自己公司的报销单模板，Skill学习模板结构并自动填充数据。

## 输入
```
分析模板 D:\templates\公司报销单.xlsx
用模板 D:\templates\公司报销单.xlsx 生成报销单，数据来自 D:\invoices\receipt_001.json
```

## 处理步骤
1. `template_matcher.py analyze` 分析模板结构，识别表头字段
2. 自动匹配发票字段与模板字段（可手动确认/修正）
3. `template_matcher.py fill` 读取发票数据，按映射填充模板
4. 输出填充后的Excel文件

## 自动匹配结果示例
```json
{
  "template_path": "D:\\templates\\公司报销单.xlsx",
  "headers": [
    {"column": 1, "letter": "A", "value": "开票日期"},
    {"column": 2, "letter": "B", "value": "销方名称"},
    {"column": 3, "letter": "C", "value": "金额（不含税）"},
    {"column": 4, "letter": "D", "value": "税额"},
    {"column": 5, "letter": "E", "value": "价税合计"},
    {"column": 6, "letter": "F", "value": "费用说明"}
  ],
  "auto_matches": [
    {"invoice_field": "invoice_date", "template_field": "开票日期", "column": "A", "confidence": 1.0},
    {"invoice_field": "seller_name", "template_field": "销方名称", "column": "B", "confidence": 1.0},
    {"invoice_field": "amount", "template_field": "金额（不含税）", "column": "C", "confidence": 1.0},
    {"invoice_field": "tax_amount", "template_field": "税额", "column": "D", "confidence": 1.0},
    {"invoice_field": "total", "template_field": "价税合计", "column": "E", "confidence": 0.6},
    {"invoice_field": "remark", "template_field": "费用说明", "column": "F", "confidence": 0.8}
  ]
}
```

## 填充结果示例
```json
{
  "success": true,
  "output_path": "D:\\output\\expense_report_20260629_001541.xlsx",
  "filled_fields": 6,
  "filled_details": [
    {"field": "开票日期", "value": "2026年06月28日", "row": 2, "column": "A"},
    {"field": "销方名称", "value": "上海某某科技有限公司", "row": 2, "column": "B"},
    {"field": "金额（不含税）", "value": 10000.0, "row": 2, "column": "C"},
    {"field": "税额", "value": 1300.0, "row": 2, "column": "D"},
    {"field": "价税合计", "value": 11300.0, "row": 2, "column": "E"},
    {"field": "费用说明", "value": "*信息技术服务费*", "row": 2, "column": "F"}
  ]
}
```

## 命令
```bash
# 分析模板
python scripts/template_matcher.py analyze --template D:\templates\公司报销单.xlsx

# 填充报销单
python scripts/template_matcher.py fill --config config.yaml --receipt D:\invoices\receipt_001.json --template D:\templates\公司报销单.xlsx --output D:\output\报销单.xlsx

# 合并多张发票
python scripts/batch_process.py --input D:\invoices\ --template D:\templates\公司报销单.xlsx --output D:\output\合并报销单.xlsx
```

## 自适应学习
- 首次使用：自动匹配 + 用户确认
- 后续使用：自动应用已确认的映射
- 学习数据保存在 `template_cache.yaml`