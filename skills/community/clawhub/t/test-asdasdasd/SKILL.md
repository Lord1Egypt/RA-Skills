---
name: extract-structured-data-from-document
description: 结构化字段抽取工具 - 基于用户定义的schema从文档中抽取结构化字段。schema定义要抽取的字段及其语义描述，支持文本、表格、段落三种类型的字段抽取。
metadata: {"openclaw": {"emoji": "🔍", "command-dispatch": "tool", "command-tool": "document_extract"}}
---

# 结构化字段抽取工具 (extract_structured_data_from_document)

## 概述

`extract_structured_data_from_document` 是一个**结构化字段抽取工具**，根据用户定义的schema从文档中抽取结构化数据。

**重要提示**：此工具专注于从文档中提取结构化字段，不适用于：
- 文档摘要生成
- 通用问答
- 文档结构解析

如需解析文档结构，请使用 `parse_document` 工具。

## 适用场景

- 从PDF/Word/Excel等文档中提取结构化数据
- 财务报表数据抽取（如营收、利润、资产负债表等）
- 合同关键条款提取
- 表单数据提取
- 任何需要从非结构化文档中提取结构化信息的任务

## 不适用场景

- 文档结构解析（请使用 `parse_document`）
- 文档摘要或总结
- 通用问答任务
- 无明确抽取目标的探索性分析

## 输入参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| document_url | string | 是 | 文档的URL地址，支持PDF、Word、Excel、图片等格式 |
| schema | object | 是 | 抽取规则定义，包含要抽取的字段及语义描述 |

`document_url` 既可以是公网可访问的文件 URL，也可以是本地文件路径。
当传入本地路径时，工具会先上传到 DPA 文档里指定的文件服务，再调用字段抽取接口。

### 环境变量

- `DPA_ENV`: `sim` 或 `prod`，默认 `sim`
- `DPA_BASE_URL`: 可选，自定义覆盖解析服务地址
- `DPA_UPLOAD_URL`: 可选，自定义覆盖文件上传地址

默认端点：

- 仿真环境：`http://imsfz.gjzq.cn:18087/ismp/yx-dpa/document`
- 仿真上传：`http://imsfz.gjzq.cn:18087/ismp/yx-gw/infras/file/file/v3/upload`
- 生产环境：`http://ims.gjzq.cn:18087/ismp/yx-dpa/document`
- 生产上传：`http://ims.gjzq.cn:18087/ismp/yx-gw/infras/file/file/v3/upload`

### Schema结构

schema是一个JSON对象，支持三种字段类型：

```json
{
  "text": [
    {
      "keyName": "字段名称",
      "keyPrompt": "字段的语义描述和抽取要求"
    }
  ],
  "table": [
    {
      "tableName": "表格名称",
      "tableDescription": "表格的描述信息",
      "tableColumn": [
        {
          "keyName": "列名称",
          "keyPrompt": "列的语义描述和抽取要求"
        }
      ]
    }
  ],
  "paragraph": [
    {
      "keyName": "段落名称",
      "keyPrompt": "段落的语义描述和抽取要求"
    }
  ]
}
```

## 关键使用规则

### ⚠️ 必须先构造Schema

**如果用户没有提供schema，必须先根据用户需求构造schema，然后再调用此工具。**

LLM负责：
1. 理解用户的抽取需求
2. 将需求转换为符合格式的schema定义
3. 调用此工具执行抽取

### Schema构造原则

1. **keyName**: 字段的标识名称，应简洁明了
2. **keyPrompt**: 字段的详细描述，包含：
   - 字段的含义
   - 数据格式要求（如"输出纯数字"、"带单位"等）
   - 来源说明（如"从合并资产负债表提取"）
   - 特殊处理要求（如"取绝对值"、"单位转换"等）

## 输出格式

返回JSON格式的结构化抽取结果，包含：
- 文本字段的抽取值和溯源信息
- 表格数据的二维数组结构
- 段落内容的完整文本
- 每个抽取结果的来源页码和坐标信息

## ⚠️ 执行模式

此工具提交的是 DPA 文档规定的异步字段抽取任务：先调用 `POST /parse` 获取 `taskId`，然后轮询 `GET /{taskId}/status`，成功后再读取 `GET /{taskId}/result`。

为了便于上层调用，工具默认会在本地帮你等待完成后直接返回结果（包含 `data` 中的 `text`、`table`、`paragraph`）。

**注意**：默认等待超时为 **60 秒**。如果文档较大、60 秒内未完成，工具会返回 `taskId`、当前 `status` 和提示信息，供后续继续查询。

也可以传入 `async` 模式立即返回 taskId，手动查询结果。

### 步骤1：获取 taskId（async模式）

