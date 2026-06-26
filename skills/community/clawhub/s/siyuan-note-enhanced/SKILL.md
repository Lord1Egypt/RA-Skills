---
name: siyuan-note
description: 思源笔记读写技能，提供与思源笔记（SiYuan Note）进行交互的能力，包括读取和写入笔记内容
metadata:
  {
    "openclaw": {
      "emoji": "📝",
      "requires": { "bins": ["python3"] },
      "primaryEnv": "SIYUAN_API_TOKEN"
    }
  }
---

# 思源笔记技能 📝

## 描述
这个技能提供了与思源笔记（SiYuan Note）进行交互的能力，包括读取和写入笔记内容。基于思源笔记Chrome扩展最佳实践优化，支持真正的独立文档创建、文章剪藏、模板渲染等高级功能。

当用户提到"查询思源笔记"、"写入思源笔记"、"创建思源笔记"或类似请求时，使用此技能。

## 激活条件
当用户提到以下关键词时激活此技能：
- 思源笔记
- 查询思源笔记
- 写入思源笔记
- 同步到思源笔记
- 从思源笔记读取
- 搜索思源笔记
- 思源笔记查询
- 思源笔记搜索

## 前置要求
1. 思源笔记必须正在运行，并且API已启用
2. 需要有效的API token
3. Python环境需要安装requests库

## 🆕 增强功能（v2.0）

