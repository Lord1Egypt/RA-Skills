---
name: siyuan-export
description: "思源笔记文档导出工具。将思源笔记文档导出为 Word(docx) 格式，支持按文档 ID/路径/名称搜索导出，图片自动打包进文档。支持单个文档导出和批量导出子文档。触发词：导出文档、导出 Word、siyuan export、思源导出、批量导出、导出子文档"
---

# 思源笔记文档导出 (siyuan-export)

通过思源笔记原生 API 将文档导出为 **Word(.docx)**，返回结构化 JSON 结果。支持单文档和批量子文档导出。

## 核心特性

| 特性 | 说明 |
|------|------|
| **双定位** | 支持文档 ID 或人类可读路径 |
| **批量导出** | `--children` 一键导出文档下所有子文档（含嵌套） |
| **单文件输出** | 图片资源自动内嵌（`removeAssets=true`），不产生外挂目录 |
| **JSON 输出** | 结构化结果，方便大模型解析 |
| **零依赖** | 仅使用 Python 标准库 |

## 前置条件

1. 思源笔记正在运行
2. 配置 Token

   **方式 A：环境变量（推荐）**
   ```bash
   # Windows PowerShell
   $env:SIYUAN_TOKEN = "你的token"
   $env:SIYUAN_BASE_URL = "http://127.0.0.1:6806"
   $env:SIYUAN_TIMEOUT = "10000"  # 可选，超时 ms
   ```

   **方式 B：config.json**（在技能目录下创建）
   ```json
   {
       "baseURL": "http://127.0.0.1:6806",
       "token": "你的token",
       "timeout": 10000
   }
   ```

   **方式 C：复制 config.example.json 重命名为 config.json**
   ```
   config.example.json → config.json
   ```
   然后填入 token

   Token 获取：思源笔记 → 设置 → 关于 → 复制 Token

## 使用方法

```bash
# 按文档名搜索导出（推荐）
python scripts/siyuan_export.py -s "关键词" -o C:/Desktop

# 按 ID 导出单个文档
python scripts/siyuan_export.py --doc-id <ID>

# 按路径导出
python scripts/siyuan_export.py --path "/AI/Test" --output C:/output

# 导出所有子文档
python scripts/siyuan_export.py --doc-id <ID> --children --output C:/Desktop/Midjourney
```

### 参数说明

| 参数 | 缩写 | 必选 | 说明 |
|------|------|:----:|------|
| `--doc-id` | `-i` | 二选一 | 文档 ID |
| `--path` | `-p` | 二选一 | 文档路径 |
| `--search` | `-s` | 二选一 | 按文档名搜索 |
| `--children` | `-c` | 否 | 批量模式：导出所有子文档 |
| `--include-self` | | 否 | 批量模式时同时导出父文档 |
| `--output` | `-o` | 否 | 输出目录（默认：桌面） |

## 返回值

### 单文档导出

成功：

```json
{
  "success": true,
  "data": {
    "path": "C:/Users/10941/Desktop/P02：设置解析.docx",
    "size_bytes": 3544783,
    "size_kb": 3461.7
  }
}
```

### 批量子文档导出

成功：

```json
{
  "success": true,
  "data": {
    "total": 16,
    "success_count": 16,
    "fail_count": 0,
    "output_dir": "C:/Users/10941/Desktop/Midjourney教程",
    "details": [
      {"id": "...", "title": "P01：认识界面", "result": {"success": true, "data": {"path": "...", "size_kb": 1234.5}}},
      ...
    ]
  }
}
```

失败：

```json
{
  "success": false,
  "error": "api_error",
  "message": "具体错误信息"
}
```

## API 接口

| 本脚本 | 思源 API | 参数 |
|--------|---------|------|
| 单文档导出 | `POST /api/export/exportDocx` | `id` + `savePath`（目录）+ `removeAssets=true` |
| 获取子文档列表 | `POST /api/query/sql` | SQL 查询 `hpath LIKE` 匹配子路径 |

## 文件结构

```
siyuan-export/
├── SKILL.md
├── config.example.json  # 配置模板（含 timeout 字段）
└── scripts/
    └── siyuan_export.py
```
