---
name: wiznote
description: 为知笔记（WizNote）API连接器，支持笔记的增删改查、搜索、附件管理、分类、标签、评论、分享等全部操作。当用户提到"为知笔记"、"WizNote"、"Wiz"，或需要在为知笔记中进行任何操作时使用此技能。
---

# 为知笔记 Skill（v2）

基于为知笔记私有化 API 的连接器，**默认使用协作笔记模式**，支持 Markdown 内容自动转换。

## 配置

```env
WIZ_ENDPOINT=http://192.168.1.121:30802
WIZ_TOKEN=<your_token>
WIZ_KB_GUID=c6522160-aca4-11ef-97d7-3bf3be62286f
WIZ_USER_ID=843909253@qq.com
WIZ_PASSWORD=i1ove1314W.
```

## 核心原则

- 所有笔记操作默认使用**协作笔记**（通过 WebSocket 协议）
- `create_note` / `update_note` 接受 Markdown 文本，自动转换为 blocks
- 传统 HTML 笔记通过 `create_note(content_type='html')` 显式创建

## API 快速索引

| 操作 | 方法 |
|------|------|
| 列出笔记 | `api.get_note_list()` |
| 搜索笔记 | `api.search_notes(keyword)` |
| 读取内容 | `api.get_note_content(doc_guid)` |
| 创建笔记 | `api.create_note(title, markdown)` |
| 更新笔记 | `api.update_note(doc_guid, markdown)` |
| 删除笔记 | `api.delete_note(doc_guid)` |
| 移动笔记 | `api.move_note(doc_guid, category)` |
| 复制笔记 | `api.copy_note(doc_guid)` |
| 分类管理 | `api.list_categories()` / `create_category()` / `delete_category()` |
| 标签管理 | `api.list_tags()` / `add_tags()` / `remove_tags()` |
| 评论 | `api.get_comments()` / `add_comment()` |
| 历史版本 | `api.get_note_history()` / `get_note_version()` |
| 分享 | `api.share_note()` / `list_shares()` |
| 附件 | `api.get_note_attachments()` / `upload_attachment()` |
| 模板创建 | `api.create_from_template(template_name, title)` |
| Markdown转Blocks | `api.markdown_to_blocks(md_text)` |

---

## 1. 笔记基础操作

### 列出笔记

```python
api.get_note_list(version=0, count=50)

# 按分类列出
api.get_notes_by_category("/My Notes/", count=50)
```

### 搜索笔记

```python
results = api.search_notes(keyword="周报", with_abstract=True)
for note in results:
    print(note['title'], note['docGuid'])
```

### 读取笔记

```python
# 自动识别协作笔记 / 普通笔记
content = api.get_note_content(doc_guid)
detail = api.get_note_detail(doc_guid)  # 元数据

note_type = detail['info'].get('type')  # 'document' 或 'collaboration'
```

---

## 2. 创建笔记（协作笔记 + Markdown）

`create_note(title, content, category, tags)` — 传入 Markdown，自动转为 blocks 并创建协作笔记。

```python
result = api.create_note(
    title="2026年第17周周报",
    content="""# 本周完成

- 完成XXX模块开发
- 修复BUG #123

## 下周计划

- [ ] 开始YYY模块
- [ ] 编写测试文档

## 风险

> 暂无
""",
    category="/openclaw/周报/",
    tags="周报,openclaw"
)
# result = {docGuid, editorToken, title, category}
```

**content_type 参数：**
- `markdown`（默认）：Markdown 文本 → blocks
- `blocks`：直接传入 blocks 列表
- `html`：创建传统 HTML 笔记

---

## 3. 更新笔记

```python
api.update_note(
    doc_guid="xxx",
    content="""# 更新后的标题

新内容段落

- [x] 已完成任务
- [ ] 待办任务
""",
    title="更新后的标题"  # 可选，同时更新标题
)
```

---

## 4. 删除 / 移动 / 复制

```python
# 删除（移到回收站）
api.delete_note(doc_guid)

# 移动到其他分类
api.move_note(doc_guid, "/openclaw/归档/")

# 复制笔记
api.copy_note(doc_guid)                           # 自动加" - 副本"
api.copy_note(doc_guid, title="新标题", category="/其他分类/")
```

