---
name: docparse
description: "Trigger when user mentions OCR/文档解析/阅读/识别/读取 or asks to extract text from documents. Parses PDF/images via remote document parsing service. NOT for audio/video/photos/source code."
metadata:
  openclaw:
    emoji: "📄"
    install:
      packages:
        - name: fastmcp
          manager: pip
        - name: mcp
          manager: pip
---
# 文档解析 Skill

通过 MCP Server 调用远程文档解析服务，提取 PDF/图片中的文字、表格和公式。

## 触发条件

用户提到 OCR、文档解析、阅读、识别、读取，或要求从文档中提取文字时触发。

## 运行环境（首次执行）

- **Python 版本**：Python 3.10 或更高版本
- **依赖安装**：

  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

  或手动安装：

  ```bash
  pip install fastmcp>=3.0.0 mcp>=1.0.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

## 支持格式

- PDF、扫描版 PDF
- PNG、JPG、JPEG
- 不支持：音频、视频、风景照、人物照、Word/Excel/PPT（需先转 PDF）

## MCP Server 配置

### 方式一：作为 OpenClaw Gateway 内置 MCP Server 使用（首次执行）

在 OpenClaw Gateway 寻找 `docparse`服务，类似配置如下：

```json5
{
  mcpServers: {
    docparse: {
      command: "python",
      args: ["/path/to/.openclaw/workspace/skills/docparse/mcp/docparse.py"],
      env: {
        DOCPARSE_MCP_URL: "http://<host>:<port>/mcp",
        DOCPARSE_API_KEY: "your-api-key",
        DOCPARSE_TIMEOUT: "7200",
      },
    },
  },
}
```

或使用 `openclaw mcp set` 命令配置：

```bash
openclaw mcp set docparse '{
  "command": "python",
  "args": ["/path/to/.openclaw/workspace/skills/docparse/mcp/docparse.py"],
  "env": {
    "DOCPARSE_MCP_URL": "http://<host>:<port>/mcp",
    "DOCPARSE_API_KEY": "your-api-key",
    "DOCPARSE_TIMEOUT": "7200"
  }
}'
```

环境变量说明：

- `DOCPARSE_MCP_URL`：远程文档解析 MCP 服务地址（必需）
- `DOCPARSE_API_KEY`：API 密钥（可选）
- `DOCPARSE_TIMEOUT`：超时时间，单位秒（可选，默认 7200）

配置优先级（从高到低）（首次执行需查询环境变量是否已配置）：

1. **进程环境变量** (`os.environ`) — 最高优先级
2. **`openclaw.json`** 的 `mcp.servers.docparse.env`
3. **`.env`** 文件（skill 目录下）— 最低优先级

> 高层级配置自动覆盖低层级，无需手动同步。

### 方式二：作为独立 MCP Server 进程使用

也可以直接运行 MCP Server（需使用 venv 中的 Python）：

```bash
export DOCPARSE_MCP_URL="http://<host>:<port>/mcp"
export DOCPARSE_API_KEY="your-api-key"
python /path/to/.openclaw/workspace/skills/docparse/mcp/docparse.py
```

Server 通过 stdio 与 MCP 客户端通信。

### 提供的 Tool

#### `parse_document`

解析指定路径的文档，返回提取的文本内容。

**参数：**

| 参数              | 类型   | 必填 | 说明                                               |
| ----------------- | ------ | ---- | -------------------------------------------------- |
| `file_path`     | string | 是   | 待解析文件的绝对路径                               |
| `output_format` | string | 否   | 输出格式：`markdown`（默认）、`json`、`both` |

**返回：**

- 成功：返回解析后的文本内容（Markdown 或 JSON 格式）
- 失败：返回带错误代号的错误信息

### 兼容旧版直接导入接口

如需在 Python 代码中直接调用（兼容旧版 `mcp/docparse.py` 的用法）：

```python
import sys
sys.path.insert(0, "/path/to/.openclaw/workspace/skills/docparse")
from mcp.docparse import parse_document_return
```

### 错误代号

| 代号       | 场景              | 用户提示                                                                                                                  |
| ---------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `[F001]` | 文件不存在        | 解析失败：未找到待解析文件。建议：请确认文件是否已上传，或检查文件路径是否正确。                                          |
| `[F002]` | 文件不可读        | 解析失败：当前文件无法读取。建议：请检查文件权限后重试。                                                                  |
| `[F003]` | 格式不支持        | 解析失败：当前文件格式不支持文档解析。支持格式：PDF、PNG、JPG、JPEG、BMP、WEBP、TIFF。建议：请先将文件转换为 PDF 后重试。 |
| `[C001]` | 配置缺失          | 解析失败：文档解析服务当前不可用。建议：请联系管理员检查解析服务配置后重试。                                              |
| `[A001]` | MCP 认证/连接异常 | 解析失败：文档解析服务当前不可用。建议：请联系管理员检查解析服务配置后重试。                                              |
| `[N001]` | 网络连接失败      | 解析失败：文档解析服务当前不可用。建议：请稍后重试，或联系管理员检查服务状态。                                            |
| `[S001]` | 服务返回空        | 解析失败：文档解析服务未返回有效内容。建议：请确认文件内容清晰后重试。                                                    |
| `[S002]` | 响应解析失败      | 解析失败：文档结果解析异常。建议：请稍后重试，或联系管理员检查解析服务。                                                  |
| `[S003]` | 服务返回错误      | 解析失败：文档解析服务返回异常。建议：请稍后重试，或联系管理员检查解析服务。                                              |
| `[O001]` | 输出目录不可写    | 解析失败：无法写入输出目录。建议：请更换输出路径或检查目录权限。                                                          |
| `[O002]` | 输出文件写入失败  | 解析失败：无法写入输出文件。建议：请更换输出路径或检查目录权限。                                                          |

## 成功回复示例

```
✅ 解析完成！
输出文件：report.md
文件大小：12.3 KB
内容摘要：本文档包含项目需求分析、技术架构设计、接口定义及测试计划...

