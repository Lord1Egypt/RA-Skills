# Changelog

## 1.1.7-hermes.3 (2026-06-04)

### 探针 v8 新发现

- **`openapi/note/v1/rename_note` 端点真存在 + 真能用**（code:0 success，已 search-note 验证标题真改了）
  - 字段 `note_id` + `title`（不是 `new_title` / `name`）
  - 错误信息命名是 camelCase (noteId/title) 但 body 实际用 snake_case
  - **跟 `rename_notebook` 区别**：前者改**单条笔记标题**，后者改**笔记本名**
  - 之前 6 轮探针都没找到，因为命名风格从 `notebook` 切到 `note`（少一个 book）
- **bin/ima.sh 新增 `rename-note` 子命令**（hermes 同步 + 文档同步）

### 探针 v8 其他结果（20 个 guess）

- **5 个"半暴露"端点全部 RAW=0 失败**（错误码暗示但路由层硬拒）：
  - `openapi/note/v1/update_doc` ← VERSION_CONFLICT 暗示有
  - `openapi/note/v1/delete_doc` ← NOTE_IS_DELETE 暗示有
  - `openapi/note/v1/transfer_note` ← NOTE_NOT_OWNER
  - `openapi/note/v1/share_doc` ← SHARE_DOC_NOPERM
  - `openapi/wiki/v1/delete_media` ← 同理
- **15 个变体名（rename_note / delete_kb_item / share_kb / set_tag 等）全 RAW=0**——腾讯对这些动词完全不开路由
- **唯一新发现：rename_note**（上面那条）

### 关键调整

- **按 KB 权限矩阵表格增加"改笔记标题"行**：`rename-note` 跨 3 类 KB 全可用
- **重点怀疑端点段标注 v8 探针结果**：5 个半暴露端点全部 RAW=0 失败
- **新增"v8 探针意外收获"段**：记录 rename_note 发现的命名规律（notebook → note 简化）

### 不变

- API 端点路径严格 1:1 映射原版（`bin/ima.sh` 不发明新接口）
- 凭证路径不变（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`）

## 1.1.7-hermes.2 (2026-06-04)

### 实测增信（基于层次 A 端到端验证）

#### 字段修复 / 实测注释

- **`get-media` 字段名修复**：`id` → `media_id`（原 51 invalid，现 0 success）
  - 错误信息 `"GetMediaInfoReq.MediaId"` 是腾讯内部 proto 字段名，CLI 序列化时要全小写
- **`create-folder` 字段实测确认**：`knowledge_base_id`（不是 `kb_id`）
  - 副作用：根目录立刻出现新 folder（`parent_folder_id` = KB 根），真实可用
- **`create-kb` 字段实测确认**：`type: KBT_MINE_KB`（不是 `name`）
  - `type=KBT_MINE_KB` 真创建，`name` 入 `list-kb` 第一项
- **`move-kb-item` 端点存在但不实现"移动"语义**（3 种场景全无效）
  - (a) KB 内文件夹间移动 → code:0 但文件位置不变
  - (b) 跨 KB 移动 → code:0 但文件位置不变
  - (c) 跨 KB + dst_folder_id → code:0 但文件位置不变
  - 结论：端点可能为腾讯内部占位/未实现
- **`rename-notebook` 真实行为**：早期 310001 → 现 code:0 + data:{}（改名"成功"）但 list-notebook **未生效**
  - 改名任意 → 100030 "名称已被占用"（即便是新笔记本 + 全新名）
  - 结论：腾讯对系统默认笔记本 (folder_type=0) 不允许改名；用户自建笔记本改名也频繁冲突

#### 按 KB 类型的"删/改/移"权限矩阵（实测）

账号 `<NICKNAME>` 3 类代表 KB × 4 能力：

| 能力 | ① 个人 | ② 参与共享 | ③ 我创建共享 |
| --- | --- | --- | --- |
| `create-folder` | ✅ code:0 | ❌ 220030 权限不足 | ✅ code:0 |
| `rename-notebook` | 100030 | 100030 | 100030（全局一致）|
| `move-kb-item` (KB 内) | code:0 但**不动** | code:0 但**不动** | code:0 但**不动** |
| `move-kb-item` (跨 KB) | code:0 但**不动** | code:0 但**不动** | code:0 但**不动** |
| `delete-*` | RAW=0 | RAW=0 | RAW=0 |

#### 官方文档系统核查（2026-06-04）

完整读完腾讯官方 `ima-skills-1.1.7.zip` 的 `knowledge-base/references/api.md`（595 行）+ `notes/references/api.md`（365 行）：

- **官方承认的 16 个端点**：create_media / add_knowledge / get_knowledge_base / get_knowledge_list / search_knowledge / search_knowledge_base / get_addable_knowledge_base_list / check_repeated_names / import_urls / get_media_info（知识库 10 个）+ search_note / list_note / get_doc_content / import_doc / append_doc / list_notebook（笔记 6 个）
- **官方没有**任何 `delete_*` / `rename_*` / `move_*` / `share_*` / `tag_*` 端点
- **错误码反推**：`210006 NOTE_IS_DELETE` / `210008 VERSION_CONFLICT` / `210005 NOTE_NOT_OWNER` / `210011 SHARE_DOC_NOPERM` 暗示后端有这些功能但**未在 OpenAPI 暴露**

#### 重点怀疑端点（值得未来重新探针）

- `openapi/note/v1/update_doc` ← VERSION_CONFLICT 暗示
- `openapi/note/v1/delete_doc` ← NOTE_IS_DELETE 暗示
- `openapi/wiki/v1/delete_media` ← 同理
- `openapi/note/v1/transfer_note` ← NOTE_NOT_OWNER
- `openapi/note/v1/share_doc` ← SHARE_DOC_NOPERM

#### 新增文档

- `references/api-quirks.md`：从 hermes 装的 runtime 同步过来
  - 新增章节：**按 KB 类型的"删/改/移"权限矩阵**、**官方文档 vs 探针交叉核对**
  - 给 LLM 调度者的硬约束：禁止发明"删除的封装"或"标记性删除"

### 不变

- API 端点路径严格 1:1 映射原版（`bin/ima.sh` 不发明新接口）
- 凭证路径不变（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`）
- 原 SKILL.md 顶层"5 个未文档化端点"声明不变

