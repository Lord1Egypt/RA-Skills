# IMA OpenAPI 实战踩坑库

按探针版本倒序排列。每个段都是一次"端点 + 实测请求 + 真响应"的复盘。

---

## v14 实战（2026-06-05 14 篇 usecases-zh 批量上传 + 验证）

### 发现 1：`browse-kb` 单次 limit 硬上限 50，验证子文件夹文件数必须分页

**症状**：批量传完 14 篇 usecases-zh 增量（8 纯增量 + 6 部分覆盖）到子文件夹 `YOUR_FOLDER_ID`，然后跑 `browse-kb` 验证——`data.knowledge_list` 返回 **50 篇**，`is_end: false`，`next_cursor: "CDI="`。第一眼以为"14 篇新传没进去"（旧 42 + 14 应该是 56，但看到 50 没增加），实际是**分页上限问题**。

**实测命令**：

```bash
# 第 1 页（默认 limit=50）
ima browse-kb <kb_id> <folder_id>
# 返回：{knowledge_list: [50 条], is_end: false, next_cursor: "CDI="}

# 想拉 100 条？
ima browse-kb <kb_id> <folder_id> "" 100
# 返回：{"code":51,"msg":"invalid GetKnowledgeListReq.Limit: value must be inside range (0, 50]"}
```

**根因**：`GetKnowledgeListReq.Limit` 范围是 `(0, 50]`——**硬上限 50**，传 51+ 触发 code=51 参数越界。

**修正 / 验证子文件夹真实总数的正确姿势**：

```bash
# 第 1 页：拿 cursor
RESP1=$(ima browse-kb $KB_ID $SUBFOLDER)
CURSOR=$(echo "$RESP1" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['next_cursor'])")
PAGE1_LEN=$(echo "$RESP1" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']['knowledge_list']))")

# 第 2 页：用 cursor 翻
RESP2=$(ima browse-kb $KB_ID $SUBFOLDER "$CURSOR" 50)
PAGE2_LEN=$(echo "$RESP2" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['data']['knowledge_list']))")
IS_END=$(echo "$RESP2" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['is_end'])")

echo "总条数 = $((PAGE1_LEN + PAGE2_LEN)), is_end=$IS_END"
# 子文件夹 50 + 7 = 57 篇（实际是 42 旧 + 14 新 + 1 旧残留）
```

**错误码 51 触发场景扩充**（v13 之前只覆盖 `list-notebook` / `list-note` 不传 limit 或 limit=0）：

| 端点 | 错误码 51 触发场景 | 备注 |
|---|---|---|
| `list-notebook` / `list-note` | limit=0 / 不传 limit | 旧规则 |
| `browse-kb` | limit > 50 | **本条新增**（v14 实战）|
| 其他 browse/list 端点 | 推测同上 | **未验证**——按"硬上限 50"同样处理 |

**含义 / 写盘后验证硬闸升级**：

- ❌ "看第 1 页 50 条没增加" = **不能**下结论说"传失败"
- ✅ 必须**分页拿全**（`page1 + page2 + ... + pageN`），`is_end=true` 才算完整
- ✅ 自动化核验脚本里加一个"分页循环拿全"函数，别只看首页
- ✅ **跟 v13 GATE 3 查重并列**——这两个都是"看着像错但实际是验证姿势问题"的典型坑

**心跳检查升级**（v10/v11/v13 旧版只查 `if [[ -n "$$fid" ]]` / GATE 3 / GATE 3 查重范围）：

```bash
# 想确认子文件夹真实文件数 = 必须分页
~/.hermes/skills/ima/bin/ima browse-kb "$KB_ID" "$SUBFOLDER" 2>&1 | python3 -c "
import json, sys
j = json.load(sys.stdin)
print('is_end=', j['data']['is_end'], 'page1=', len(j['data']['knowledge_list']))
if not j['data']['is_end']:
    print('⚠️ 还有下一页，必须 cursor 翻')
"
```

### 发现 2：含全角冒号的中文文件名 Linux 文件系统 + IMA 上传都支持

**症状**：`usecases-zh/电商多 Agent 架构：从查数到全链路自动运营.md` 这种含**全角冒号 `：`** 的文件名，担心：
1. Linux 文件系统不接受（导致 `mv` 失败）
2. IMA 端点不接受（导致 `upload-file` 失败）

