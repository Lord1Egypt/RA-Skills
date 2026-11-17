# 腾讯 IMA 知识库 API 配置指南（v3.0 — IMA OpenAPI v1.1.7）

> ⚠️ **v3.0 重大变更**：
> - API 端点从 `/v1/note/create` 迁移到 `/openapi/note/v1/import_doc`
> - Base URL 从 `https://ima.im.qq.com/openapi` 改为 `https://ima.qq.com`
> - 环境变量从 `IMA_CLIENT_ID`/`IMA_API_KEY` 改为 `IMA_OPENAPI_CLIENTID`/`IMA_OPENAPI_APIKEY`
> - 存储模式从"笔记本"改为"知识库"两步流程

## 两套 API 系统（不可混用）

IMA 有两套完全独立的 API，对应 UI 中两个不同的标签页：

| API 系统 | 路径前缀 | 管理对象 | UI 对应 |
|---------|---------|---------|---------|
| **Notes API** | `/openapi/note/v1/` | 笔记、笔记本 | IMA「笔记本」标签页 |
| **Knowledge Base API** | `/openapi/wiki/v1/` | 知识库、知识条目 | IMA「知识库」标签页 |

**关键区别**：「FIM知识库」是**知识库**（wiki API），不是笔记本（note API）。

## 获取凭证

### 步骤 1: 访问 IMA 开放平台

打开 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface)

### 步骤 2: 登录并获取凭证

1. 使用 QQ 或微信扫码登录
2. 在「Agent 接口」页面获取凭证：
   - **Client ID**: 应用标识
   - **Api Key**: API 密钥

### 步骤 3: 复制凭证

```text
Client ID: your_client_id_here
Api Key: your_api_key_here
```

## 本地配置

### 设置环境变量（v3.0）

```bash
# Windows PowerShell — 持久化设置
[System.Environment]::SetEnvironmentVariable("IMA_OPENAPI_CLIENTID", "your_client_id", "User")
[System.Environment]::SetEnvironmentVariable("IMA_OPENAPI_APIKEY", "your_api_key", "User")

# Windows PowerShell — 临时设置（当前会话）
$env:IMA_OPENAPI_CLIENTID = "your_client_id"
$env:IMA_OPENAPI_APIKEY = "your_api_key"

# Linux/macOS
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"
```

> 旧变量名 `IMA_CLIENT_ID`/`IMA_API_KEY` 仍兼容回退，但建议迁移到新名。

### 可选：指定知识库

```bash
$env:IMA_KB_NAME = "FIM知识库"  # 默认值
```

### 验证配置

```python
from scripts.ima_client import IMAClient

client = IMAClient()
if client.test_connection():
    print("✅ IMA 连接成功")
else:
    print("❌ IMA 连接失败，请检查凭证")
```

## API 基础信息（v1.1.7）

- **Base URL**: `https://ima.qq.com`
- **认证方式**: Header `ima-openapi-clientid` + `ima-openapi-apikey`
- **数据格式**: JSON
- **无需本地客户端**: 所有操作通过云端 API 完成

### Notes API 端点

| 功能 | 端点 | 说明 |
|------|------|------|
| 创建笔记 | `POST /openapi/note/v1/import_doc` | 从 Markdown 创建笔记 |
| 追加内容 | `POST /openapi/note/v1/append_doc` | 向现有笔记追加内容 |
| 获取笔记内容 | `POST /openapi/note/v1/get_doc_content` | 读取笔记纯文本/JSON |
| 列出笔记 | `POST /openapi/note/v1/list_note` | 列出笔记本中的笔记 |
| 搜索笔记 | `POST /openapi/note/v1/search_note` | 按标题/正文搜索 |
| 列出笔记本 | `POST /openapi/note/v1/list_notebook` | 列出所有笔记本 |

### Knowledge Base API 端点