工具返回格式：
```json
{
  "taskId": "202603251633-8e44b4a2",
  "taskType": "extraction",
  "message": "字段抽取任务已创建"
}
```

**重要**：请记录返回的 `taskId`，用于后续查询任务状态和结果。

### 步骤2：查询任务状态

使用 `document_get_result` 工具查询抽取结果：

```json
{
  "tool": "document_get_result",
  "args": {
    "task_id": "202603251633-8e44b4a2"
  }
}
```

### 步骤3：解析结果

成功时返回的结构：
```json
{
  "code": 200,
  "message": "检索成功，召回内容已返回。",
  "data": {
    "text": [
      {
        "keyName": "本期营业收入",
        "keyValue": "500亿元",
        "source": {
          "docUrl": "https://example.com/report.pdf",
          "pageNum": 3,
          "bbox": [100, 200, 300, 250]
        }
      }
    ],
    "table": [...],
    "paragraph": [...]
  }
}
```

### 完整调用流程示例

1. **调用 extract_structured_data**：
```
输入: /path/to/document.pdf, schema={...}
返回: {"taskId": "202603251633-abc123", "taskType": "extraction", "message": "字段抽取任务已创建"}
```

2. **查询结果**：
```
输入: task_id="202603251633-abc123"
返回: {"code": 200, "data": {"text": [...], "table": [...], "paragraph": [...]}}
```

### 返回字段说明

| 字段 | 类型 | 描述 |
|------|------|------|
| taskId | string | 任务ID，用于查询任务状态 |
| taskType | string | 任务类型，"extraction" 表示字段抽取任务 |
| message | string | 任务状态描述 |
| data.text | array | 文本字段抽取结果列表 |
| data.table | array | 表格抽取结果列表 |
| data.paragraph | array | 段落抽取结果列表 |

## 调用示例

### 示例1：用户直接给抽取需求（无schema）

**用户请求**：
```
请从这份年报中提取公司的营业收入、去年同期营业收入、本期营业费用等信息
```

**LLM首先构造Schema**：
```json
{
  "text": [
    {
      "keyName": "本期营业收入",
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
    },
    {
      "keyName": "去年同期营业收入",
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
    },
    {
      "keyName": "本期营业费用",
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
    },
    {
      "keyName": "去年同期营业费用",
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
    }
  ],
  "table": [],
  "paragraph": []
}
```

**然后调用工具**：
```json
{
  "tool": "extract_structured_data_from_document",
  "args": {
    "document_url": "https://example.com/annual_report_2024.pdf",
    "schema": {
      "text": [
        {
          "keyName": "本期营业收入",
          "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
        },
        {
          "keyName": "去年同期营业收入",
          "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
        },
        {
          "keyName": "本期营业费用",
          "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
        },
        {
          "keyName": "去年同期营业费用",
          "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元"
        }
      ],
      "table": [],
      "paragraph": []
    }
  }
}
```

**工具返回**：
```json
{
  "text": [
    {
      "keyName": "本期营业收入",
      "keyValue": "500亿元",
      "source": {
        "docUrl": "https://example.com/annual_report_2024.pdf",
        "pageNum": 3,
        "bbox": [100, 200, 300, 250]
      }
    },
    {
      "keyName": "去年同期营业收入",
      "keyValue": "420亿元",
      "source": {
        "docUrl": "https://example.com/annual_report_2024.pdf",
        "pageNum": 3,
        "bbox": [100, 260, 300, 310]
      }
    }
  ],
  "table": [],
  "paragraph": []
}
```

### 示例2：复杂文档 - 表格数据抽取

**用户请求**：
```
从这份银行资产负债表中提取同业存放的数据，包括本期和去年年底的数值
```

**LLM构造Schema**：
```json
{
  "text": [],
  "table": [
    {
      "tableName": "合并及银行资产负债表",
      "tableDescription": "银行合并及本身的资产负债表",
      "tableColumn": [
        {
          "keyName": "序号",
          "keyPrompt": "依据表格顺序增加序号，如1,2,3,4"
        },
        {
          "keyName": "项目",
          "keyPrompt": "仅采集下述项目：同业存放"
        },
        {
          "keyName": "项目值",
          "keyPrompt": "不同年份的项目值按照年份紧邻排列，如果某一年为空值也按空值输出，输出纯数字，且取绝对值"
        },
        {
          "keyName": "所属时期",
          "keyPrompt": "从下述选择项目所属时期：本期、去年同期、前年同期、去年年底、前年年底"
        },
        {
          "keyName": "年份",
          "keyPrompt": "项目值对应时间，包括年份、月份、日期等"
        },
        {
          "keyName": "单位",
          "keyPrompt": "项目单位，比如：亿元、百万元、元等"
        }
      ]
    }
  ],
  "paragraph": []
}
```

