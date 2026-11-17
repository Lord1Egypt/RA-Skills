# API 速查

> IMA OpenAPI 完整参考（基于 ima-knowledge 和 ima-note 最新文档对齐）。
> 所有调用都依赖 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 环境变量。

## 1. 环境变量配置

```bash
# 必需的环境变量
export IMA_OPENAPI_CLIENTID="你的ClientID"
export IMA_OPENAPI_APIKEY="你的APIKey"

# 获取地址：https://ima.qq.com/agent-interface
```

## 2. 通用调用函数（Python）

```python
import urllib.request
import json

def ima_api(path, data=None):
    """IMA OpenAPI 通用调用函数"""
    headers = {
        "ima-openapi-clientid": "你的ClientID",
        "ima-openapi-apikey": "你的APIKey",
        "Content-Type": "application/json"
    }
    url = f"https://ima.qq.com/{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data or {}).encode('utf-8'),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))
```

## 3. 知识库 API（wiki/v1/*）

### 3.1 读取类

| 功能 | 端点 | 关键参数 | 说明 |
|------|------|---------|------|
| 搜索知识库（含角色信息） | `openapi/wiki/v1/search_knowledge_base` | `query`, `cursor`, `limit` (1-20) | **推荐** 替代不存在的 `list_knowledge_bases` |
| 列出知识库内容 | `openapi/wiki/v1/get_knowledge_list` | `knowledge_base_id`, `cursor`, `limit` (1-50) | 不带 folder_id 列出根目录 |
| 按名称定位文件/文件夹 | `openapi/wiki/v1/search_knowledge` | `query`, `knowledge_base_id` | 获取位置和类型信息 |
| 发现广场公开知识库 | `openapi/wiki/v1/search_knowledge_base_in_square` | `question`, `cursor`, `limit` (1-20) | 与 search_knowledge_base 不同 |
| 导出媒体内容（COS URL）| `openapi/wiki/v1/export_media_for_ima_sandbox` | `media_id` | **返回 COS 链接需二次下载** |

### 3.2 写入类

| 功能 | 端点 | 关键参数 | 说明 |
|------|------|---------|------|
| 创建知识库 | `openapi/wiki/v1/create_knowledge_base` | `name`, `type` (1001个人/1002共享/1004订阅) | - |
| 更新知识库信息 | `openapi/wiki/v1/update_knowledge_base_basic_info` | `id`, `update_fields` | 可选更新字段：1-名称, 2-封面, 3-简介, 4-推荐问题 |
| 创建文件夹 | `openapi/wiki/v1/create_folder` | `knowledge_base_id`, `name`, `parent_folder_id` | - |
| 重命名文件/文件夹 | `openapi/wiki/v1/rename_knowledge` | `media_id`, `new_name` | - |
| 置顶/取消置顶 | `openapi/wiki/v1/set_knowledge_top` | `media_id`, `is_top` | - |
| 移动文件 | `openapi/wiki/v1/move_knowledge` | `src_kb_id`, `dst_kb_id`, `dst_folder_id`, `infos` | **每次最多 10 个文件** |
| 导入网页链接 | `openapi/wiki/v1/import_urls` | `knowledge_base_id`, `urls[]` | 批量导入 URL |
| 上传文件 | `openapi/wiki/v1/upload_file` | `knowledge_base_id`, `file` | 走 COS 上传流程 |
| 把已有笔记加入知识库 | `openapi/wiki/v1/add_knowledge` | `knowledge_base_id`, `media_id` | 虚拟关联（不改 parent_folder_id） |

### 3.3 权限管理

| 功能 | 端点 | 关键参数 |
|------|------|---------|
| 改知识库权限 | `openapi/wiki/v1/update_knowledge_base_permission` | `knowledge_base_id`, `permission` |
| 加入知识库 | `openapi/wiki/v1/join_knowledge` | `knowledge_base_id` |
| 改文件访问状态 | `openapi/wiki/v1/update_knowledge_access_status` | `media_id`, `access_status` |

### 3.4 标签管理

