---
name: yuque-connector
description: 语雀知识库双向同步技能。支持本地文件导入语雀（Word/Excel/Markdown/HTML/文本/zip文件夹），也支持从语雀下载文档到本地。覆盖搜索、创建、更新、目录管理等操作，含错误自动恢复和进阶用法。触发词：导入语雀、上传语雀、下载语雀、语雀知识库、语雀文档、发送到语雀、从语雀下载、yuque、传到语雀、同步语雀。
agent_created: true
---

# 语雀知识库双向同步

## 概述

语雀知识库与本地文件的双向同步工具。支持将本地文件导入语雀，也支持从语雀下载文档内容到本地保存。通过语雀 MCP 的 19 个工具实现完整的读写能力。

## 支持的文件格式

### 导入（本地 → 语雀）

| 格式 | 导入方式 | 说明 |
|------|---------|------|
| `.md` | 直接导入 | 原文作为 body，`format: markdown` |
| `.docx` | 读取转换后导入 | 使用 docx 技能读取内容，转 Markdown 导入 |
| `.xlsx` | 读取转换后导入 | 使用 xlsx 技能读取数据，转 Markdown 表格导入，每个工作表单独创建文档 |
| `.html` | 直接导入 | 原文作为 body，`format: html` |
| `.txt` | 转换后导入 | 包裹为 Markdown 格式导入 |
| `.csv` | 转换后导入 | 转为 Markdown 表格导入 |
| `.json` | 转换后导入 | 转为格式化代码块导入 |
| zip/文件夹 | 批量导入 | 解压后逐个处理内部文件，批量创建文档 |

### 下载（语雀 → 本地）

| 下载内容 | 输出格式 | 说明 |
|---------|---------|------|
| 单篇文档 | `.md` | 使用 `yuque_get_doc` + `format: markdown`，保存为 Markdown 文件 |
| 整个知识库 | 多个 `.md` | `yuque_list_docs` + 逐篇 `yuque_get_doc`，每个文档一个文件 |
| 指定目录 | 多个 `.md` | `yuque_get_toc` 筛选目录下文档，逐篇下载 |
| 小记 | `.md` | `yuque_list_notes` + `yuque_get_note`，保存为 Markdown |

---

## 操作示例（附实际结果）

### 示例 1：上传 Markdown 文件到语雀

**输入**：用户说「把这个文件传到考试系统知识库」

**执行步骤**：
```
1. Read(file_path="C:/Users/Admin/报告/6月周报.md")  → 获取文件内容
2. DeferExecuteTool("mcp__yuque__yuque_get_doc", {repo_id: "78381340", ...})
   或直接 DeferExecuteTool("mcp__yuque__yuque_create_doc",
     {repo_id: "78381340", title: "6月周报", body: "<文件内容>", format: "markdown"})
```

**实际返回结果**：
```
文档创建成功
标题: 6月周报
文档ID: 272726945
slug: 6-zhou-bao
链接: https://www.yuque.com/jiuwu-tue7v/lerk9f/6-zhou-bao
```

**用户拿到手的是**：一个可以直接点击打开的语雀文档链接，文档内容与本地 Markdown 一致。

---

### 示例 2：从语雀下载文档到本地

**输入**：用户说「把语雀考试系统知识库里的「语雀知识库连接器配置技能」下载到本地」

**执行步骤**：
```
1. DeferExecuteTool("mcp__yuque__yuque_get_doc",
     {repo_id: "78381340", doc_id: "yuque-connector-skill", format: "markdown"})
   → 返回 Markdown 格式的文档正文
2. Write(file_path="C:/Users/Admin/下载/语雀知识库连接器配置技能.md",
         content=<返回的body>)
```

**实际返回结果**：
```
已下载到本地
文件路径: C:/Users/Admin/下载/语雀知识库连接器配置技能.md
文件大小: 4.2 KB
来源: https://www.yuque.com/jiuwu-tue7v/lerk9f/yuque-connector-skill
```

**用户拿到手的是**：本地 Markdown 文件，可在任意编辑器中打开编辑。

---

### 示例 3：批量下载整个知识库

**输入**：用户说「把考试系统知识库所有文档都下载到本地」

**执行步骤**：
```
1. DeferExecuteTool("mcp__yuque__yuque_list_docs", {repo_id: "78381340"})
   → 返回文档列表（含每篇文档的 id、title、slug）
2. 遍历每篇文档：
   DeferExecuteTool("mcp__yuque__yuque_get_doc",
     {repo_id: "78381340", doc_id: "<doc_id>", format: "markdown"})
   → Write("C:/Users/Admin/下载/考试系统知识库/<title>.md", <body>)
3. 批量间加 1 秒间隔（防 429）
```

