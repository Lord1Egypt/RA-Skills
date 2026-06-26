# wiz-mcp

为知笔记（WizNote）MCP STDIO Server - 用于在 Trae/OpenClaw 等 MCP 客户端中查询、读取和创建为知笔记内容。

## 功能特性

- **列出笔记**：获取笔记元数据列表
- **搜索笔记**：通过扫描元数据实现本地搜索
- **读取笔记**：支持普通 HTML/Lite/协作笔记的 Markdown 转换
- **创建笔记**：支持通过 URL 自动抓取或手动输入 Markdown 创建笔记
- **列出附件**：普通附件接口 + 协作笔记回退解析
- **下载附件**：支持普通附件和协作资源下载（二进制转 Base64）

## 安装

```bash
# 1. 克隆或下载项目
cd wiz-mcp

# 2. 创建虚拟环境（推荐）
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt --break-system-packages
```

## 配置

1. 复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，配置以下环境变量：

| 变量 | 必填 | 说明 |
|------|------|------|
| WIZ_USER_ID | 是 | 为知笔记账号（邮箱） |
| WIZ_PASSWORD | 是 | 为知笔记密码 |
| WIZ_BASE_URL | 是 | 为知服务器地址（如 `http://127.0.0.1:5688` 或 `https://your-domain:5687`） |
| WIZ_GROUP_NAME | 否 | 群组名称（可选） |
| WIZ_KB_GUID | 否 | 知识库 GUID（可选，若填 URL 则忽略） |

## 启动

```bash
python wiz_mcp_server.py
# 或使用虚拟环境
.venv/bin/python wiz_mcp_server.py
```

## Trae mcpServers 配置示例

在 Trae 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "wiz-mcp": {
      "command": "/path/to/wiz-mcp/.venv/bin/python",
      "args": ["/path/to/wiz-mcp/wiz_mcp_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      },
      "cwd": "/path/to/wiz-mcp"
    }
  }
}
```

## 冒烟测试

```bash
python mcp_smoke_test.py
# 或使用虚拟环境
.venv/bin/python mcp_smoke_test.py
```

## MCP Tools

### 1. wiz_list_notes

列出笔记元数据

```json
{
  "start_version": 0,
  "count": 50
}
```

### 2. wiz_search_notes

搜索笔记（扫描元数据本地过滤）

```json
{
  "query": "关键词",
  "start_version": 0,
  "page_size": 100,
  "max_pages": 10,
  "fields": ["title", "category"],
  "case_sensitive": false
}
```

### 3. wiz_get_note

读取笔记内容（自动下载图片/附件到本地）

```json
{
  "doc_guid": "笔记GUID",
  "format": "markdown",
  "include_info": true,
  "include_resources": true
}
```

**说明：** `include_resources` 默认为 `true`，会自动下载笔记中的图片和附件到 `output/notes/{doc_guid}/` 目录。

### 4. wiz_create_note

创建笔记（支持 URL 抓取）

```json
{
  "title": "笔记标题",
  "content": "Markdown 内容",
  "url": "https://example.com/article",
  "category": "/My Notes/",
  "tags": "tag1,tag2"
}
```

### 5. wiz_list_attachments

列出附件

```json
{
  "doc_guid": "笔记GUID",
  "note_type": "collaboration"
}
```

### 6. wiz_download_attachment

下载附件

```json
{
  "kind": "normal",
  "doc_guid": "笔记GUID",
  "att_guid": "附件GUID",
  "name": "文件名.pdf"
}
```

## 目录结构

```
wiz-mcp/
├── wiz_mcp_server.py          # 服务入口
├── mcp_smoke_test.py          # 冒烟测试
├── requirements.txt           # 依赖
├── .env                       # 环境变量（需手动创建）
├── .env.example               # 环境变量示例
├── .gitignore                # Git 忽略配置
├── README.md                  # 项目文档
├── prd.md                    # PRD 需求文档
├── output/                    # 输出目录
│   └── notes/                # 导出的笔记（含图片/附件）
├── .trae/
│   └── skills/wiznote-mcp/  # Trae Skill 指南
│       └── SKILL.md
└── scripts/                  # 核心代码
    ├── __init__.py
    ├── logging.py             # 日志模块
    ├── config.py             # 配置管理
    ├── wiz_open_api.py       # HTTP/WS API
    ├── server.py             # MCP 服务
    ├── note.py               # Note 模型
    ├── note_parser.py        # 解析器基类
    ├── note_fixer.py         # Markdown 修复
    ├── note_parser_factory.py # 解析器工厂
    ├── html_note_parser.py   # HTML 解析器
    ├── lite_note_parser.py   # Lite 解析器
    └── collaboration_note_parser.py # 协作笔记解析器
```

## 依赖说明

| 依赖 | 用途 |
|------|------|
| requests | HTTP 请求 |
| websocket-client | WebSocket 协作笔记 |
| python-dotenv | 环境变量加载 |
| html2text | HTML 转 Markdown |
| bs4 | BeautifulSoup 解析 |
| certifi | SSL 证书 |
| trafilatura | URL 网页抓取 |
| markdown | Markdown 转 HTML |
| pypdf | PDF 解析 |
| pytesseract | OCR 文字识别 |
| pillow | 图片处理 |

## License

MIT
