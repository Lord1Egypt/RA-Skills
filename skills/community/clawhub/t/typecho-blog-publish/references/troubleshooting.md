# Typecho 编辑器模式问题排查指南

## 问题现象

发布文章后，在后台预览或编辑时看到的是 HTML 源码而不是渲染后的效果。

## 可能原因

### 原因 1：编辑器模式设置

Typecho 后台编辑器有两种模式：
1. **可视化编辑器**（所见即所得）
2. **HTML/代码编辑器**

**检查方法**：
- 进入文章编辑页面
- 查看编辑器右上角是否有 "HTML"/"可视化" 切换按钮
- 如果当前是 HTML 模式，会显示源码

**解决方案**：
- 点击切换按钮切换到可视化模式
- 或者在设置中默认使用可视化编辑器

### 原因 2：文章内容字段错误

Typecho 的 XML-RPC 可能使用不同的字段存储内容。

**尝试方案**：

修改 `publish_post.py`，尝试不同的字段组合：

```python
# 方案 A：使用 description 字段
post_data = {
    'title': title,
    'description': html_content,
}

# 方案 B：使用 text 字段
post_data = {
    'title': title,
    'text': html_content,
}

# 方案 C：同时设置
post_data = {
    'title': title,
    'description': html_content,
    'text': html_content,
}
```

### 原因 3：Markdown 插件冲突

如果 Typecho 安装了 Markdown 插件，可能会重复解析。

**检查方法**：
- 后台 → 控制台 → 插件
- 查看是否启用了 Markdown 相关插件

**解决方案**：
- 如果启用，尝试禁用
- 或者在发布时使用纯 HTML（不经过 Markdown 转换）

## 测试步骤

### 测试 1：手动发布测试

1. 在 Typecho 后台手动新建文章
2. 切换到 HTML 模式
3. 输入简单 HTML：`<h1>测试</h1><p>这是<strong>测试</strong></p>`
4. 保存并预览
5. 如果显示正常，说明 HTML 本身没问题

### 测试 2：XML-RPC 字段测试

运行测试脚本，尝试不同字段组合：

```bash
python3 test_xmlrpc_fields.py
```

### 测试 3：检查文章内容

在数据库中查看实际存储的内容：

```sql
SELECT text FROM typecho_contents WHERE cid = 918;
```

## 快速解决方案

### 方案 A：使用 Typecho 原生 Markdown

如果 Typecho 支持 Markdown：

1. 后台 → 设置 → 编辑器
2. 启用 Markdown 编辑器
3. 修改脚本，直接发布原始 Markdown（不转换）

### 方案 B：强制 HTML 模式

修改脚本，添加明确的 HTML 标记：

```python
post_data = {
    'title': title,
    'description': f'<!--markdown-->{html_content}',
}
```

### 方案 C：使用 Typecho 的 text 字段

Typecho 的 `metaWeblog.newPost` 可能更认 `text` 字段：

```python
post_data = {
    'title': title,
    'text': html_content,  # 主要字段
    'description': html_content,  # 备用
}
```

## 调试工具

查看实际发送的数据：

```python
# 在 publish_post.py 中添加
import pprint
print("发送的数据：")
pprint.pprint(post_data)
```

## 下一步

请尝试以下操作：

1. **检查编辑器模式**：在后台切换到可视化模式查看
2. **测试新文章**：用修复后的脚本发布新文章（ID: 919）
3. **查看数据库**：检查存储的内容是否正确
4. **反馈结果**：告诉我具体表现

---

*创建时间：2026-03-26 08:45*