**实际返回结果**：
```
已下载 12 篇文档到 C:/Users/Admin/下载/考试系统知识库/
├── 语雀知识库连接器配置技能.md
├── 考试平台使用指南（第1章）.md
├── 考试平台使用指南（第2章）.md
├── ...
└── 定价方案说明.md
```

**用户拿到手的是**：一个文件夹，里面是知识库全部文档的 Markdown 副本。

---

### 示例 4：上传 Excel 到语雀（多工作表拆分）

**输入**：用户说「把这个 Excel 传到语雀」

**执行步骤**：
```
1. Skill("xlsx") → 读取 Excel 所有工作表数据
2. 对每个工作表：
   - 将数据转为 Markdown 表格
   - 标题 = "{文件名} - {工作表名}"
   - DeferExecuteTool("mcp__yuque__yuque_create_doc",
       {repo_id: "78381340", title: "<标题>", body: "<Markdown表格>", format: "markdown"})
```

**实际返回结果**：
```
已导入 3 篇文档：
1. 销售数据.xlsx - Q1业绩 → https://www.yuque.com/jiuwu-tue7v/lerk9f/q1-ye-ji
2. 销售数据.xlsx - Q2业绩 → https://www.yuque.com/jiuwu-tue7v/lerk9f/q2-ye-ji
3. 销售数据.xlsx - Q3业绩 → https://www.yuque.com/jiuwu-tue7v/lerk9f/q3-ye-ji
```

**用户拿到手的是**：3 个语雀文档链接，每个链接打开后是一张格式整齐的数据表格。

---

## 核心工作流

### 导入：本地文件 → 语雀

```
1. 读取源文件（Read 工具 / docx 技能 / xlsx 技能）
2. 转换内容为 Markdown 或 HTML
3. yuque_create_doc → 返回语雀链接
   参数: repo_id(必填), title(必填), body(内容), format("markdown"推荐), slug(可选), public(0/1)
```

### 下载：语雀 → 本地

```
1. yuque_get_doc(repo_id, doc_id, format: "markdown") → 获取文档正文
2. Write 保存到本地指定路径，文件名 = 文档标题 + ".md"
3. 返回保存路径给用户
```

### 批量下载：整个知识库/目录

```
1. yuque_list_docs(repo_id) 或 yuque_get_toc(repo_id) 获取文档列表
2. 循环: yuque_get_doc → Write，每篇间隔 1 秒
3. 汇总: 列出所有保存的文件路径
```

### 同步检查：对比本地与语雀差异

```
1. yuque_get_doc 获取语雀最新内容
2. Read 读取本地文件内容
3. 对比差异并报告：哪些文档语雀有更新、哪些本地有修改
4. 用户选择同步方向（上传/下载/双向合并）
```

---

## 下载功能详细说明

### yuque_get_doc 参数

```
repo_id:  知识库 ID（必填）
doc_id:   文档 ID 或 slug（必填）
format:   "markdown"（推荐，返回纯 Markdown）| "lake" | "html"
include_lake: true（同时返回 Lake 原始格式，保留 Mermaid 源码等）
```

### 下载时文件名处理

- 优先使用文档 `title` 作为文件名
- 清理非法字符（\/:*?"<>|）
- 添加 `.md` 扩展名
- 如目标目录已有同名文件，追加序号：`标题(2).md`

### 批量下载限流

- 每篇文档下载后等待 1 秒（防止 429 限流）
- 如遇 429，等待 5 秒后重试，最多重试 3 次
- 可通过 `yuque_get_toc` 先获取目录结构，选择性下载特定目录

---

## 进阶功能

### 1. 目录管理（组织知识库结构）

```python
# 获取当前目录结构
yuque_get_toc(repo_id="78381340")

# 在根目录下新建分组
yuque_update_toc(repo_id="78381340",
  toc_data='{"action":"appendNode","action_mode":"child","target_uuid":"","type":"TITLE","title":"月度报告"}')

# 在指定分组下添加文档（需要先知道分组的 uuid）
yuque_update_toc(repo_id="78381340",
  toc_data='{"action":"appendNode","action_mode":"child","target_uuid":"<分组uuid>","type":"DOC","title":"6月报告","doc_id":"<doc_id>"}')
```

**适用场景**：新知识库初始化、批量导入后整理目录、跨目录移动文档。

### 2. 文档搜索与引用

```python
# 搜索文档（全文搜索）
yuque_search(query="考试系统", type="doc")

# 搜索知识库
yuque_search(query="培训", type="repo")

# 搜索后获取全文
yuque_get_doc(repo_id="<id>", doc_id="<id>", format: "markdown")
```

**适用场景**：查找历史文档、引用已有内容到新文档中。