## 1.1.7-hermes.1 (2026-06-04)

### 改造（基于腾讯官方 v1.1.7）

- **OpenClaw 风格 frontmatter → Hermes 风格 frontmatter**
- **增加 `bin/ima.sh` POSIX 桥接**：18 个子命令（16 个原版端点 + 5 个未文档化端点 - 3 个 - ? + 1 个便利封装）
  - 笔记：list-notebook / list-note / search-note / get-doc / new-doc / append-doc
  - 知识库：list-kb / addable-kb / get-kb / browse-kb / search-kb / add-url / get-media
  - 上传：check-name / create-media / add-knowledge / upload-file（封装）
  - 高级：create-folder / create-kb / move-kb-item / create-notebook / rename-notebook（**未文档化但真实存在**）
- **凭证路径对齐 Hermes `.env` 约定**：`IMA_OPENAPI_CLIENTID` + `IMA_OPENAPI_APIKEY`
- **新增 `_meta.json` + `skill-card.md`**：按 mmx-cli 模板

### 探针发现

通过对 ima.qq.com 域做穷举式主动探针（POST 50+ 候选端点，观察 RAW 响应长度），发现 5 个原版 SKILL.md / api.md 文档中**未列出**但实际可用的端点：

- `openapi/wiki/v1/create_folder`
- `openapi/wiki/v1/create_knowledge_base`
- `openapi/wiki/v1/move_knowledge`
- `openapi/note/v1/add_notebook`
- `openapi/note/v1/rename_notebook`

字段结构按探针实际响应反推，未经腾讯官方文档背书。

### Roadmap

- 🟡 **删除 / 移动 / 重命名相关指令正在开发中**
  腾讯 OpenAPI 路由层经主动探针确认未暴露 delete 端点，需在桌面/移动端手工操作或通过 cookie 自动化曲线实现。
- ⚪ 标签管理、知识库分享/成员管理正在评估
- ⚪ 与腾讯桌面端/移动端的 UI 自动化集成（待评估）

### Verified

- 22 个端点（16 文档化 + 5 探针发现 + 1 便利封装）端到端真请求跑通
- bin/ima.sh 22 个子命令（含 1 个便利封装）全部能用
- 凭证加载逻辑（IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY）通过 `check_weixin_requirements` 同款 `check_ima_requirements` 验证

## 1.1.7 (2026-04-22, 腾讯官方)

原始发布。来源：https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip
