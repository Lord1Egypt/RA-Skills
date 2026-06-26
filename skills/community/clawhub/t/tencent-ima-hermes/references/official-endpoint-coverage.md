# IMA OpenAPI 官方端点覆盖核对（2026-06-04）

**目的**：未来 agent 接手 ima skill 扩展任务时，**先看这个文件再决定要不要探针**。绝大多数"删/移/改"路径已经被穷尽过。

**来源**：腾讯官方 `ima-skills-1.1.7.zip`（已留存在 `/tmp/ima_inspect/ima-skill/`）的 `knowledge-base/references/api.md` + `notes/references/api.md`（跟 hermes 改造版字节级相同）。**这两个文件是腾讯显式承认的端点全清单**。

---

## 官方 16 个端点（v1.1.7 全部）

**知识库 10 个**（`POST /openapi/wiki/v1/<action>`）：

| # | 端点 | 用途 | `bin/ima` 子命令 |
| --- | --- | --- | --- |
| 1 | `create_media` | 上传文件第一步（拿 COS 凭证） | `create-media` |
| 2 | `add_knowledge` | 上传第二步 / 笔记入知识库 | `add-knowledge` |
| 3 | `get_knowledge_base` | 知识库元信息 | `get-kb` |
| 4 | `get_knowledge_list` | 浏览知识库内容 | `browse-kb` |
| 5 | `search_knowledge` | KB 内搜索 | `search-kb` |
| 6 | `search_knowledge_base` | 搜索 KB 列表 | `list-kb` |
| 7 | `get_addable_knowledge_base_list` | 可添加的 KB 列表 | `addable-kb` |
| 8 | `check_repeated_names` | 文件名查重 | `check-name` |
| 9 | `import_urls` | 导入 URL 到 KB | `add-url` |
| 10 | `get_media_info` | 媒体访问信息 | `get-media` |

**笔记 6 个**（`POST /openapi/note/v1/<action>`）：

| # | 端点 | 用途 | `bin/ima` 子命令 |
| --- | --- | --- | --- |
| 1 | `search_note` | 搜索笔记 | `search-note` |
| 2 | `list_note` | 笔记列表 | `list-note` |
| 3 | `get_doc_content` | 读笔记内容 | `get-doc` |
| 4 | `import_doc` | 新建笔记 | `new-doc` |
| 5 | `append_doc` | 追加内容 | `append-doc` |
| 6 | `list_notebook` | 笔记本列表 | `list-notebook` |

---

## 探针额外发现的 5 个真存在端点（未文档化）

来源：6 轮探针（`/tmp/probe_ima_v2..v7.cjs` + `/tmp/probe_ima_final.cjs`）共 50+ 候选。

| 端点 | 字段 | 状态 |
| --- | --- | --- |
| `openapi/wiki/v1/create_folder` | `knowledge_base_id` + `name` | ✅ code:0 真创建 |
| `openapi/wiki/v1/create_knowledge_base` | `type` (`KBT_MINE_KB`/`KBT_SHARED_KB`) + `name` | ✅ code:0 真创建 |
| `openapi/wiki/v1/move_knowledge` | `src_knowledge_base_id` + `media_id` + `dst_knowledge_base_id` + `dst_folder_id` | ⚠️ code:0 但**实际不移动**（3 种场景全测过） |
| `openapi/note/v1/add_notebook` | `folder_name`（不是 name） | ✅ code:0 真创建 |
| `openapi/note/v1/rename_notebook` | `folder_id` + `folder_name` | ⚠️ code:0 但 list 实际**未生效**；新名报 100030 名称已被占用 |

---

## 官方**没有**的端点（用户最常问"为什么没有"）

  - ❌ `delete_note` / `delete_doc` / `delete_kb_item` / `delete_folder` / `delete_media` / `delete_knowledge_base` / `delete_notebook`
  - ❌ `rename_folder` / `rename_kb` / `rename_media` / `update_doc` / `edit_doc` / `modify_doc`
  - ❌ `move_folder` / `move_note` / `move_to_folder`（move_knowledge 端点存在但不实现移动语义）
  - ❌ `share_doc` / `share_kb` / `invite_member` / `change_role` / `permission_*`
  - ❌ `add_tag` / `remove_tag` / `set_tag` / `list_tags`
  - ❌ `archive_doc` / `restore_doc` / `trash_*` / `recycle_*`

**全部 RAW=0（腾讯路由层硬拒绝）** 或 51/100001（参数错但路径不通）。

---

## 错误码反推的"半暴露"端点（值得未来重新探针）

| 错误码 | 名称 | 强烈暗示存在的端点 |
| --- | --- | --- |
| `210006` | `NOTE_IS_DELETE` | `openapi/note/v1/delete_doc` 或 `delete_note` |
| `210008` | `VERSION_CONFLICT` | `openapi/note/v1/update_doc`（带 `version` 字段乐观锁） |
| `210005` | `NOTE_NOT_OWNER` | `openapi/note/v1/transfer_note` |
| `210011` | `SHARE_DOC_NOPERM` | `openapi/note/v1/share_doc` |
| `210012` | `USER_IS_DELETE` | 用户级删除（不在 OpenAPI 范围） |
| `210030` | `notebook_NAME_EXIST` | 同名查重（已有 add_notebook，拒绝逻辑暴露了重复检测） |
| `110020` | 安全打击 | 内容违规（已存在但非用户面） |
| `110021` | 请求频控 | 限流（非用户面） |