---

## 5. 分类（文件夹）管理

```python
# 列出所有分类
categories = api.list_categories()

# 创建分类
api.create_category(parent="/My Notes/", name="项目A")

# 删除分类
api.delete_category("/My Notes/项目A/")

# 重命名分类
api.rename_category("/My Notes/旧名称/", "新名称")
```

---

## 6. 标签管理

```python
# 列出所有标签
tags = api.list_tags()

# 为笔记添加标签
api.add_tags(doc_guid, ["周报", "重要"])

# 批量添加（逗号分隔字符串）
api.add_tags(doc_guid, "周报,2026,openclaw")

# 移除标签
api.remove_tags(doc_guid, "临时标签")

# 全局重命名标签
api.rename_tag("旧标签名", "新标签名")
```

---

## 7. 评论功能

```python
# 获取评论
comments = api.get_comments(doc_guid)

# 添加评论
api.add_comment(doc_guid, "这是一条评论内容")

# 删除评论
api.delete_comment(doc_guid, comment_guid)
```

---

## 8. 历史版本

```python
# 获取版本列表
versions = api.get_note_history(doc_guid)

# 读取指定版本内容
version_data = api.get_note_version(doc_guid, version_id)
```

---

## 9. 分享与权限

```python
# 分享笔记（生成链接）
share_info = api.share_note(
    doc_guid,
    access='read',    # 'read' 或 'edit'
    expire_days=30     # 0=永久
)
# share_info 包含分享URL

# 列出所有分享
api.list_shares()

# 取消分享
api.cancel_share(share_id)
```

---

## 10. 附件管理

```python
# 列出附件
attachments = api.get_note_attachments(doc_guid)

# 上传附件
result = api.upload_attachment(doc_guid, "/path/to/file.pdf")

# 下载附件
data = api.download_attachment(doc_guid, att_guid)

# 下载协作笔记图片
data = api.get_collaboration_image(doc_guid, image_name)
```

---

## 11. 模板创建

```python
# 可用模板：weekly_report / meeting_minutes / todo / reading_notes / project_plan / blank
result = api.create_from_template(
    template_name='weekly_report',
    title="2026年第17周周报",
    category="/openclaw/周报/",
    tags="周报",
    attendees="张三,李四",   # 会议模板变量
    recorder="王五",          # 会议模板变量
)
```

### 模板内容预览

**weekly_report（周报）**
```markdown
# {title}
## 本周完成
- 
## 进行中
- 
## 下周计划
- 
## 风险与问题
> 
## 备注
```

**meeting_minutes（会议纪要）**
```markdown
# {title}
**日期**: {date}
**参会人**: {attendees}
**记录人**: {recorder}
## 会议议题
1. 
## 讨论内容
### 议题一
### 议题二
## 决议
- [ ] 
## 后续行动（表格）
```

**todo（待办清单）**
按紧急/重要四象限组织

**project_plan（项目计划）**
含时间线表格、风险评估表格

**reading_notes（读书笔记）**
含核心观点、章节摘要、精彩摘录

---

## 12. Markdown → Blocks 转换

`markdown_to_blocks(md_text)` — 将 Markdown 转换为协作笔记 blocks 列表，支持：

| 语法 | 转换结果 |
|------|---------|
| `# 标题` | `text_block(heading=1)` |
| `**粗体**` | `attributes: style-bold` |
| `*斜体*` | `attributes: style-italic` |
| `` `代码` `` | `attributes: style-code` |
| `[链接](url)` | `attributes: link` |
| `- 列表` | `list_block()` |
| `1. 有序` | `list_block(ordered=True)` |
| `- [x] 完成` | `list_block(checkbox='checked')` |
| `> 引用` | `text_block(quoted=True)` |
| ` ```code``` ` | `code_block()` |
| `\| 表 \|` | `table_block()` |
| `---` | `embed(embedType='hr')` |
| `![alt](src)` | `embed(embedType='image')` |

