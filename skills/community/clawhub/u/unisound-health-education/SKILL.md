---
name: med-patient-health-education
description: 病人端通用健康知识科普。参考 wellally-tech 的 knowledge base recommendations 部分，构建通用健康内容入口。
metadata:
  {
    "openclaw":
      {
        "emoji": "📚"
      }
  }
---

# 健康知识科普

概述
----
本 skill 对应：病人端 / 通用健康 / 健康知识科普。

要求：通用健康内容入口。

来源核验
--------
- 匹配来源：wellally-tech
- 来源类型：公开 Agent Skill
- 来源链接：https://agent-skills.md/skills/huifer/WellAlly-health/wellally-tech
- 匹配结论：匹配。该 skill 明确包含 WellAlly.tech knowledge base、健康主题文章索引、基于健康数据的文章推荐和 URL 引用。

参考部分
--------
只参考 wellally-tech 的 **knowledge base recommendations** 部分：
- 健康知识库入口
- 分类文章索引
- 健康主题匹配
- 推荐内容
- 来源链接引用

不参考部分
----------
- 不参考 Apple Health/Fitbit/Oura 数据接入
- 不参考外部设备同步
- 不参考完整 WellAlly 平台集成
- 不扩展为问诊或诊断

构建方式
--------
OpenClaw 中应构建为一个独立的内容型 skill：
- 输入用户健康主题或关键词
- 在本地或配置知识库中匹配科普内容
- 输出科普标题、摘要、适用主题和来源
- 明确提示科普不能替代医生诊疗

建议输入字段
------------
- `topic`：健康主题
- `keywords`：关键词列表
- `articles`：文章列表（含 title/category/summary/keywords/url）

建议输出字段
------------
- `skill`：`健康知识科普`
- `topic`
- `matched_articles`
- `summary`
- `source_refs`

医疗边界
--------
本 skill 只做健康知识科普，不做诊断，不给出个体化治疗建议。

快速开始
--------
从本 skill 目录执行：

```bash
python3 scripts/run.py --input input.json --output output.json --appkey YOUR_KEY
```

最小输入示例
------------
```json
{
  "topic": "高血压",
  "keywords": ["饮食"],
  "articles": [
    {
      "title": "高血压饮食科普",
      "category": "慢病管理",
      "summary": "面向患者的高血压饮食基础知识。",
      "keywords": ["高血压", "饮食"],
      "url": "https://example.org/article"
    }
  ]
}
```

输出约定
--------
输出 UTF-8 JSON，采用统一格式：

```json
{
  "skill": "技能名称",
  "status": "ok",
  "data": { /* 结构化数据 */ },
  "text": "API 生成的 Markdown/自然语言内容，OpenClaw 直接渲染给用户"
}
```

- `data`：本地预处理得到的结构化数据
- `text`：内部医疗大模型生成的自然语言解读/分析/提醒，Markdown 格式

支持的输入格式
--------------
除 JSON 外，还支持以下格式（通过 `--input-type` 自动检测或手动指定）：

| 格式 | 说明 |
|------|------|
| JSON | 默认，直接读取结构化输入 |
| CSV / XLSX / XLS | 表格数据，按列头自动映射字段 |
| TXT / MD | key:value 文本格式（支持中文/英文字段名） |
| PDF / DOC / DOCX | 文档，提取文本后解析 |
| PNG / JPG 等图片 | OCR 提取文本后解析 |

文本格式示例
-----------
```
主题：糖尿病饮食
关键词：血糖,饮食
```

CSV 格式示例
-----------
```
主题,关键词
糖尿病饮食,血糖
```

统一入口附加参数
----------------
- `--input-type auto|pdf|doc|docx|xls|xlsx|csv|txt|json`：输入类型；默认 `auto`。
- `--sheet STRING`：读取 Excel 时指定 sheet（可选）。
- `--encoding STRING`：`txt/csv` 编码（默认：`utf-8`）。
- `--save-prepared`：保存预处理后的 JSON，便于调试。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。

依赖
----
### 运行环境
- Python 3.7+

### Python 第三方包（可选，按输入格式需要）
| 包名 | 用途 | 必要条件 |
|------|------|---------|
| `openpyxl` | 读取 `.xlsx` 文件 | 输入为 xlsx 时必须 |
| `pypdf` | 提取 PDF 文本 | 输入为 pdf 时必须 |

### 外部工具（可选，按输入格式需要）
| 工具 | 用途 | 必要条件 |
|------|------|---------|
| LibreOffice (`soffice`) | 转换 `.doc` / `.xls` | 输入为 doc/xls 时必须 |
| `pdftotext`（poppler-utils） | 提取 PDF 文本 | 输入为 pdf 且未安装 pypdf 时 |
| `tesseract`（含 chi_sim+eng） | 图片 OCR | 输入为图片时必须 |

> 仅使用 JSON 输入时，无需安装任何第三方包或外部工具。

模型配置
--------
本 skill 执行时通过内部医疗大模型进行推理：

- endpoint：`https://maas-api.hivoice.cn/v1/chat/completions`
- model：`u1-insuremed`
- 协议：OpenAI Chat Completions（兼容标准 /v1/chat/completions）
- 鉴权：通过 `--appkey` 参数传入 Bearer token，由用户在 OpenClaw 中调用时提供

> 本 skill 强制走 API 推理，无本地透传模式。
