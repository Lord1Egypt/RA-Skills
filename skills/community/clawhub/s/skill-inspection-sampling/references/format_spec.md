# 检验抽样数据格式规范

## 目录
- [方案配置格式](#方案配置格式)
- [数据文件格式](#数据文件格式)
- [抽样结果格式](#抽样结果格式)
- [抽样记录格式](#抽样记录格式)
- [分析报告格式](#分析报告格式)

---

## 方案配置格式

### 简单随机抽样
```json
{
  "name": "simple_random_500",
  "type": "simple",
  "params": {
    "sample_size": 500
  }
}
```

### 分层抽样
```json
{
  "name": "stratified_by_category",
  "type": "stratified",
  "params": {
    "strata_field": "产品类别",
    "sample_size": 200,
    "allocation": "proportional"
  }
}
```

### 系统抽样
```json
{
  "name": "systematic_10pct",
  "type": "systematic",
  "params": {
    "sample_rate": 0.1,
    "interval": 10,
    "random_start": 1
  }
}
```

### 整群抽样
```json
{
  "name": "cluster_by_batch",
  "type": "cluster",
  "params": {
    "cluster_field": "批次号",
    "cluster_rate": 0.2
  }
}
```

---

## 数据文件格式

### CSV格式要求
- 编码:UTF-8或GBK
- 首行为表头
- 支持逗号、分号、制表符分隔
- 示例:
```csv
序号,产品名称,产品类别,检验项目,检验结果,批次号
001,产品A,A类,外观,合格,批次1
002,产品B,B类,尺寸,合格,批次1
003,产品C,A类,功能,不合格,批次2
```

### Excel格式要求
- 支持 .xlsx/.xls
- 读取第一个sheet
- 首行为表头
- 示例字段:序号、产品名称、检验项目、检验结果、检验日期

### JSON格式要求
- 数组格式或对象数组格式
```json
[
  {"序号": "001", "产品名称": "产品A", "检验结果": "合格"},
  {"序号": "002", "产品名称": "产品B", "检验结果": "不合格"}
]
```

---

## 抽样结果格式

```json
{
  "scheme_name": "simple_random_500",
  "scheme_type": "simple",
  "sampling_time": "2024-01-15T10:30:00",
  "data_summary": {
    "total_records": 10000,
    "fields": ["序号", "产品名称", "产品类别", "检验项目", "检验结果"]
  },
  "sampling_params": {
    "sample_size": 500,
    "method": "random_without_replacement"
  },
  "samples": [
    {"index": 0, "original_index": 156, "序号": "156", "产品名称": "产品X"},
    {"index": 1, "original_index": 892, "序号": "892", "产品名称": "产品Y"}
  ],
  "sample_count": 500,
  "sampling_rule": "从10000条记录中随机抽取500条，无放回抽样"
}
```

---

## 抽样记录格式

```json
{
  "record_id": "REC2024011500001",
  "scheme_name": "simple_random_500",
  "created_at": "2024-01-15T10:30:00",
  "operator": "system",
  "data_source": "./product_data.csv",
  "original_record_count": 10000,
  "sample_count": 500,
  "status": "completed",
  "log": [
    {"time": "10:30:00", "action": "load_scheme", "detail": "加载方案 simple_random_500"},
    {"time": "10:30:01", "action": "parse_data", "detail": "解析CSV文件，10000条记录"},
    {"time": "10:30:02", "action": "execute_sampling", "detail": "执行简单随机抽样"},
    {"time": "10:30:03", "action": "save_result", "detail": "保存抽样结果"}
  ]
}
```

---

## 分析报告格式

```json
{
  "report_id": "RPT2024011500001",
  "generated_at": "2024-01-15T11:00:00",
  "sample_source": "./sampling_result.json",
  "original_source": "./product_data.csv",
  "statistics": {
    "sample_count": 500,
    "original_count": 10000,
    "achievement_rate": 100.0
  },
  "field_analysis": {
    "检验结果": {
      "type": "categorical",
      "distribution": {
        "合格": 480,
        "不合格": 20
      },
      "missing_count": 0
    },
    "产品类别": {
      "type": "categorical",
      "distribution": {
        "A类": 180,
        "B类": 170,
        "C类": 150
      },
      "missing_count": 0
    }
  },
  "quality_assessment": {
    "coverage_rate": 100.0,
    "missing_rate": 0.0,
    "representativeness": "良好",
    "conclusion": "样本对总体具有良好的代表性，抽样质量满足检验要求"
  },
  "recommendations": [
    "本次抽样符合统计要求，可继续进行质量检验",
    "不合格品占比4%，建议重点关注"
  ]
}
```

---

## 验证规则

### 数据文件验证
- 文件必须存在且可读
- CSV/Excel:至少包含1行数据
- JSON:必须是数组且至少包含1个元素
- 数据行不能全部为空

### 方案参数验证
- sample_size:正整数，不超过总记录数
- sample_rate:0-1之间的浮点数
- strata_field:必须存在于数据字段中
- interval:正整数
- cluster_field:必须存在于数据字段中

### 抽样结果验证
- sample_count <= original_count
- 样本索引不重复（无放回抽样）
- 样本索引在有效范围内