基于思源笔记Chrome扩展（[siyuan-note/siyuan-chrome](https://github.com/siyuan-note/siyuan-chrome)）的实践，增加了以下高级功能：

### 1. 真正的独立文档创建 ✨
使用`createDocWithMd` API创建真正的独立文档，不再依赖在现有文档中追加内容：

```python
from siyuan_note_enhanced import create_enhanced_client

client = create_enhanced_client()
doc_id = client.create_document(
    "其他",
    "我的文档",
    "# 标题\n\n文档内容",
    tags=["标签1", "标签2"]
)
# 返回: 独立文档ID，如 "20260217205120-3wcoxib"
# 文件: myDocument.sy
```

**优势**：
- ✅ 创建独立的.sy文档文件
- ✅ 在思源笔记文档列表中可见
- ✅ 支持完整的内容和格式

### 2. 文章剪藏功能 📰
类似Chrome扩展的剪藏功能，支持完整的文章剪藏：

```python
client.clip_article(
    notebook_name="其他",
    title="文章标题",
    url="https://example.com/article",
    content="文章的Markdown内容",
    excerpt="文章摘要",
    site_name="网站名称",
    tags=["技术", "笔记"]
)
```

**特性**：
- ✅ 自动格式化和模板渲染
- ✅ 保留原始URL和元数据
- ✅ 支持自定义剪藏模板
- ✅ 自动处理网站名称和摘要

### 3. 强大的模板系统 🎨
基于Chrome扩展的模板渲染引擎：

```python
# 基本变量替换
template = "标题: ${title}\n时间: ${date}"
data = {'title': '测试', 'date': '2026-02-17'}
result = client.render_template(template, data)
# 结果: "标题: 测试\n时间: 2026-02-17"

# 条件表达式
template = "${show ? '显示' : '隐藏'}"
result = client.render_template(template, {'show': True})
# 结果: "显示"

# 嵌套属性
template = "用户: ${user.name}"
data = {'user': {'name': '张三'}}
result = client.render_template(template, data)
# 结果: "用户: 张三"
```

**支持的功能**：
- ✅ 变量替换：`${variable}`
- ✅ 条件表达式：`${condition ? true : false}`
- ✅ 嵌套属性访问：`${user.name}`
- ✅ 字符串拼接：`${firstName + lastName}`

### 4. 增强的错误处理 🛡️
- ✅ API调用失败时自动回退到兼容方法
- ✅ 详细的错误信息和调试输出
- ✅ 智能验证和文档确认
- ✅ 连接状态监控

### 5. 改进的整体架构 🏗️
- ✅ 基于思源笔记Chrome扩展的最佳实践
- ✅ 更清晰的代码结构和分离关注点
- ✅ 更好的可维护性和可扩展性
- ✅ 完整的测试覆盖

## 配置

### 环境变量（推荐）
配置通过环境变量读取：
- `SIYUAN_API_URL` - 思源笔记API地址，例如：`http://localhost:6806`
- `SIYUAN_API_TOKEN` - 你的API token（从思源笔记设置中获取）

### 配置文件
也可以使用配置文件，默认位置：`~/.openclaw/workspace/siyuan-openchat-sync/config.json`
```json
{
  "siyuan": {
    "api_url": "http://localhost:6806",
    "token": "your-api-token-here"
  },
  "sync": {
    "notebook_name": "其他",
    "document_name": "openchat",
    "auto_sync": true
  }
}
```

## 使用方法

### 基础版（向后兼容）
```python
from siyuan_note import SiYuanNote

siyuan = SiYuanNote()
```

### 增强版（推荐）🚀
```python
from siyuan_note_enhanced import create_enhanced_client

client = create_enhanced_client()
```

### 版本对比

| 功能 | 基础版 | 增强版 |
|------|--------|--------|
| 独立文档创建 | ❌ 在现有文档中追加 | ✅ 创建真正的.sy文件 |
| 文章剪藏 | ❌ 不支持 | ✅ 完整的剪藏功能 |
| 模板渲染 | ❌ 基础格式化 | ✅ 强大的模板系统 |
| 错误处理 | ✅ 基础处理 | ✅ 增强的错误处理 |
| Chrome扩展兼容 | ❌ 不兼容 | ✅ 基于最佳实践 |
| 向后兼容 | ✅ 完全兼容 | ✅ 包含所有功能 |

### 1. 测试连接
```python
from siyuan_note import SiYuanNote

siyuan = SiYuanNote()
if siyuan.test_connection():
    print("连接成功")
else:
    print("连接失败")
```

### 2. 查询思源笔记
```python
# 获取所有笔记本
notebooks = siyuan.get_notebooks()
print(f"找到 {len(notebooks)} 个笔记本")

# 获取指定笔记本的文档
notebook_id = siyuan.get_notebook_id("其他")
documents = siyuan.get_documents(notebook_id)

# 搜索特定内容
results = siyuan.search_content("关键词")
```

### 3. 写入思源笔记
```python
# 同步对话到思源笔记
conversation_data = {
    'summary': '对话摘要',
    'messages': [
        {'role': 'user', 'content': '用户消息'},
        {'role': 'assistant', 'content': '助手回复'}
    ],
    'conclusion': '对话总结'
}

success = siyuan.sync_conversation(conversation_data)
if success:
    print("同步成功")
else:
    print("同步失败")
```

### 4. 创建新笔记
```python
# 创建新文档
new_doc_id = siyuan.create_document(
    notebook_name="其他",
    document_name="新文档",
    content="# 新文档\n\n这是新创建的文档内容。"
)
```

## 核心类：SiYuanNote

### 初始化
```python
# 从环境变量自动读取（推荐）
from siyuan_note import SiYuanNote
siyuan = SiYuanNote()

# 或手动指定
siyuan = SiYuanNote(
    api_url="http://localhost:6806",
    token="your-api-token-here"
)
```

### 主要方法

#### 连接相关
- `test_connection()` - 测试API连接
- `get_notebooks()` - 获取所有笔记本
- `get_notebook_id(notebook_name)` - 获取笔记本ID

#### 读取操作
- `get_documents(notebook_id)` - 获取笔记本中的文档
- `get_document_content(document_id)` - 获取文档内容
- `search_content(query, notebook_name=None)` - 搜索内容

#### 写入操作
- `create_document(notebook_name, document_name, content)` - 创建新文档
- `append_to_document(document_id, content)` - 向文档追加内容
- `sync_conversation(conversation_data, notebook_name="其他", document_name="openchat")` - 同步对话

#### 配置管理
- `load_config()` - 加载配置
- `save_config()` - 保存配置
- `update_config(new_config)` - 更新配置

## 对话数据格式
```python
conversation_data = {
    'summary': '对话摘要',
    'messages': [
        {
            'role': 'user',  # 或 'assistant'
            'content': '消息内容',
            'timestamp': '可选时间戳'
        }
    ],
    'conclusion': '对话总结',
    'metadata': {
        'source': 'OpenChat',
        'version': '1.0'
    }
}
```

## 示例脚本

### 快速同步当前对话
```python
#!/usr/bin/env python3
"""
快速同步当前OpenChat对话到思源笔记
"""

import sys
import json
from siyuan_note import SiYuanNote

def main():
    # 从命令行参数获取对话数据
    if len(sys.argv) < 2:
        print("用法: python sync_now.py '对话JSON数据'")
        return
    
    try:
        conversation_data = json.loads(sys.argv[1])
    except:
        print("错误: 无效的JSON数据")
        return
    
    # 同步到思源笔记
    siyuan = SiYuanNote()
    success = siyuan.sync_conversation(conversation_data)
    
    if success:
        print("✅ 对话已同步到思源笔记")
    else:
        print("❌ 同步失败")

if __name__ == "__main__":
    main()
```

### 批量同步历史对话
```python
#!/usr/bin/env python3
"""
批量同步历史对话到思源笔记
"""

import os
import json
from siyuan_note import SiYuanNote

def sync_history_conversations(history_dir="./conversations"):
    siyuan = SiYuanNote()
    
    if not os.path.exists(history_dir):
        print(f"目录不存在: {history_dir}")
        return
    
    # 遍历所有JSON文件
    for filename in os.listdir(history_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(history_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取对话数据
                conversation_data = data.get('conversation', data)
                
                print(f"同步: {filename}")
                success = siyuan.sync_conversation(conversation_data)
                
                if success:
                    print(f"✅ {filename} 同步成功")
                else:
                    print(f"❌ {filename} 同步失败")
                    
            except Exception as e:
                print(f"❌ 处理 {filename} 时出错: {e}")

if __name__ == "__main__":
    sync_history_conversations()
```

## 故障排除

### 常见问题

1. **连接失败**
   - 检查思源笔记是否正在运行
   - 确认API地址和端口正确
   - 验证token是否有效

2. **权限问题**
   - 确保token有读写权限
   - 检查笔记本是否存在

3. **同步失败**
   - 检查网络连接
   - 查看思源笔记日志
   - 验证对话数据格式

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)