### 块快捷构造方法

```python
# 基础块
api.text_block('文本', heading=2)               # 标题/段落/引用
api.list_block('文本', ordered=True, level=2)    # 列表
api.table_block(['列1','列2'], [['a','b']])       # 表格（返回block+extra_data）
api.code_block('print("hello")', 'python')        # 代码块（返回block+extra_data）
api.divider_block()                               # 分隔线
api.image_block('https://...', '图片说明')         # 图片（URL或协作笔记内部文件名）

# v2.1 新增
api.link_block('百度', 'https://www.baidu.com')   # 链接文本
api.webpage_block('http://baidu.com')              # 嵌入网页
api.audio_block(src, file_name, file_size, file_type)  # 音频
api.file_block(src, file_name, file_size, file_type)   # 文件嵌入（office类型）
api.drawio_block(src)                              # 流程图/UML（SVG文件名）
api.encrypt_text_block(password, text, prompt)     # 加密文本块
api.formula_block(tex)                             # 数学公式

# 行内样式构造（加粗/链接等混合文本）
api.make_inline_block([
    ('标签：', True),    # True=加粗
    ('内容', False),     # False=普通
])
```

### 功能兼容性矩阵

| 功能 | 写入支持 | 读取支持 | 备注 |
|------|:--------:|:--------:|------|
| 标题 (heading 1-3) | ✅ | ✅ | |
| 段落文本 | ✅ | ✅ | |
| **加粗** | ✅ | ✅ | `style-bold` 属性 |
| *斜体* | ✅ | ✅ | `style-italic` 属性 |
| ~~删除线~~ | ✅ | ✅ | `style-strikethrough` 属性 |
| `行内代码` | ✅ | ✅ | `style-code` 属性 |
| [链接](url) | ✅ | ✅ | `link` 属性 |
| 引用块 | ✅ | ✅ | `quoted=True` |
| 有序/无序列表 | ✅ | ✅ | |
| 复选框列表 | ✅ | ✅ | `checked=True/False` |
| 代码块 | ✅ | ✅ | 需 extra_data |
| 表格 | ✅ | ⚠️ | 写入完整，读取时单元格内容为空（已知限制） |
| 分割线 | ✅ | ✅ | |
| 图片 | ✅ | ✅ | URL或内部文件名 |
| 音频 | ✅ | ✅ | 需先上传附件获取src |
| 文件嵌入 | ✅ | ✅ | 需先上传附件获取src |
| 流程图/UML | ✅ | ✅ | 需先上传SVG获取src |
| 加密文本 | ✅ | ✅ | AES加密 |
| 数学公式 | ✅ | ✅ | LaTeX语法 |
| 网页嵌入 | ✅ | ✅ | |

---

## 13. 协作笔记底层操作（高级）

```python
# 创建协作笔记（直接用 blocks）
result = api.create_collaboration_note(
    title="标题",
    blocks=[
        api.text_block('一级标题', heading=1),
        api.text_block('正文'),
    ],
    category="/My Notes/",
    tags="标签"
)

# 更新协作笔记（内部 del + create）
api.update_collaboration_note(doc_guid, blocks, title="新标题")

# 获取 editorToken
token = api.get_collaboration_token(doc_guid)

# 获取原始 JSON 内容
raw = api.get_collaboration_content(token, doc_guid)
md = api.parse_collaboration_content(raw)
```

---

## 14. Wrapper 命令行

