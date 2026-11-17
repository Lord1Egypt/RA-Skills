# 安全准则

> 任何破坏性操作前必读。任何不可逆操作必须先备份 + 用户确认 + 操作日志。
>
> ⚠️ **2026-09 重要更新**：IMA 平台当前 API **不支持**笔记、文件夹、文件的删除操作（仅支持标签删除）。详见第 3 节。

## 1. 破坏性操作清单

| 操作 | API | 风险 | 保护级别 |
|------|-----|------|:--------:|
| ~~删除笔记~~ | ~~`delete_note`~~ | ❌ **API 不支持** | — |
| 删除标签 | `tag_delete` | 所有关联自动解除 | 🔴 高 |
| 重命名标签 | `tag_rename` | 新名重复会**自动合并** | 🔴 高 |
| 移动文件 | `move_knowledge` | 标签数组可能清空 | 🟡 中 |
| ~~删除文件夹~~ | — | ❌ **API 不支持** | — |
| ~~删除文件~~ | — | ❌ **API 不支持** | — |

**IMA 平台删除能力边界（2026-09 现状）**：
- ✅ 可删除：标签（`tag_delete`）
- ❌ 不可删除：笔记、知识库、文件夹、文件、媒体
- 不可删除对象的处理方式：用户需在 **IMA 客户端手动删除**

## 2. 通用保护原则

1. **备份优先**：所有破坏性操作前必须先备份到本地
2. **三重确认门**：备份完成 + 内容已验证 + 用户显式确认
3. **操作日志**：每次破坏性操作后必须记录到 `/sandbox/workspace/logs/note_operations.log`
4. **优先用可逆方案**：`tag_remove` 优于 `tag_delete`，创建新笔记优于删除旧笔记
5. **影响范围可见**：执行前必须告诉用户"将影响 X 个文件/标签"
6. **IMA 限制认知**：删除笔记/文件夹/文件只能让用户在客户端操作，不要尝试构造或寻找删除 API

## 3. 删除笔记 — **改用客户端手动操作 + 新笔记替代模式**

> ⚠️ **重要变化**：IMA 平台当前 API **不支持删除笔记**（`delete_note` 已无效）。
> 原 v4.0.0 的"安全删除流程"中的 `delete_note` curl 调用是**无效操作**，必须改为：
> 1. **创建新笔记替代**（推荐）
> 2. **告知用户在 IMA 客户端手动删除**

### 3.1 推荐方案：创建新笔记替代旧笔记（推荐）

**核心思路**：不删除旧笔记，创建内容完全的新笔记，标注替代关系。

```bash
# 1. 读取旧笔记内容（保留作为版本历史）
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<旧note_id>","target_content_format":1}' | \
python3 -c "
import sys, json
d = json.load(sys.stdin)
if d['code'] == 0:
    content = d['data']['content']
    backup_path = f'/sandbox/workspace/backups/notes/{d[\"data\"][\"note_id\"]}_backup.md'
    with open(backup_path, 'w') as f: f.write(content)
    print(f'已备份旧笔记到: {backup_path}')
"

# 2. 基于旧版本生成新内容（人工或 LLM 辅助）

# 3. 创建新笔记（获得新的 note_id）
curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d @new_note_request.json | python3 -m json.tool
# 返回: {"code": 0, "data": {"note_id": "<新note_id>"}}

# 4. 在新笔记中标注"替代旧版 v1.X（note_id=XXX）"
# 5. 旧笔记保留作为历史版本
# 6. 用户在 IMA 客户端手动决定是否删除旧笔记
```

**优势**：
- ✅ 完全规避 API 不支持删除的限制
- ✅ 保留版本历史，可回溯
- ✅ 零误删风险
- ✅ 用户拥有最终决定权

### 3.2 客户端手动删除流程

如需删除旧笔记，按以下流程告知用户：

**步骤 1：告知用户**
- 笔记标题：XXX
- 笔记 ID：XXX
- 删除位置：XXX（哪个笔记本）

**步骤 2：用户确认**
- 用户明确回复"确认删除"

**步骤 3：指引用户在 IMA 客户端操作**
- 打开 IMA 客户端 → 进入对应笔记本
- 找到目标笔记 → 右键 → 删除
- 或者：笔记右上角 ⋯ → 删除

**步骤 4：验证删除结果**
- 用 `list_note`（单数）API 确认笔记不在列表中

### 3.3 严禁操作

❌ **不要尝试**：
- 调用已失效的 `delete_note` API（即使文档还有说明）
- 构造或寻找其他"伪删除"接口
- 通过 `push_note` + `content_cos_key` 覆盖试图"擦除"内容
- 重试 `delete_note`（浪费时间）

✅ **应当做**：
- 明确告知用户 IMA 平台的 API 边界
- 推荐"创建新笔记替代"方案
- 指引客户端手动删除路径

## 4. 删除标签（`tag_delete`）保护

> ⚠️ 删除后所有关联自动解除，不可恢复。

调用前必须：
1. 用 `tag_list(keyword=新名)` 检查新名是否存在
2. 用 `get_knowledge_list(tags=[标签])` 列出受影响文件数
3. 告知用户所有关联自动解除且不可恢复
4. **用户显式确认**

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_delete" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "tag_name": "<标签名>"}'
```

## 5. 重命名标签（`tag_rename`）保护

> ⚠️ 新名重复会**自动合并**到旧名——所有文件可能被打上意外标签。

调用前必须：
1. 用 `tag_list(keyword=新名)` 检查新名是否存在
2. 若存在，告知用户会"自动合并"并显式确认
3. 用 `get_knowledge_list` 列出受影响文件数
4. **用户显式确认**

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_rename" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "old_tag_name": "<旧名>", "new_tag_name": "<新名>"}'
```

## 6. 移动文件（`move_knowledge`）保护

详见 [folder-organization.md](folder-organization.md) 第 0.4 节。

关键保护：
- 移动前**必须备份标签**（`move` 会清空标签数组）
- 移动后**逐个重新打标**

## 7. 操作日志

所有破坏性操作后必须记录：

```bash
# 追加到操作日志
echo "$(date -Iseconds) | <操作类型>: <note_id 或 tag_name> | 标题: <标题> | 备份路径: <路径>" \
  >> /sandbox/workspace/logs/note_operations.log
```

**日志格式**：

```
时间戳 | 操作 | ID | 标题 | 备份路径
```

**目的**：建立可审计的操作记录，万一误删可追溯。

## 8. 删除能力演进追踪

IMA 平台删除能力可能随版本变化，使用前建议：

1. 用 `npx clawhub inspect ima-knowledge` 或类似官方 skill 看最新规则
2. 检查 ima-knowledge SKILL.md 的"规则"部分是否有变更
3. 测试 API 是否已恢复支持

已知能力矩阵（2026-09-28 现状）：

| 操作 | 2026-05 试跑 | 2026-09 现状 |
|------|:------------:|:------------:|
| 删除标签 | ✅ 可用 | ✅ 可用 |
| 删除笔记 | ✅ 可用 | ❌ 不可用 |
| 删除文件夹 | ❌ 不可用 | ❌ 不可用 |
| 删除文件 | ❌ 不可用 | ❌ 不可用 |
| 删除知识库 | ❌ 不可用 | ❌ 不可用 |

> 💡 即使历史试跑中 `delete_note` 可用，**当前已不可用**。务必按 2026-09 现状执行。