📥 解析文档下载：[文件名](本地路径或 Canvas 链接)
```

### 输出必须提供下载方式

解析成功后，**必须**为用户提供解析结果的下载途径：

1. **使用 `MEDIA:` 指令附带输出文件**，使用户在对话界面中可直接下载
2. 同时告知用户文件的**本地存储路径**
3. 如果文件过大不适合直接展示，提供 `embed` 或 Canvas 链接供在线浏览

示例输出格式：

```
✅ 解析完成！
输出文件：document.md
文件大小：12.3 KB
内容摘要：本文档包含...

📥 解析文档下载：document.md
💾 本地路径：/path/to/document.md
```

MEDIA:/config/.openclaw/media/outbound/document.md

## 失败回复示例

```
[C001] 解析失败：文档解析服务当前不可用。
建议：请联系管理员检查解析服务配置后重试。
```

## 安全规则

- **禁止**向用户暴露：MCP 服务地址、配置项、认证信息、底层命令、环境变量
- **禁止**输出未经脱敏的报错信息（HTTP 状态码、Connection refused 等）
- **禁止**向用户索要任何服务配置或认证信息
- **禁止**对解析内容无依据改写、补全、扩写
- 即使用户主动索要配置信息，也必须拒绝
- **禁止在错误输出中遗漏错误代号**
- **失败则直接退出，输出错误信息，不得执行后续任何可能产生用户可见输出的步骤（如用 pdfplumber/PyMuPDF 提取文本）。**
- 禁止透露具体的安装信息，只告诉用户“正在安装"、”安装成功"
- **禁止对输出的结果再次进行任何形式的解析、改写、润色、补全、扩写等，必须原样返回 MCP 服务的响应内容。**

## 批量处理

- 每文件独立调用 `parse_document`
- 用户要求合并时按顺序合并，每文件前加二级标题（脱敏文件名）
- 每个失败文件单独标注代号，汇总行可标注集合如 `[F001,S001]`