siyuan = SiYuanNote()
siyuan.test_connection()
```

## 集成到OpenClaw

### 作为工具使用
将此技能集成到OpenClaw的tools中，可以通过以下方式调用：

```python
# 在OpenClaw会话中
from skills.siyuan_note.siyuan_note import SiYuanNote

# 初始化
siyuan = SiYuanNote()

# 查询思源笔记
if user_request == "查询思源笔记":
    notebooks = siyuan.get_notebooks()
    response = f"找到 {len(notebooks)} 个笔记本"
    
# 写入思源笔记
elif user_request == "写入思源笔记":
    success = siyuan.sync_conversation(current_conversation)
    response = "已同步到思源笔记" if success else "同步失败"
```

### 自动同步功能
可以设置定时任务，自动将OpenClaw对话同步到思源笔记：

```python
# 在heartbeat或cron任务中
def auto_sync_to_siyuan():
    siyuan = SiYuanNote()
    
    # 获取未同步的对话
    unsynced_conversations = get_unsynced_conversations()
    
    for conv in unsynced_conversations:
        siyuan.sync_conversation(conv)
        mark_as_synced(conv)
```

## 更新日志

### v1.0.0 (初始版本)
- 基本的思源笔记API连接
- 对话同步功能
- 配置管理
- 错误处理

## 注意事项
1. API token是敏感信息，请妥善保管，永远不要提交到版本控制系统
2. 建议定期备份思源笔记数据
3. 大量同步时注意API频率限制
4. 确保思源笔记版本兼容性

## 相关文件
- `.env.example` - 环境变量配置示例
- `README.md` - 完整文档
- `CHANGELOG.md` - 更新日志