**未来探针建议**（如果用户明确要继续）：
  - `openapi/note/v1/update_doc` body: `{note_id, content, content_format, version}` —— VERSION_CONFLICT 强信号
  - `openapi/note/v1/delete_doc` body: `{note_id}` 或 `{note_ids:[]}` 批量 —— NOTE_IS_DELETE 强信号
  - `openapi/wiki/v1/delete_media` body: `{media_id}` —— 同理
  - `openapi/note/v1/share_doc` body: `{note_id, share_type, expire_time}` —— SHARE_DOC_NOPERM 强信号

**风险**：腾讯可能对未授权账号返回 RAW=0 拒服务（不是 51/100001），看起来跟"端点不存在"一样。需要真实场景触发（先创建内容再操作）才能区分。

---

## 按 KB 类型的"删/改/移"权限矩阵（实测 2026-06-04）

账号 `YOUR_ACCOUNT`（uid `YOUR_UID`）3 类代表 KB：

  - ① 个人库 `YOUR_PERSONAL_KB_ID`（"YOUR_ACCOUNT的知识库"，创建者）
  - ② 参与共享 `UUB5V03Vb0OOi_SJ2IsmgGYQO7UWd6zyvjv75DGCssg=`（"OpenClaw-实战知识库"，普通成员，186 人）
  - ③ 我创建共享 `3x7uG4a4kWAvXMaQLW1dh_gNo17Cujp1yU6iJrK3EUU=`（"OpenClaw小龙虾高级私享库"，创建者，489 内容）

| 能力 | 子命令 | ① 个人 | ② 参与共享 | ③ 我创建共享 |
| --- | --- | --- | --- | --- |
| 创建文件夹 | `create-folder` | ✅ code:0 | ❌ 220030 权限不足 | ✅ code:0 |
| 改笔记本名 | `rename-notebook` | 100030 名称冲突 | 100030 | 100030（全局一致）|
| KB 内移动文件 | `move-kb-item` | code:0 但不动 | code:0 但不动 | code:0 但不动 |
| 跨 KB 移动文件 | `move-kb-item` | code:0 但不动 | code:0 但不动 | code:0 但不动 |
| 删除类 | `delete-*` | RAW=0 | RAW=0 | RAW=0 |

**实战可用工作流**：
  - ① 个人库：create-folder / create-kb / upload-file / search-kb
  - ③ 我创建共享库：create-folder / upload-file —— **可用 OpenAPI 维护自己的共享库**
  - ② 参与共享库：browse-kb / search-kb / get-media —— **只读**
  - 删/移/改名：3 类都**走 ima 客户端 UI**

---

## 重要字段踩坑（写给未来的自己）

| 端点 | 错 | 对 | 错误信号 |
| --- | --- | --- | --- |
| `get_media_info` | `{id: "..."}` | `{media_id: "..."}` | 51 "GetMediaInfoReq.MediaId: value length must be at least 1 runes" |
| `create_folder` | `{kb_id: "..."}` | `{knowledge_base_id: "..."}` | 51 "value length must be at least 1 runes" |
| `create_knowledge_base` | `{name: "..."}` | `{type: "KBT_MINE_KB", name: "..."}` | 51 "value must be in list [KBT_MINE_KB KBT_SHARED_KB]" |
| `add_notebook` | `{name: "..."}` | `{folder_name: "..."}` | 100001 字段名错 |
| `list_notebook` | （无 limit） | `{"cursor":"","limit":20}` | 51 "value must be inside range (0, 20]" |
| `get_knowledge_base` | （无 ids） | `{"ids":["<kb_id>"]}` | 51 "value must contain between 1 and 20 items" |
| `search_note` | `{query:"..."}` | `{search_type, sort_type, query_info:{title/content}, start, end}` | 100001 ListNoteBook param is error |
| `create_media` | 读 `data.cos_key` | 读 `data.cos_credential.cos_key` | 空字符串 |

---

## LLM 调度者的硬约束（不能违反）

  1. **不要发明"删除的封装"或"标记为删除"** —— 违反腾讯 OpenAPI 使用条款
  2. **遇到"删除/移动/重命名"需求 → 直接告诉用户去 ima 客户端操作**，不要试图用 OpenAPI 假装能做
  3. **想恢复这些能力 → 走桌面客户端 cookie + Playwright 自动化**（层次 B 方案），但**需要用户明确决策**
  4. **任何新增端点必须先查这个文件 + 跑 Step 0**（读 references/api.md + 错误码表）—— 不要重做已穷尽的探针
  5. **写 SKILL.md 时标注"已探针穷尽"**，让用户能搜到结论

---

## 副作用数据清单（hermes 探针创建，待用户手工清理）

  - 知识库 7 个：hermes-probe-kb / hermes-probe-shared / hermes-final-test-kb / hermes-final-shared / 层次A-KB-162618 / 层次A-KB-端到端 / 层次A-收尾KB-163532
  - 文件夹 7 个（都在"YOUR_ACCOUNT的知识库"根）：hermes-probe-folder / hermes-final-test-folder / hermes-probe-v4-* / 层次A-新文件夹A / 层次A-验证-* / 层次A-端到端验证 / 层次A-收尾-*
  - 笔记本 1 个：层次A-原名（新建后 rename 失败）
  - 笔记 1 条："这是一条由 hermes skill bin/ima 创建的..."（note_id 7467969428850318）
  - 文件 1 个：ima-test-upload.txt

**OpenAPI 无 delete 端点 → 必须用户在 ima 客户端手工清理**。
