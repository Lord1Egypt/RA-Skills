# 飞书云文档 Block 类型映射表

> 飞书 Docx API 的 block_type 枚举值。创建文档 blocks 时必须使用正确的 block_type，否则返回 400 Bad Request。

## block_type 完整映射

| block_type | 名称 | Markdown 对应 | block 字段名 |
|-----------|------|-------------|------------|
| 1 | Page（页面根块） | — | `page` |
| 2 | Text（文本） | 普通段落 | `text` |
| 3 | Heading1（一级标题） | `# ` | `heading1` |
| 4 | Heading2（二级标题） | `## ` | `heading2` |
| 5 | Heading3（三级标题） | `### ` | `heading3` |
| 6 | Heading4（四级标题） | `#### ` | `heading4` |
| 7 | Heading5（五级标题） | `##### ` | `heading5` |
| 8 | Heading6（六级标题） | `###### ` | `heading6` |
| 9 | Heading7（七级标题） | — | `heading7` |
| 10 | Heading8（八级标题） | — | `heading8` |
| 11 | Heading9（九级标题） | — | `heading9` |
| 12 | Bullet（无序列表） | `- ` 或 `* ` | `bullet` |
| 13 | Ordered（有序列表） | `1. ` | `ordered` |
| 14 | Code（代码块） | ` ``` ` | `code` |
| 15 | Quote（引用） | `> ` | `quote` |

## 常见错误

| 错误 | 正确值 | 说明 |
|------|-------|------|
| Code 用 block_type=2 | **block_type=14** | 2 是 Text，不是 Code |
| Quote 用 block_type=11 | **block_type=15** | 11 是 Heading9，不是 Quote |

## Block 结构示例

### Text（block_type=2）

```json
{
    "block_type": 2,
    "text": {
        "elements": [{"text_run": {"content": "文本内容"}}],
        "style": {}
    }
}
```

### Heading1（block_type=3）

```json
{
    "block_type": 3,
    "heading1": {
        "elements": [{"text_run": {"content": "标题内容"}}],
        "style": {}
    }
}
```

### Bullet（block_type=12）

```json
{
    "block_type": 12,
    "bullet": {
        "elements": [{"text_run": {"content": "列表项"}}],
        "style": {}
    }
}
```

### Code（block_type=14）

```json
{
    "block_type": 14,
    "code": {
        "elements": [{"text_run": {"content": "code content"}}],
        "style": {"language": 1}
    }
}
```

### Quote（block_type=15）

```json
{
    "block_type": 15,
    "quote": {
        "elements": [{"text_run": {"content": "引用内容"}}],
        "style": {}
    }
}
```

## 关键约束

### 1. elements 中不要加多余字段

```json
// ❌ 错误 — 多了 "type" 字段
{"text_run": {"type": "text_run", "content": "文本"}}

// ✅ 正确
{"text_run": {"content": "文本"}}
```

### 2. 空行不要创建空文本块

```python
# ❌ 错误 — 空行创建空块会导致 400
if not stripped:
    blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": ""}}]}})

# ✅ 正确 — 空行直接跳过
if not stripped:
    continue
```

### 3. 图片块需要预上传 token

图片不能直接用 URL，必须先通过飞书上传 API 获取 `file_token`，再创建图片块。当前实现暂时跳过图片。

### 4. 单次请求最多 50 个 blocks

```
POST /docx/v1/documents/{document_id}/blocks/{document_id}/children
```

**payload 中 `children` 数组最多 50 个 block**。长文章必须分批插入：

```python
for i in range(0, len(blocks), 50):
    batch = blocks[i:i+50]
    requests.post(url, headers=headers, json={"children": batch})
```

### 5. payload 中不要传 index

```json
// ❌ 错误 — index=-1 可能导致问题
{"children": blocks, "index": -1}

// ✅ 正确 — 不传 index，默认追加到末尾
{"children": blocks}
```

## API 端点

| 操作 | 方法 | URL |
|------|------|-----|
| 创建文档 | POST | `/docx/v1/documents` |
| 插入 blocks | POST | `/docx/v1/documents/{document_id}/blocks/{document_id}/children` |
| 获取文档信息 | GET | `/docx/v1/documents/{document_id}` |

## 认证

```
Authorization: Bearer {tenant_access_token}
Content-Type: application/json
```

获取 token：`POST /auth/v3/tenant_access_token/internal`，payload 为 `{"app_id": "...", "app_secret": "..."}`。