**实测**：
1. Linux 文件系统：`touch "test_电商_架构：从查数.md"` + `ls` → ✅ 创建成功、列出正常
2. IMA 上传：`upload-file` + `check_repeated_names` → ✅ 全 code:0，落到子文件夹 `parent_folder_id` 正确
3. KB 端验证：`browse-kb` 找到完整标题 + `media_id` 正常

**含义**：

- **H1 标题 = 文件名**（按 SKILL.md 默认规则 2）这条硬规则**不限制**标点符号
- 中文标点（`：` / `（）` / `——` / `？` / `！`）都可作 H1 一部分
- 特殊字符**只有 `/` 和 `\` 不能用**（Linux 文件系统限制），其他都行
- v12 实战踩坑（`head -1` 取到空行后 `cp` 失败）跟"全角冒号不支持"**无关**——v12 坑是 H1 提取 + mv 链的 bug，不是文件名字符限制

**写盘硬闸简化**（v12 旧规则要"先把非法字符替换"可**部分废弃**）：

- ✅ 全角中文标点 = 保留
- ❌ 半角 `/` 和 `\` = 必须替换为 `-` 或其他
- ❌ 半角 `?` `*` `<` `>` `|` `"` = 必须替换（虽然 v14 没测，但跟 Linux 文件系统规则一致）

---

## v13 实战（2026-06-05 42 篇 usecases 翻译批量上传）

### 发现 1：`upload-file` GATE 3 按**内容指纹**查重，不是按文件名

**症状**：批量上传 42 篇翻译到「OpenClaw 参考方案」子文件夹（`YOUR_FOLDER_ID`）。**前 1 篇**用旧名 `ai-video-editing_zh.md` 手动 `upload-file` 成功（KB title = `ai-video-editing_zh.md`）。后续把所有 42 篇本地文件**改成 H1 中文名**（如 `通过对话进行 AI 视频剪辑.md`）后重传——41 篇成功，**`通过对话进行 AI 视频剪辑.md` 这篇**失败：

```json
{"code":-100,"msg":"GATE 3: 同名文件已存在。请加 --force 自动加时间戳后缀保留两者，或手动改名。"}
```

**根因推断**：`check_repeated_names` 端点**不只查文件名**，还查**内容指纹**。本场景下：
- 旧项 `ai-video-editing_zh.md` 已存在于子文件夹（手动传的）
- 新传 `通过对话进行 AI 视频剪辑.md`（H1 重命名后）—— **文件名不同**但**内容相同**
- GATE 3 触发 = 按内容判重复

**错误信息歧义**："同名文件已存在" 字面是按名查重，实际是按内容。这是腾讯 IMA 错误信息的字面/实际不符（类似 v11 发现 4 的 210005 "not author" 实际是"媒体类型不支持"）。

**含义 / 修正错位的可行路径**：
- ❌ "改文件名不换内容"重传修正错位 = 不可行（除非 `--force`）
- ❌ "用 slug 名重传覆盖"= 不可行
- ✅ **唯一干净修正**：用户 IMA App 手工删旧 → 重新 `upload-file`（**不**带 `--force`）
- ✅ 想保留新旧两份 = 传 `--force`，CLI 自动加 `_YYYYMMDDHHmmss` 后缀

**对应 SKILL.md 默认规则 2**（KB 文件标题 = H1）的实战含义：
- 第一版用英文文件名传 = 错位
- 改 H1 中文名后重传 = **可以**用 `--force` 保留两份（错的英文 + 对的中文）
- **更干净** = 用户 IMA App 手工删错的，再传 H1 中文名

**心跳检查升级**（v10/v11 旧版只查 `if [[ -n "$fid" ]]`）：

```bash
# 想确认 check_repeated_names 的 body 字段对不对，看 bin/ima 注释+实测
grep -nB 2 -A 5 'check_repeated_names' ~/.hermes/skills/ima/bin/ima
# 看 params[] 里 name 的值（是不是带后缀？跟 file_name 一致？）
```

### 发现 2：`check_repeated_names` 的 `folder_id` 决定查重范围

**实测**：同 KB 下，**根目录**的旧 `a.md` 跟**子文件夹**下的新 `b.md`（内容相同）**不**触发 GATE 3（不同 folder 范围）。**同子文件夹**下触发。

**含义**：
- 跨子文件夹复制内容是安全的（不会触发 GATE 3）
- 同子文件夹重传 = 触发
- 想"把内容从 A 文件夹复制到 B 文件夹" = 安全可行
- 想"在 A 文件夹替换" = 需先删旧的

---

## v11 探针（2026-06-04 `rename-note` 对 markdown 实测）

### 发现 1：`rename-note` 只对 note 媒体生效，对 KB 上传文件无效

**症状**：对「方案跑通」里的 markdown 文件（`media_id=markdown_YOUR_UID_bfc4e068...`）调 `rename-note` 想改成 `Hermes Agent v0.15.1 本机安全审计（2026-06-04）.md`：

```bash
ima rename-note 'markdown_6e79dd5d...' 'Hermes Agent v0.15.1 本机安全审计（2026-06-04）.md'
# → {"code":210005,"msg":"RenameNote not author","request_id":"..."}
```

**对比**（同一时间调真 note）：
```bash
ima rename-note '7468267769700677' '【已挂载KB-勿删】Hermes Agent v0.15.1 本机安全审计（2026-06-04）'
# → {"code":0,"msg":"success","data":{}}
```

**根因推断**：
- 端点 `openapi/note/v1/rename_note` 名字带 "note"——只对 `note` 媒体类型（`media_type=11`）开放
- 对 `media_type=7`（markdown 文件）拒绝
- 错误码 210005 字面 "not author" 是误导——**实际是"该媒体类型不支持 rename_note"**（不是权限问题）

**含义**（比 v10 更严重）：
- KB 上传的 markdown 文件**标题一旦定下来不可改**
- "修标题"的唯一办法：**新文件 + 新 file_name + 重新 upload-file** → 产生新 COS 对象 + 新 KB 条目 → 旧文件必须 IMA App 手工删
- **之前 SKILL.md 说的"rename-note 是唯一可用的修复动作"要修正**——它对**误创的真 note** 仍能用（加 `【勿删】` 前缀等），但**对 KB 上传的 markdown 文件无效**

### 发现 2：用户默认规则 ——「KB 文件标题 = 文章 H1」

**场景**：想把审计文章（`# Hermes Agent v0.15.1 本机安全审计（2026-06-04）`）上传到「方案跑通」。
- **错做法**：用 slug 化文件名 `hermes-security-audit-2026-06-04.md` 上传 → KB 标题 = `hermes-security-audit-2026-06-04.md` ≠ 文章 H1，违反默认规则
- **正做法**：`mv` 本地文件成 `Hermes Agent v0.15.1 本机安全审计（2026-06-04）.md`（含中文 / 标点 / 版本号，跟 H1 一字不差）→ 再 `upload-file` → KB 标题 = 文章 H1 ✓

**执行规则**（`upload-file` 前必做）：
1. 读文章 H1（第一行 `# ...`）
2. `mv` 本地文件成 H1 文字（保留 `.md` 扩展名）—— 跟 H1 完全一致，不是 slug
3. 再 `upload-file`

**为什么不能 slug 化**：KB 文件在搜索 / 列表里按 title 排序，slug 化 = 用户扫一眼看不懂 = 违反"知识库是给自己 / 团队看"的初衷。`hermes-agent` 文档说"title MUST equal file_name (with extension)"——所以**让 file_name = H1 是最干净的解**。

### 发现 3：v10 修复后注释误导还在

**症状**：`bin/ima` 的 v10 修复段（add_knowledge 阶段附近）注释里写"命名空间遵循 create_folder v9 探针结论：纯数字 (e.g. YOUR_TARGET_FOLDER_ID)，不要 folder_ 前缀"。

**实际**：v11 探针已确认 `add_knowledge` 端点**要带 `folder_` 前缀**（纯数字 → 222000 文件夹不存在）。这条注释**误导了今天的 agent**（又试了一次纯数字错 222000）。

**修复方向**：改注释前先实测 `upload-file <kb_id> <file> YOUR_TARGET_FOLDER_ID` 和 `upload-file <kb_id> <file> YOUR_TARGET_FOLDER_ID` 两次，确认带前缀才是真确的，再修注释。**不要凭"我之前写的就是对的"改注释**——`bin/ima` 是会变的，注释可能跟实现脱节。

**心跳检查升级**：
```bash
# 旧：检查 if [[ -n "$fid" ]] 分支还在
grep -n 'if \[\[ -n "\$fid" \]\]' ~/.hermes/skills/ima/bin/ima

# 新（v11）：还要检查注释的字段名跟实际请求一致
grep -nB 1 -A 1 'folder_id' ~/.hermes/skills/ima/bin/ima
# 看注释里说的形式（纯数字 / 带前缀）跟 printf body 里 json.dumps 的形式是否一致
```

---

## v10 探针（2026-06-04 修复 `upload-file` 时发现）

### 发现 1：同一 KB 内 `folder_id` 在不同端点接受形式不同

**最坑的点**：跨端点不一致——**`create_folder` 跟 `add_knowledge` 对 folder_id 的形式要求相反**。

| 端点 | 接受形式 | 例子 | 错传后果 |
|---|---|---|---|
| `create_folder` | **带 `folder_` 前缀**（v11/13 确认） | `YOUR_PARENT_FOLDER_ID` | 纯数字 → `code:222001 文件夹不存在`（v13 实测） |
| `add_knowledge`（文件模式） | **带 `folder_` 前缀** | `YOUR_TARGET_FOLDER_ID` | 纯数字 → `code:222000 文件夹不存在` |
| `add_knowledge`（笔记模式） | **不接受** folder_id | — | 必落 KB 根（不能用此模式进子文件夹） |
| `import_doc`（note 命名空间） | note 笔记本 hash id | `folder453087040e892a2d` | wiki folder id → `code:310001 文件夹不存在` |

**复盘路径**：
1. 任务：把审计 md 上传到「OpenClaw·技术策展库 / 🧪 验证记录 / 方案跑通」
2. 第一次试 `upload-file <kb_id> <file> YOUR_TARGET_FOLDER_ID`（纯数字，照搬 v9 探针 `create_folder` 结论）
3. preflight ✓ → check_repeated_names ✓ → create_media ✓ → cos-upload 200 → add_knowledge 返 `code:222000 文件夹不存在`
4. 第二次试 `upload-file <kb_id> <file> YOUR_TARGET_FOLDER_ID`（带前缀）
5. 全过，新文件 `parent_folder_id=YOUR_TARGET_FOLDER_ID` 验证落在「方案跑通」✓

### 发现 2：`upload-file` 封装历史上漏 `folder_id`（已修复 2026-06-04）

**症状**：`upload-file <kb_id> <file> [folder_id]` CLI 接受第 3 参数，但文件**永远落 KB 根**——因为 add_knowledge 阶段构造的 JSON body 没有 `folder_id` 字段。

**根因**（在 `bin/ima` 行 401 附近）：原版只构造了 `media_type`/`media_id`/`title`/`knowledge_base_id`/`file_info` 五字段，没有 `folder_id`。

**修复**：增加 `if [[ -n "$fid" ]]` 分支，传入时添加 `"folder_id":<fid>` 字段。**复测**验证：传 `folder_xxx` 形式 → 真落到对应子文件夹。

**心跳检查**（下次进 skill 先 grep 这一行确认修复还在）：
```bash
grep -n 'if \[\[ -n "\$fid" \]\]' ~/.hermes/skills/ima/bin/ima
# 期望：1 个匹配，在 add_knowledge 阶段附近
```

**注释里**有误导：修复时写的注释说"命名空间遵循 create_folder v9 探针结论：纯数字"——**实际错了**，add_knowledge 要带前缀。修复 comment 也修了，但**没修成**（见 v10 后续 TODO）。下次有人看 `bin/ima` 注释，要看实测不要看注释。

### 发现 3：只看一半 API 列表就下结论

**症状**：在 SKILL.md「写入入口选型表」里看到 `add-knowledge --note` 没有 folder_id → 立刻判断"无法进 KB 子文件夹" → 跟用户说"做不到，去 IMA App 拖"。