| 功能 | 端点 | 关键参数 |
|------|------|---------|
| 给文件打标签 | `openapi/wiki/v1/tag_add` | `kb_id`, `item_id`, `item_name`, `tag_name` |
| 从文件移除标签 | `openapi/wiki/v1/tag_remove` | `kb_id`, `item_id`, `item_name`, `tag_name` |
| 列出标签 | `openapi/wiki/v1/tag_list` | `kb_id`, `cursor`, `limit` (1-100) |
| 删除标签 | `openapi/wiki/v1/tag_delete` | `kb_id`, `tag_name` |
| 重命名标签 | `openapi/wiki/v1/tag_rename` | `kb_id`, `old_tag_name`, `new_tag_name` |

## 4. 笔记 API（note/v1/*）

### 4.1 读取类

| 功能 | 端点 | 关键参数 | 说明 |
|------|------|---------|------|
| 搜索笔记 | `openapi/note/v1/search_note` | `search_type` (0=标题/1=正文), `query_info`, `start`, `end` | start-end 差值 ≤ 20 |
| 列出笔记 | `openapi/note/v1/list_note` | `folder_id`, `sort_type`, `cursor`, `limit` (≤20) | **注意是单数 list_note，不是 list_notes** |
| 列出笔记本 | `openapi/note/v1/list_notebook` | `cursor`, `limit` | **单数 list_notebook** |
| 导出笔记 | `openapi/note/v1/export_note` | `note_id`, `target_content_format` (0/1/2) | **返回 COS URL 需二次下载** |
| 导出笔记 block 结构 | `openapi/note/v1/export_note_blocks` | `note_id` | update_note 的前置步骤 |

### 4.2 写入类

| 功能 | 端点 | 关键参数 | 说明 |
|------|------|---------|------|
| 创建笔记 | `openapi/note/v1/import_doc` | `content_format` (固定 1), `content`, `title`, `folder_id` | 第一行文本会被自动提取为标题 |
| 追加内容到笔记 | `openapi/note/v1/append_doc` | `note_id`, `content_format`, `content` | 适合短内容直接追加 |
| 按 block 编辑笔记 | `openapi/note/v1/update_note` | `note_id`, `block_id`, `content` | 需先 export_note_blocks 定位 |
| 创建笔记本 | `openapi/note/v1/add_notebook` | `name` | **注意是 add_notebook，不是 create_notebook** |
| 重命名笔记本 | `openapi/note/v1/rename_notebook` | `folder_id`, `new_name` | - |
| 重命名笔记 | `openapi/note/v1/rename_note` | `note_id`, `new_title` | - |
| 移动笔记 | `openapi/note/v1/move_notes` | `note_ids[]`, `dst_folder_id` | **复数 move_notes** |
| push 笔记 | `openapi/note/v1/push_note` | `note_id`, `content_cos_key` | 长内容走 COS 上传路径 |
| ~~删除笔记~~ | ~~`openapi/note/v1/delete_note`~~ | ❌ **API 已不支持（2026-09）** | 需用户在 IMA 客户端手动删除 |

## 5. 错误代码参考（基于 ima-note api.md）

| code | 名称 | 说明 | 解决方案 |
|------|------|------|---------|
| 0 | OK | 成功 | - |
| 210001 | PARAM_ERROR | 参数错误 | 检查参数值 |
| 210002 | REQ_WITH_INVALID_UID | 携带无效的 UID | 检查 UID 有效性 |
| 210003 | SERVICE_ERROR | 服务器内部错误 | 告知用户稍后再试，**无需重试** |
| 210004 | SPACE_NOT_ENOUGH | 用户空间不够 | 清理空间或升级 |
| 210005 | NOTE_NOT_OWNER | 不是笔记的作者 | 仅作者可操作 |
| 210006 | NOTE_IS_DELETE | 笔记已被删除 | 检查 note_id |
| 210007 | COS_CRED_ERROR | COS 上传凭证出错 | 重试或联系 IMA |
| 210008 | VERSION_CONFLICT | 版本冲突 | 重新拉取最新版本 |
| 210009 | CONTENT_SIZE_OVERLOAD | 单篇笔记超限 | **拆分写入** |
| 210010 | EXIST_GUIDE | 新手引导笔记重复 | 跳过或改名 |
| 210011 | SHARE_DOC_NOPERM | 共享知识库无权访问 | 联系知识库管理员 |
| 210012 | USER_IS_DELETE | 用户已注销 | - |
| 210030 | NOTEBOOK_NAME_EXIST | 笔记本名称重复 | 改名 |
| 210031 | NOTEBOOK_NUM_LIMIT | 笔记本数量达上限 | 清理 |
| 210032 | BATCH_EXEC_FAIL | 批量部分失败 | 检查 `data.failed_list` |
| 210033 | BATCH_EXEC_ALL_FAIL | 批量全部失败 | 重试 |
| 210034 | PRIVATE_NOTE_NOT_OWNER | 私有笔记非作者 | 无权访问 |
| 210035 | FOLDER_NOT_EXIST | 笔记本不存在 | 检查 folder_id |
| 20002 | - | apiKey 超过最大限频 | 降低调用频率 |
| 20004 | - | apiKey 鉴权失败 | 检查 IMA_OPENAPI_CLIENTID/IMA_OPENAPI_APIKEY |

