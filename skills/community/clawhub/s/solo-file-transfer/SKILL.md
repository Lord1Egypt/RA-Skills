---
name: file-transfer
description: |
  文件传输技能 — 合并docx-to-md + ima-knowledge-upload。
  (1) Word文档(.docx)转Markdown并提取图片
  (2) 上传文件/网页/笔记到IMA知识库
  (3) 链式操作：docx→md→IMA一键上传
  Use when: 用户需要文档格式转换、文件上传到知识库、Word转Markdown、上传报告到IMA。
metadata:
  openclaw:
    emoji: 📤
    requires:
      python: "3.7+"
      pip: ["python-docx"]
      env: ["IMA_OPENAPI_CLIENTID", "IMA_OPENAPI_APIKEY"]
---

# file-transfer 📤

> docx→md + IMA上传。二合一。

## 模块 A：docx → Markdown

将Word文档(.docx)转换为Markdown格式，提取图片。

```python
import sys
sys.path.insert(0, '<skill_dir>/scripts')
from docx_to_md import docx_to_md
docx_to_md('文件.docx', '输出目录')
```

**转换规则：** 标题(#)→列表(-/1.)→表格→图片(![])

## 模块 B：IMA知识库上传

向指定知识库上传文件，完整流程：`check_repeated_names` → `create_media` → COS上传 → `add_knowledge`。

```bash
SKILL_DIR=<skill_dir>
OPTS=$(printf '{"clientId":"%s","apiKey":"***"}' "$IMA_OPENAPI_CLIENTID" "$IMA_OPENAPI_APIKEY")
node "$SKILL_DIR/scripts/ima_api.cjs" "<api_path>" '<json_body>' "$OPTS"
```

**核心API路径：**
| 操作 | api_path | 关键参数 |
|:-----|:---------|:---------|
| 搜索知识库 | `openapi/wiki/v1/search_knowledge_base` | `query`, `cursor` |
| 获取知识库信息 | `openapi/wiki/v1/get_knowledge_base` | `ids` |
| 创建媒体 | `openapi/wiki/v1/create_media` | `file_name`, `file_size`, `knowledge_base_id` |
| COS上传 | `scripts/cos-upload.cjs` | `--file --secret-id --secret-key --token --bucket --region --cos-key` |
| 添加知识 | `openapi/wiki/v1/add_knowledge` | `media_type`, `media_id`, `title`, `knowledge_base_id` |
| 添加网页 | `openapi/wiki/v1/import_urls` | `urls`, `knowledge_base_id` |
| 浏览知识库 | `openapi/wiki/v1/get_knowledge_list` | `knowledge_base_id`, `cursor` |

**上传文件流程：**
1. `check_repeated_names` — 检查重名
2. `create_media` — 获取上传凭证
3. `scripts/cos-upload.cjs` — COS上传 ⚠️ 非零退出=停止
4. `add_knowledge` — 添加知识 ⚠️ title必须等于file_name

## 模块 C：链式操作

docx → md → IMA上传一体：

```
① docx_to_md.py 转换 → 得到 .md + images/
② ima_api.cjs create_media → COS upload → add_knowledge
③ 返回知识库链接
```

## 依赖

- Python 3.7+, python-docx
- Node.js（ima_api.cjs）
- 环境变量: `IMA_OPENAPI_CLIENTID`, `IMA_OPENAPI_APIKEY`