| 功能 | 端点 | 说明 |
|------|------|------|
| 搜索知识库 | `POST /openapi/wiki/v1/search_knowledge_base` | 按名称搜索，返回 `kb_id` |
| 可添加知识库列表 | `POST /openapi/wiki/v1/get_addable_knowledge_base_list` | 列出可添加内容的知识库 |
| 添加知识 | `POST /openapi/wiki/v1/add_knowledge` | 添加笔记/网页/文件到知识库 |
| 浏览知识库 | `POST /openapi/wiki/v1/get_knowledge_list` | 浏览知识库内容 |
| 导入 URL | `POST /openapi/wiki/v1/import_urls` | 服务端抓取 URL（保留图片） |

## 存储流程

### 流程 1：纯文本笔记（X/Twitter/飞书/手动内容）

```python
from scripts.ima_client import IMAClient

client = IMAClient()

# Step 1: 创建笔记（Notes API）
note = client.create_note(title="标题", content=markdown_content)
note_id = note["note_id"]

# Step 2: 添加到知识库（Knowledge Base API）
kb_id = client.find_knowledge_base_by_name("FIM知识库")
client.add_note_to_knowledge_base(
    note_id=note_id,
    title="标题",
    knowledge_base_id=kb_id,  # media_type=11, note_info.content_id=note_id
)
```

### 流程 2：URL 导入（公众号/普通网页 — 保留图片）

```python
from scripts.ima_client import IMAClient

client = IMAClient()
kb_id = client.find_knowledge_base_by_name("FIM知识库")

# IMA 服务端抓取 URL，保留图片和排版
results = client.import_urls(
    knowledge_base_id=kb_id,
    urls=["https://mp.weixin.qq.com/s/xxxxx"],
)
```

### 智能路由（推荐用 save_to_ima）

```python
from scripts.web_to_all import save_to_ima

# 自动路由：
# - 公众号/网页 URL → import_urls（保留图片）
# - X/Twitter/飞书 URL → 纯文本笔记（逐字转录）
result = save_to_ima(content, title, knowledge_base="FIM知识库", source_url=url)
```

## add_knowledge 的 media_type 枚举

| media_type | 类型 | note_info/web_info 字段 |
|-----------|------|------------------------|
| 2 | 网页 | `web_info.content_id=<url>` |
| 6 | 公众号文章 | 同上，URL 匹配 `mp.weixin.qq.com/s` |
| 11 | 笔记 | `note_info.content_id=<note_id>` |
| 7 | Markdown | 需先 create_media + COS 上传 |

## IMA 存放路由规则

| source_url 类型 | IMA 存放方式 | 原因 |
|----------------|------------|------|
| 公众号（`mp.weixin.qq.com`） | `import_urls`（服务端抓取） | 保留图片和排版 |
| 普通网页 | `import_urls`（服务端抓取） | 保留图片和排版 |
| **X/Twitter** | **纯文本笔记（逐字转录）** | 技能规则要求逐字转录 |
| 飞书 wiki | 纯文本笔记（逐字转录） | 需登录认证，IMA 无法抓取 |
| 无 URL | 纯文本笔记 | 手动内容/飞书转录 |

## 安全注意事项

⚠️ **重要提示**：
- **Api Key 等同于密码**，不要泄露给他人
- 永远不要将真实凭证提交到 Git
- 已在 `.gitignore` 中添加 `.env` 规则
- 定期轮换 Api Key

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| `401 Unauthorized` | 检查 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 是否正确 |
| `404 Not Found` | API 端点已变更，确认用 `/openapi/note/v1/import_doc`（非 `/v1/note/create`） |
| 笔记不在知识库中 | 知识库≠笔记本，必须用两步流程：create_note → add_knowledge |
| `import_urls` 文件夹不存在 | folder_id 不等于 knowledge_base_id，用 `get_root_folder_id()` 获取 |
| X 链接 IMA 存储错误 | X/Twitter 必须逐字转录（纯文本笔记），不可用 import_urls |
| `code=210001` 参数错误 | 检查请求体 JSON 格式，`content_format` 必须为 1（MARKDOWN） |