**实际**：还有 `add-knowledge`（5 参文件模式）+ `upload-file` 4 步流水线（preflight → check_repeated_names → create_media → cos-upload → add_knowledge）可以走，是**唯一**能进 KB 子文件夹的路径。

**教训**：写"无法做 X"前必须**完整扫一遍** 23 个子命令（list-notebook / list-note / search-note / get-doc / new-doc / append-doc / list-kb / addable-kb / get-kb / browse-kb / search-kb / add-url / get-media / check-name / create-media / add-knowledge / create-folder / create-kb / move-kb-item / create-notebook / rename-notebook / rename-note / upload-file）以及它们**调用的底层端点**（不看 case 实现只读 help 也不行——help 只列 subcommand，不列端点 body 字段）。

---

## v9 探针（2026-06-04 实战踩坑）

### 发现 1：跨命名空间 folder_id 不能混用

- `import_doc` 的 `folder_id` 是 **note 命名空间**（`list-notebook` 拿到的 `folder<32hex>` 形式）
- KB 子文件夹的 `folder_<digits>` 是 **wiki 命名空间**
- 错把 wiki folder id 给 `import_doc` → `code:310001 文件夹不存在`

### 发现 2：笔记挂 KB 后无法移到子文件夹

- `add_knowledge` 的笔记模式（`media_type=11`）**没有 folder_id 参数**，笔记必进 KB 根
- `move_knowledge` 端点返 `code:0` 但 `move_results:{}`，**实际不移动**（3 类 KB 都一样；详见 SKILL.md 源码 `bin/ima` 行 232-248 的注释，腾讯可能后端占位/未实现）
- 唯一进 KB 子文件夹的路径：文件上传模式（`upload-file` 4 步流水线）

### 发现 3：CLI 误创的 note 无法删除

- `import_doc` 误调（参数错、传空等）会创建**空内容笔记**到默认 notebook
- 跑 `ima new-doc --help` 会把 `--help` 当 content 误创 1 个空标题笔记（看 help 用 `ima --help`，别带子命令）
- **OpenAPI 不暴露 `delete_doc` 端点**——只能去 IMA 客户端 UI 手工清理，或保留复用（不浪费 quota）

---

## v8 探针（2026-06-04 之前的发现）

### `rename_note` 端点真存在

- 端点：`openapi/note/v1/rename_note`
- 字段：`note_id` + `title`
- 真生效（code:0）
- **唯一可用的"修复"动作**——能改笔记标题，配合误创场景保留+改名（例如把 "误创" 改名为 "[保留] 误创 2026-06-04"），但不能删除

---

## 错误码速查

| code | 含义 | 触发场景 |
|---|---|---|
| 0 | 成功 | — |
| 51 | 参数值越界 | `list-notebook`/`list-note` 不传 limit 或 limit=0；`browse-kb` 传 limit>50（v14 实战：硬上限 50）；其他 browse/list 端点推测同上 |
| 222000 | 文件夹不存在 | `add_knowledge` 传错形式 folder_id（纯数字应带前缀）/ 引用了不存在的 folder |
| 310001 | 文件夹不存在（note 命名空间）| `import_doc` 错传 wiki folder id |
| 210001 | 必填字段为空 | `rename_note` 的 note_id 或 title 空（命名是 camelCase 但 body 用 snake_case） |
| 210005 | 媒体类型不支持 rename | `rename_note` 调 markdown 文件 / 非 note 媒体（字面 "not author" 是误导） |
| 100030 | 字段错误 | `rename_notebook` 字段名不对（v8 探针时 RAW=0；疑似腾讯内部错误码泄漏）|
| -100 | 程序错误 | 缺凭证、参数非法、缺 apiPath、网络错误。`msg` 已含修复建议 |
| -200 | skill 需更新 | `ima_api` 启动检查发现新版本；原请求未发送；从 stdout 读 `instruction` |

---

## 批量建子目录的 bash 编码坑

- bash 变量名**不能用中文**（`L1_每日快报=folder_xxx` 在 `set -euo pipefail` 下报 `command not found` 被吞，导致 `$L1_每日快报` 解析成空字符串 → `create_folder` 收到的 `folder_id` 字段为空 → 全建到 KB 根）
- 修复方式：用 **`scripts/build_kb_structure.py`**（python 调 ima_api.cjs，天然支持中文键名）