```bash
# 列出笔记
python wiznote_wrapper.py list [count]

# 搜索
python wiznote_wrapper.py search <keyword>

# 读取
python wiznote_wrapper.py get <doc_guid>

# 创建（Markdown）
python wiznote_wrapper.py create "标题" "Markdown内容" --category /My Notes/ --tags tag1,tag2

# 更新
python wiznote_wrapper.py update <doc_guid> "新Markdown内容" --title "新标题"

# 删除 / 移动 / 复制
python wiznote_wrapper.py delete <doc_guid>
python wiznote_wrapper.py move <doc_guid> /新分类/
python wiznote_wrapper.py copy <doc_guid> [新标题] [分类]

# 分类管理
python wiznote_wrapper.py categories
python wiznote_wrapper.py create_category /父分类/ 新名称
python wiznote_wrapper.py delete_category /分类路径/

# 标签管理
python wiznote_wrapper.py tags
python wiznote_wrapper.py add_tags <doc_guid> tag1,tag2
python wiznote_wrapper.py remove_tags <doc_guid> tag1

# 评论
python wiznote_wrapper.py comments <doc_guid>
python wiznote_wrapper.py add_comment <doc_guid> <text>

# 历史版本
python wiznote_wrapper.py history <doc_guid>

# 分享
python wiznote_wrapper.py share <doc_guid> [read|edit] [expire_days]
python wiznote_wrapper.py shares

# 附件
python wiznote_wrapper.py attachments <doc_guid>
python wiznote_wrapper.py upload <doc_guid> <file_path>

# 模板
python wiznote_wrapper.py templates
python wiznote_wrapper.py template weekly_report "标题" [分类]

# Markdown转Blocks预览
python wiznote_wrapper.py md2blocks "# 标题\n- 列表项"
```

---

## 15. 常见问题

### Q: Token 过期怎么办？
A: Token 有效期约 15 分钟，API 会在初始化时自动登录获取。

### Q: 如何创建普通 HTML 笔记？
A: `api.create_note(title, html, content_type='html')`

### Q: 协作笔记更新失败？
A: `update_collaboration_note` 使用 del + create 方式覆盖，op 修改（err:1002）为已知限制。

### Q: 分类不存在？
A: 必须先通过 Web 界面创建分类，或使用 `create_category()` 创建。

### Q: Markdown 表格导出？
A: 支持，Markdown 表格自动转为 `table_block`。

## 技术架构

- **认证**：用户名密码 → token
- **普通笔记**：REST API（create/save/download）
- **协作笔记**：REST API 创建 + **WebSocket**（sharejs JSONv0 协议）读写
- **内容格式**：Markdown → blocks（协作笔记） / HTML（普通笔记）
- **附件**：Base64 / 二进制流

## 项目来源

GitHub: https://github.com/damoncui668/wiz-mcp

## 更新记录

- **2026-04-28 v2**：全面升级
  - 笔记操作默认改为协作笔记模式
  - 新增：`delete_note` / `move_note` / `copy_note`
  - 新增：分类管理（创建/删除/重命名）
  - 新增：标签管理（添加/移除/重命名标签）
  - 新增：评论功能（查看/添加/删除）
  - 新增：历史版本（查看版本列表/读取版本）
  - 新增：分享功能（创建分享/列分享/取消分享）
  - 新增：附件上传
  - 新增：`markdown_to_blocks` 转换器（支持表格、代码块、复选框等）
  - 新增：5个笔记模板（周报/会议纪要/待办/读书笔记/项目计划）
  - 新增：`create_from_template` 一键从模板创建
  - 新增：Block 快捷构造方法（code_block / divider_block / image_block）
  - 调研报告：https://github.com/altairwei/WizNotePlus、https://github.com/WizTeam/WizQTClient、https://github.com/famotime/Wiznotes_tools

- **2026-05-14 v2.1**：功能扩展
  - 新增：链接块 `link_block(text, url)`
  - 新增：网页嵌入块 `webpage_block(url)`
  - 新增：音频块 `audio_block(src, file_name, file_size, file_type)`
  - 新增：文件嵌入块 `file_block(src, file_name, file_size, file_type)`
  - 新增：流程图/UML 块 `drawio_block(src)`
  - 新增：加密文本块 `encrypt_text_block(password, text, prompt)`
  - 新增：公式块 `formula_block(tex)`
  - 新增：加粗/斜体/删除线行内样式 `make_inline_block(parts)`
  - 改进：`table_block` 动态列宽算法优化（中文按2倍宽度计算）
  - 改进：`update_collaboration_note` 支持删除线 `style-strikethrough`
  - 功能兼容性测试完成：标题/引用/链接/代码/公式/分割线/图片/音频/文件/流程图/表格/加密文本/网页嵌入