### 3. 文档更新（同步修改）

```python
# 更新已有文档内容
yuque_update_doc(repo_id="78381340", doc_id="272726945",
  title="6月周报（修订版）", body="<新内容>", format: "markdown")
```

**适用场景**：本地文件修改后同步到语雀、修正已上传文档的内容。

### 4. 小记（快速笔记）

```python
# 创建小记
yuque_create_note(body="今天完成了语雀连接器的配置工作")

# 列出小记
yuque_list_notes(limit=10)

# 获取小记详情
yuque_get_note(note_id="<id>")
```

**适用场景**：快速记录碎片想法、待办事项、临时笔记。

### 5. 知识库创建与管理

```python
# 创建新知识库
yuque_create_book(name="新项目文档", slug="new-project")

# 获取知识库详情
yuque_get_book(repo_id="78381340")

# 更新知识库信息
yuque_update_book(repo_id="78381340", name="新名称", description="更新后的描述")
```

### 6. Board 资源创建（思维导图/流程图）

```python
# 创建思维导图
yuque_create_resource(resource_type="board", type="mindmap",
  dsl="# 中心主题\n## 分支1\n### 细节\n## 分支2",
  doc_id=272726945)

# 创建流程图
yuque_create_resource(resource_type="board", type="flowchart",
  dsl="A[开始] --> B[处理] --> C[结束]",
  doc_id=272726945)
```

### 7. Markdown 内容处理注意事项

