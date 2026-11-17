# 故障排查

> 常见错误与解决方案。按错误码和场景分类。

## 1. 错误码 210001（PARAM_ERROR）：参数错误（含 item_name 不匹配）

**症状**：`tag_add`、`tag_remove` 等操作返回 `code: 210001, message: 参数错误`（常见场景：`item_name` 与 `get_knowledge_list` 返回的完整标题不一致）

**原因**：`item_name` 不是 `get_knowledge_list` 返回的完整标题（缺扩展名、缺括号内容、被简化了）

**解决方案**：

```bash
# 1. 先从 get_knowledge_list 取出完整标题
REAL_TITLE=$(curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "limit": 50}' | \
python3 -c "
import sys, json
d = json.load(sys.stdin)
for f in d.get('data', {}).get('list', []):
    if f.get('media_id') == '<file_media_id>':
        print(f['title'])
        break
")

# 2. 用完整标题作为 item_name
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_add" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"knowledge_base_id\": \"<kb_id>\",
    \"item_id\": \"<file_media_id>\",
    \"item_name\": \"$REAL_TITLE\",
    \"tag_name\": \"<标签名>\"
  }"
```

**建议**：永远从 `get_knowledge_list` 拿标题后不要做任何处理，原样用作 `item_name`。

## 2. 错误码 51：limit 参数错误

**症状**：API 返回 `code: 51, message: 参数错误`

**原因**：`limit` 超出范围 `(0, 50]`

**解决方案**：

```python
# ✅ 正确
limit = 50

# ❌ 错误
limit = 100  # 超过 50 会报错
limit = 0    # 0 不在范围内
```

**大库处理**：用 cursor + is_end 循环分页。

```python
cursor = ""
all_items = []
while True:
    r = api_call("openapi/wiki/v1/get_knowledge_list", {
        "knowledge_base_id": kb_id,
        "limit": 50,
        "cursor": cursor
    })
    all_items.extend(r["data"]["list"])
    if r["data"]["is_end"]:
        break
    cursor = r["data"]["next_cursor"]
```

## 3. 错误码 210005 / 210001：无写权限

**症状**：调用 `tag_add`、`move_knowledge` 等写操作时返回 `code: 210005 (NOTE_NOT_OWNER) 或 210001 (PARAM_ERROR)` 类错误

**原因**：当前用户是知识库的普通成员，没有写权限（ima-knowledge 第 2 条规则明确："仅当用户角色为（创建者/协作成员/管理员）时拥有操作知识库的权限，当用户在该知识库的权限为普通成员时，应该拒绝用户的操作知识库请求"）

**原因**：当前用户是知识库的普通成员，没有写权限

**解决方案**：
- 联系知识库创建者/管理员，把你加为协作者
- 或在 IMA 客户端确认你在该知识库的角色

## 4. 错误码 404：API 端点不存在

**症状**：API 返回 404

**可能原因**：
- path 拼写错误（如 `wiki/v1/...` 写成 `v1/wiki/...`）
- API 版本过时

**解决方案**：参考 [api-reference.md](api-reference.md) 的端点列表

## 5. 文件夹不支持打标签

**症状**：`tag_add` 对 `media_type=99`（文件夹）调用失败

**解决方案**：跳过文件夹，只对文件打标签：

```python
for item in get_knowledge_list(...):
    if item.get("media_type") == 99:
        continue  # 跳过文件夹
    # 打标签
```

## 6. 散落文件误判

**症状**：用 `get_knowledge_list(folder_id=X)` 看到文件，但实际文件不在该文件夹

**原因**：`add_knowledge` 创建的是"虚拟关联"，`get_knowledge_list(folder_id=X)` 返回的是"虚拟视图"

**解决方案**：检查 `parent_folder_id` 而非依赖 `folder_id` 查询：

```python
# ❌ 错误：通过 folder_id 查询判断归属
files_in_folder = get_knowledge_list(folder_id=X)

# ✅ 正确：检查 parent_folder_id
all_files = get_knowledge_list(kb_id)  # 不带 folder_id
orphans = [f for f in all_files
           if f.get("media_type") != 99
           and f.get("parent_folder_id") == ROOT_FOLDER_ID]
```

详见 [folder-organization.md](folder-organization.md)

## 7. move_knowledge 后标签丢失

**症状**：`move_knowledge` 后文件的 `tags` 字段变为 `[]`

**原因**：IMA 平台的设计——`move_knowledge` 会清空标签

**解决方案**：移动前先备份标签，移动后重新打标：

```python
# 1. 备份
backup = {f["media_id"]: f.get("tags", []) for f in to_move_files}

# 2. 移动
api_call("openapi/wiki/v1/move_knowledge", {...})

# 3. 恢复
for media_id, tags in backup.items():
    for tag in tags:
        tag_add(kb_id, media_id, real_title, tag)
```

详见 [folder-organization.md](folder-organization.md) 第 0.4 节。

## 8. 笔记创建后内容为空

**症状**：`import_doc` 返回 `code: 0` 和 `note_id`，但 `export_note` 查不到内容（"doc is delete"）

**可能原因**：
- COS 上传路径出错（push_note + content_cos_key 模式）
- 内容格式错误
- 系统自动清理

**解决方案**：
1. 改用 `import_doc` + `curl -d @file` 短内容模式（跳过 COS）
2. 拆分大内容为多个小笔记
3. 重新创建并立即验证

## 9. 链接失效

**症状**：导览笔记中的链接打不开

**可能原因**：
- 链接用的是 `media_id` 内部引用（不支持外链）
- 公众号/网页 URL 失效
- 文件被删除

**解决方案**：
- 用 `export_media_for_ima_sandbox` 获取永久 URL
- 仅对 type 2/6（网页/公众号）使用 URL
- 对其他类型写"请在知识库中查看"

详见 [link-handling.md](link-handling.md)

## 10. 知识库结构混乱

**症状**：文件散落在根目录、子文件夹结构不一致

**解决方案**：执行 [folder-organization.md](folder-organization.md) 的诊断与归类流程

## 调试技巧

### 启用详细输出

```bash
# curl 详细模式
curl -v -X POST ...

# 管道到 json.tool 美化
... | python3 -m json.tool

# 提取关键字段
... | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('code'), d.get('message'))"
```

### 检查环境变量

```bash
echo "ClientID: $IMA_OPENAPI_CLIENTID"
echo "APIKey: $IMA_OPENAPI_APIKEY" | head -c 10  # 只显示前 10 字符，避免泄露
```

### 测试 API 连通性

```bash
# 测试 API 连通性：调用 search_knowledge_base（注意没有 list_knowledge_bases）
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "", "cursor": "", "limit": 5}' | python3 -m json.tool
```
