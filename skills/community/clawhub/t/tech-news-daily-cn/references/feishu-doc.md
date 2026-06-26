# 飞书文档操作参考

## 获取知识库节点

```json
// 1. 获取知识库列表
{ "action": "spaces" }

// 2. 获取知识库子节点（需传入 space_id）
{ "action": "nodes", "space_id": "xxx", "parent_node_token": "xxx" }
```

## 创建文档

```json
{
  "action": "create",
  "title": "科技新闻日报 | 2026年4月4日",
  "folder_token": "GUQFwzZL2id2kyk1oZ5clyc0nab",
  "owner_open_id": "ou_d8ace8a146610ca26bc07d8e68a5620f"
}
```

## 写入文档内容

```json
{
  "action": "write",
  "doc_token": "V6zdd8fL2oCufnxFbivc3OhfnIg",
  "content": "# 标题\n\n正文内容..."
}
```

**注意：** 飞书文档不支持 Markdown 表格，使用列表和粗体替代。

## 文档内容示例

```markdown
# 科技新闻日报 | 2026年4月4日

## 🌐 国际科技热榜

### 1. 新闻标题
- 相关度：⭐⭐⭐⭐⭐ | 推荐度：95/100
- 摘要：这是新闻摘要
- 来源：The Guardian
- 链接：https://example.com

## 🇨🇳 国内 AI 热榜

...
```

---

## 常用节点 Token

- **个人知识库**：space_id = `7621391289904516315`
- **首页**：node_token = `GUQFwzZL2id2kyk1oZ5clyc0nab`