- **代码块**：确保用 ``` 包裹，语雀渲染器支持语法高亮
- **图片链接**：外部图片 URL（https://）可在语雀中正常显示；本地图片路径不会生效
- **表格**：使用标准 Markdown 表格语法，语雀完全支持
- **Mermaid 图表**：使用 `include_lake: true` 获取原始 Mermaid 源码
- **数学公式**：语雀支持 LaTeX 语法（$...$ 和 $$...$$）
- **锚点链接**：语雀文档内部链接格式为 `((doc_id '显示文字'))`

---

## 错误处理与自动恢复

### 常见错误及自动恢复策略

| 错误码 | 含义 | 自动恢复 | 手动处理 |
|--------|------|---------|---------|
| **401** | Token 无效/过期 | 自动提示重新获取 | 前往 [设置页](https://www.yuque.com/settings/tokens) 重新生成 |
| **403** | 权限不足 | 提示检查知识库权限 | 确认账号是否有该知识库的读写权限 |
| **404** | 文档/知识库不存在 | 提示检查 ID 是否正确 | 用 `yuque_list_books` 确认正确的 repo_id |
| **422** | 参数验证失败 | 自动修正常见参数问题（如 format 大小写） | 检查传入参数是否符合 API 要求 |
| **429** | 请求频率超限 | **自动等待 5 秒后重试，最多 3 次** | 批量操作时主动加大间隔（2-3 秒） |
| **500** | 语雀服务异常 | **自动等待 10 秒后重试，最多 2 次** | 稍后再试，或检查 [语雀状态页](https://www.yuque.com) |
| **网络超时** | 连接超时 | **自动重试 1 次** | 检查网络连接 |

### 重试机制（内置）

所有 MCP 调用遇到以下情况时自动重试：
```
重试条件: 429（限流）/ 500（服务异常）/ 网络超时
重试次数: 最多 3 次
重试间隔: 429→5秒, 500→10秒, 超时→3秒（指数退避）
失败后: 停止操作，报告失败详情和建议
```

### 配置写入失败恢复

如果 `~/.workbuddy/mcp.json` 写入失败：
1. 检查文件是否存在 → 不存在则创建（含基础结构 `{}`）
2. 检查 JSON 是否合法 → 不合法则读取原文件内容，修复后重写
3. 检查磁盘空间 → 空间不足则提示清理
4. 写入前自动备份原文件为 `mcp.json.bak`

### MCP 服务加载失败排查

如果语雀 MCP 工具无法调用：
1. **验证 MCP 配置**：读取 `~/.workbuddy/mcp.json`，确认 yuque 条目存在且格式正确
2. **验证 Token**：调用 `yuque_get_user` 测试连通性，失败则 Token 有问题
3. **验证 npx**：Bash 执行 `npx -y yuque-mcp --help` 确认包可下载
4. **重写配置**：以上均正常则删除 yuque 条目后重新写入
5. **最终回退**：如 MCP 确实无法加载，降级使用 `urllib` 直接调语雀 REST API：
   ```
   Base URL: https://www.yuque.com/api/v2
   认证: X-Auth-Token header
   端点: /user, /users/{login}/repos, /repos/{id}/docs, /repos/{id}/docs/{id}
   ```

### 批量操作断点续传

批量导入/下载超过 10 篇文档时：
1. 每成功一篇记录 doc_id 到临时进度文件
2. 如中途失败，重启后从进度文件中读取已完成的 doc_id
3. 跳过已完成，从中断处继续
4. 全部完成后删除进度文件

---

## 全部可用工具速查

### 文档操作（核心）

| 工具 | 用途 | 必填参数 | 可选参数 |
|------|------|---------|---------|
| `yuque_create_doc` | 创建/导入文档 | repo_id, title | body, format, slug, public |
| `yuque_update_doc` | 更新已有文档 | repo_id, doc_id | title, body, format, slug, public |
| `yuque_get_doc` | 读取文档内容 | repo_id, doc_id | format, include_lake |
| `yuque_list_docs` | 列出知识库文档 | repo_id | - |

### 知识库与目录

| 工具 | 用途 | 必填参数 | 可选参数 |
|------|------|---------|---------|
| `yuque_list_books` | 列出知识库 | login | - |
| `yuque_get_book` | 知识库详情 | repo_id | - |
| `yuque_create_book` | 创建知识库 | name | slug, description, public |
| `yuque_update_book` | 更新知识库 | repo_id | name, description, public, slug |
| `yuque_get_toc` | 获取目录结构 | repo_id | - |
| `yuque_update_toc` | 更新目录结构 | repo_id, toc_data | - |

### 搜索

| 工具 | 用途 | 必填参数 |
|------|------|---------|
| `yuque_search` | 搜索文档或知识库 | query, type(doc/repo) |

### 小记

| 工具 | 用途 | 必填参数 | 可选参数 |
|------|------|---------|---------|
| `yuque_list_notes` | 列出小记 | - | limit, page, status |
| `yuque_get_note` | 获取小记详情 | note_id | - |
| `yuque_create_note` | 创建小记 | body | - |
| `yuque_update_note` | 更新小记 | note_id | body |

### Board 资源

| 工具 | 用途 | 必填参数 |
|------|------|---------|
| `yuque_create_resource` | 创建思维导图/流程图 | resource_type("board"), type, dsl |
| `yuque_get_resource` | 获取 Board 内容 | resource_type("board"), resource_id |
| `yuque_update_resource` | 更新 Board | resource_type("board"), resource_id, dsl |

### 用户

| 工具 | 用途 |
|------|------|
| `yuque_get_user` | 获取当前用户信息（用于验证 Token 有效性） |

---

## 配置指南

> **首次使用必读**：本技能依赖语雀 MCP 连接器。每位使用者需要配置**自己的语雀 Token**，Token 不随技能分发。

### 第一步：获取你的语雀 Token

1. 打开 [语雀](https://www.yuque.com) 并登录**你自己的账号**
2. 点击右上角 **头像 → 设置 → Tokens**（直达：https://www.yuque.com/settings/tokens）
3. 点击 **新建令牌**
4. 权限勾选 **读取 + 写入**
5. 复制生成的 Token（**只显示一次，务必保存**）

### 第二步：配置 MCP 连接器

告知 AI 助手「配置语雀连接器」，并附上你的 Token。

助手会自动完成以下操作：
1. 读取 `~/.workbuddy/mcp.json`（保留已有配置）
2. 写入语雀条目：

```json
{
  "mcpServers": {
    "yuque": {
      "command": "npx",
      "args": ["-y", "yuque-mcp"],
      "env": {
        "YUQUE_PERSONAL_TOKEN": "<你自己的Token>"
      }
    }
  }
}
```

3. 写入前自动备份原文件为 `mcp.json.bak`

### 第三步：验证连接

配置后重启 WorkBuddy，助手会自动调用 `yuque_get_user` 验证连通性。返回你的用户名即表示成功。

### 换电脑怎么办？

- **Token**：跟随你的语雀账号，换电脑同样有效
- **MCP 配置**：需要重新写入（配置文件是本地的）
- **技能文件**：重新安装即可
- 只需把你的 Token 再贴给助手，一键恢复全部功能

---

## 已知限制

| 限制 | 说明 | 替代方案 |
|------|------|---------|
| 图片上传 | MCP 不支持通用图片附件 | 外部图片 URL 可在 Markdown 中直接引用 |
| 二进制文件 | 视频、音频等需手动上传 | 语雀网页端手动上传 |
| yuque_create_resource | 仅支持 board 类型 | 二进制文件用网页端上传 |

## 参考信息

- **npm 包**: `yuque-mcp`
- **官方仓库**: https://github.com/yuque/yuque-mcp-server
- **API Base**: `https://www.yuque.com/api/v2`
- **Token 设置**: https://www.yuque.com/settings/tokens
