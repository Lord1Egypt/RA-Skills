# 更新日志

## v2.0.0 (2026-02-17) - 增强版 🚀
**基于思源笔记Chrome扩展优化**

### 🆕 新增功能
- ✅ 使用`createDocWithMd` API实现真正的独立文档创建
- ✅ 新增文章剪藏功能（类似Chrome扩展）
- ✅ 实现强大的模板渲染系统
- ✅ 增强的错误处理和回退机制
- ✅ 新增`SiYuanNoteEnhanced`类

### 📈 改进
- ✅ 基于思源笔记Chrome扩展最佳实践
- ✅ 改进的API参数处理
- ✅ 更好的用户反馈和调试信息
- ✅ 优化的代码结构和可维护性

### 🔧 API变更
- 新增：`create_document()` 现在创建独立文档
- 新增：`clip_article()` 文章剪藏功能
- 新增：`render_template()` 模板渲染
- 优化：错误处理和回退机制

### ✅ 兼容性
- ✅ 完全向后兼容v1.0.0
- ✅ 基础功能保持不变
- ✅ 现有配置继续有效

### 📚 参考项目
- 思源笔记Chrome扩展: [siyuan-note/siyuan-chrome](https://github.com/siyuan-note/siyuan-chrome)
- 学习了以下实践：
  - 使用createDocWithMd API的最佳参数组合
  - 模板渲染系统的实现
  - 文章剪藏的完整流程
  - 错误处理和用户体验优化

## v1.0.0 (初始版本)
- 基本的思源笔记API连接
- 对话同步功能
- 配置管理
- 错误处理

---

# 迁移指南

## 从v1.0迁移到v2.0

**好消息：完全兼容！** 如果您使用的是基础功能，无需任何修改即可继续使用。

### 享受新功能

如果您想使用新功能，只需导入增强版：

```python
# 之前（基础版）
from siyuan_note import SiYuanNote
siyuan = SiYuanNote()

# 现在（增强版，推荐）
from siyuan_note_enhanced import create_enhanced_client
client = create_enhanced_client()
```

### 新功能示例

**创建独立文档**：
```python
# v1.0: 在现有文档中创建内容块
doc_id = siyuan.create_document("其他", "文档", "内容")

# v2.0: 创建真正的独立文档.sy文件
doc_id = client.create_document("其他", "文档", "内容")
```

**文章剪藏**：
```python
# v2.0: 新功能
client.clip_article(
    notebook_name="其他",
    title="文章标题",
    url="https://example.com",
    content="内容",
    tags=["标签"]
)
```

**使用模板**：
```python
# v2.0: 新功能
template = "${title} - ${date}"
result = client.render_template(template, {'title': '标题', 'date': '2026-02-17'})
```

### 配置保持不变
- 仍然使用相同的配置文件
- API地址和token配置相同
- 笔记本和文档保持兼容

### 测试升级
```python
# 测试增强版功能
from siyuan_note_enhanced import create_enhanced_client

client = create_enhanced_client()

# 测试连接
if client.test_connection():
    print("✅ 增强版连接成功")

# 测试独立文档创建
doc_id = client.create_document("其他", "测试文档", "这是测试内容")
if doc_id:
    print(f"✅ 独立文档创建成功: {doc_id}")
```