## 6. 关键 API 详解

### 6.1 `get_knowledge_list`

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "cursor": "", "limit": 50}'
```

| 参数 | 必填 | 说明 |
|------|:----:|------|
| `knowledge_base_id` | ✅ | 知识库 ID |
| `cursor` | ✅ | 首次为空字符串，翻页用 `next_cursor` |
| `limit` | ✅ | 1-50 |
| `folder_id` | ❌ | 文件夹 ID（不传=根目录）|
| `tags` | ❌ | 按标签筛选（数组）|

**返回结构**（注意是 `knowledge_list` 不是 `list`）：
```json
{
  "knowledge_list": [
    {"media_id": "...", "title": "...", "parent_folder_id": "...", "tags": [...], "media_type": 99},
    ...
  ],
  "is_end": false,
  "next_cursor": "...",
  "current_path": [{"folder_id": "...", "name": "..."}]
}
```

### 6.2 `move_knowledge`

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/move_knowledge" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "src_knowledge_base_id": "<kb_id>",
    "dst_knowledge_base_id": "<kb_id>",
    "dst_folder_id": "<target_folder_id>",
    "dst_folder_name": "<target_folder_name>",
    "infos": [{"media_id": "<file_media_id>"}]
  }'
```

**注意**：
- `infos` 最多 10 个文件
- 返回的 `data.move_results[media_id].ret_code` 表示单文件结果

### 6.3 `tag_add` / `tag_remove`

**`item_name` 必须严格匹配 `get_knowledge_list` 返回的完整标题**（含扩展名和括号内容）。简化标题会导致 **220001** 错误（注意：220001 来自旧文档，实际 IMA 平台可能改用 210001）。

### 6.4 `export_note` 返回 COS URL

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<note_id>","target_content_format":1}' | python3 -c "
import sys, json, urllib.request
d = json.load(sys.stdin)
if d['code'] == 0:
    url = d['data']['content_url']
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
else:
    print(d)
"
```

**关键**：`data.content_url` 是 COS 链接，**约 3 小时时效**，需要二次 `curl` 请求获取内容。

### 6.5 `import_doc` 创建笔记

```bash
# 第一行文本会被自动提取为笔记标题
python3 -c "
import json
with open('guide_content.md', 'r') as f:
    content = f.read()
with open('note_request.json', 'w') as f:
    json.dump({
        'content_format': 1,
        'content': content,
        'title': '📖 主题导览：[主题名称]',
        'folder_id': '<目标笔记本 ID>'
    }, f, ensure_ascii=False, indent=2)
"

curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d @note_request.json | python3 -m json.tool
```

**注意**：`title` 参数会被忽略，**第一行 `content` 文本**会成为标题。

### 6.6 `append_doc` 追加内容

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/append_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id": "<note_id>", "content_format": 1, "content": "<追加内容>"}'
```

### 6.7 `export_note_blocks` + `update_note` 精细编辑

```bash
# 第一步：获取 block 结构
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note_blocks" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id": "<note_id>"}'

# 第二步：按 block_id 修改
curl -s -X POST "https://ima.qq.com/openapi/note/v1/update_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id": "<note_id>", "block_id": "<block_id>", "content": "<新内容>"}'
```