**调用工具**：
```json
{
  "tool": "extract_structured_data_from_document",
  "args": {
    "document_url": "https://example.com/bank_balance_sheet.pdf",
    "schema": {
      "table": [
        {
          "tableName": "合并及银行资产负债表",
          "tableDescription": "银行合并及本身的资产负债表",
          "tableColumn": [
            {"keyName": "序号", "keyPrompt": "依据表格顺序增加序号，如1,2,3,4"},
            {"keyName": "项目", "keyPrompt": "仅采集下述项目：同业存放"},
            {"keyName": "项目值", "keyPrompt": "输出纯数字，且取绝对值"},
            {"keyName": "所属时期", "keyPrompt": "从下述选择：本期、去年同期、前年同期、去年年底"},
            {"keyName": "年份", "keyPrompt": "项目值对应时间"},
            {"keyName": "单位", "keyPrompt": "项目单位"}
          ]
        }
      ]
    }
  }
}
```

### 示例3：用户已提供Schema

**用户请求**：
```
请使用以下schema从文档中提取数据：
- 本期营业收入（单位：亿元）
- 去年同期营业收入（单位：亿元）
- 董事会制度（段落内容）
```

**由于用户已提供schema，直接调用**：
```json
{
  "tool": "extract_structured_data_from_document",
  "args": {
    "document_url": "https://example.com/company_report.pdf",
    "schema": {
      "text": [
        {
          "keyName": "本期营业收入",
          "keyPrompt": "输出纯数字，单位亿元"
        },
        {
          "keyName": "去年同期营业收入",
          "keyPrompt": "输出纯数字，单位亿元"
        }
      ],
      "paragraph": [
        {
          "keyName": "董事会制度",
          "keyPrompt": "公司的董事会制度相关信息"
        }
      ],
      "table": []
    }
  }
}
```

## 完整Schema示例

以下是一个完整的schema示例，涵盖文本、表格和段落三种类型：

```json
{
  "paragraph": [
    {
      "keyName": "财务会计制度、利润分配和审计",
      "keyPrompt": "公司的财务会计制度、利润分配和审计相关信息"
    },
    {
      "keyName": "董事会制度",
      "keyPrompt": "公司的董事会制度相关信息"
    }
  ],
  "text": [
    {
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元",
      "keyName": "本期营业收入"
    },
    {
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元",
      "keyName": "去年同期营业收入"
    },
    {
      "keyPrompt": "输出纯数字，且取绝对值。必须带上单位。若项目值单位是百万元，需要转换为亿元",
      "keyName": "本期营业费用"
    }
  ],
  "table": [
    {
      "tableName": "合并及银行资产负债表",
      "tableDescription": "",
      "tableColumn": [
        {
          "keyPrompt": "依据表格顺序增加序号，如1,2,3,4",
          "keyName": "序号"
        },
        {
          "keyPrompt": "仅采集下述项目：同业存放",
          "keyName": "项目"
        },
        {
          "keyPrompt": "输出纯数字，且取绝对值",
          "keyName": "项目值"
        },
        {
          "keyPrompt": "从下述选择：本期、去年同期、前年同期、去年年底",
          "keyName": "所属时期"
        },
        {
          "keyPrompt": "项目值对应时间",
          "keyName": "年份"
        },
        {
          "keyPrompt": "项目单位",
          "keyName": "单位"
        }
      ]
    }
  ]
}
```

## 工具定义

```json
{
  "name": "extract_structured_data_from_document",
  "description": "结构化字段抽取工具 - 基于schema从文档中抽取结构化字段，支持文本、表格、段落三种类型",
  "parameters": {
    "type": "object",
    "properties": {
      "document_url": {
        "type": "string",
        "description": "文档的URL地址，支持PDF、Word、Excel、图片等格式"
      },
      "schema": {
        "type": "object",
        "description": "抽取规则定义，必须包含text、table、paragraph三个字段，每个字段都是数组",
        "properties": {
          "text": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "keyName": {"type": "string"},
                "keyPrompt": {"type": "string"}
              },
              "required": ["keyName", "keyPrompt"]
            }
          },
          "table": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tableName": {"type": "string"},
                "tableDescription": {"type": "string"},
                "tableColumn": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "keyName": {"type": "string"},
                      "keyPrompt": {"type": "string"}
                    },
                    "required": ["keyName", "keyPrompt"]
                  }
                }
              },
              "required": ["tableName", "tableDescription", "tableColumn"]
            }
          },
          "paragraph": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "keyName": {"type": "string"},
                "keyPrompt": {"type": "string"}
              },
              "required": ["keyName", "keyPrompt"]
            }
          }
        },
        "required": ["text", "table", "paragraph"]
      }
    },
    "required": ["document_url", "schema"]
  }
}
```