### 6.8 `search_note` 按标题/正文搜索

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/search_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"search_type": 0, "query_info": {"title": "主题导览"}, "start": 0, "end": 20}'
```

**返回**：
```json
{
  "search_note_infos": [
    {
      "note_book_info": {
        "note_id": "...",
        "title": "...",
        "summary": "...",
        "note_ext_info": {"folder_id": "...", "folder_name": "..."}
      },
      "highlightInfo": {"doc_title": "包含<em>高亮</em>的标题"}
    }
  ],
  "is_end": true,
  "total_hit_num": 3
}
```

### 6.9 `list_note` 列出笔记

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/list_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"folder_id": "", "sort_type": 0, "cursor": "", "limit": 20}'
```

**注意**：cursor 翻页用偏移量（已获取条目数）。

### 6.10 `export_media_for_ima_sandbox` 获取永久 URL

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/export_media_for_ima_sandbox" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"media_id": "<文件media_id>"}'
```

**返回结构**：
```json
{
  "media_type": 2,
  "media_content_url_info": {
    "url": "https://...",
    "headers": {"key": "value"}  // 如果非空需要传入 header
  }
}
```

**`media_type` 速查表**（从 ima-knowledge knowledge_base_read.md 完整版）：

| 值 | 类型 | 链接策略 |
|----|------|---------|
| 1 | PDF 文件 | ⚠️ 标注"请在知识库查看" |
| 2 | 网页 | ✅ 获取真实 URL |
| 3 | Word 文件 | ⚠️ 标注"请在知识库查看" |
| 4 | PPT 文件 | ⚠️ 标注"请在知识库查看" |
| 5 | Excel 文件 | ⚠️ 标注"请在知识库查看" |
| 6 | 公众号文章 | ✅ 获取真实 URL |
| 7 | Markdown | ⚠️ 不内嵌链接，写为纯文本 |
| 9 | 图片 | ⚠️ 标注"请在知识库查看" |
| 11 | 笔记 | ⚠️ 不内嵌链接，写为纯文本 |
| 12 | QA 对话 | ⚠️ 标注"请在知识库查看" |
| 13 | TXT 文本 | ⚠️ 不内嵌链接，写为纯文本 |
| 14 | Xmind | ⚠️ 标注"请在知识库查看" |
| 15 | 录音 | ⚠️ 标注"请在知识库查看" |
| 16 | 网页视频 | ⚠️ 标注"请在知识库查看" |
| 17 | 对话 | ⚠️ 标注"请在知识库查看" |
| 18 | 视频 | ⚠️ 标注"请在知识库查看" |
| 19 | 播客 | ⚠️ 标注"请在知识库查看" |
| 20 | HTML | ⚠️ 标注"请在知识库查看" |
| 21 | EPUB 文件 | ⚠️ 标注"请在知识库查看" |
| 99 | 文件夹 | ❌ 不可链接 |

## 7. IMA 平台已知限制（2026-09）

| 操作 | 状态 |
|------|:----:|
| ❌ 删除笔记 | API 不支持，需客户端手动 |
| ❌ 删除知识库 | API 不支持 |
| ❌ 删除文件夹 | API 不支持 |
| ❌ 删除文件 | API 不支持 |
| ✅ 删除标签 | API 支持 |
| ✅ 修改笔记 frontmatter | API 不支持（创建时设定）|
| ✅ 向量搜索 | 由 IMA search/fetch 处理，不归本 skill |

---

## 8. v5.0.0 → v5.0.1 变更总结

### 修正的错误

| v5.0.0 错误 | v5.0.1 正确 |
|------------|------------|
| `get_media_info` | ❌ 删除（不存在）|
| `list_knowledge_bases` | `search_knowledge_base` |
| `list_notebooks` | `list_notebook` |
| `list_notes` | `list_note` |
| `create_notebook` | `add_notebook` |
| `220001` 等旧错误码 | `210001`-`210035` + `20002`/`20004` |

### 补充的缺失端点（11 个）

- `search_knowledge`
- `search_knowledge_base_in_square`
- `create_knowledge_base`
- `update_knowledge_base_basic_info`
- `rename_knowledge`
- `set_knowledge_top`
- `import_urls`
- `add_knowledge`
- `update_knowledge_base_permission`
- `join_knowledge`
- `update_knowledge_access_status`
- `move_notes`（note/v1，复数）
- `push_note`
- `rename_note`
- `rename_notebook`
