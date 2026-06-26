# IMA 写入流程详细 Recipe

(2026-06-04 实战沉淀。在「OpenClaw·技术策展库」上传 Hermes Agent 安全审计时发现关键路径。)

## 0. 工作原则

**做坏了不擅自动手修复，先汇报情况。** 三栏汇报：正确（已做）/ 错位（已做）/ 需要常总手工处理（agent 做不了）。来源：常总 2026-06-04 强纠正。

## 1. 写入入口选型（已实测）

| 场景 | 命令 | 必读 |
|---|---|---|
| 笔记到「笔记本」 | `new-doc "<content>" [folder_id] [title]` | folder_id 必须 note 命名空间 (`folder<32hex>`)，**不是** wiki folder |
| 笔记挂到 KB | `add-knowledge --note <kb_id> <note_id> <title>` | **必进 KB 根**，无 folder_id 参数 |
| 文件到 KB（含子文件夹） | `upload-file <kb_id> <file> [folder_id] [--force]` | **唯一**能指定 KB 子文件夹的入口 |
| 移动 KB 内子文件夹 | `move-kb-item` | **空壳端点**，3 类场景实测全无效（code:0 + `move_results:{}`） |
| 删笔记 / 删 KB 项 | — | OpenAPI 不暴露，必须 IMA App 手工 |
| 改笔记标题 | `rename-note <note_id> <new_title>` | 唯一"修复"动作（v8 探针发现） |

## 2. upload-file 4 步流水线（看 `bin/ima` 行 288+）

```
GATE 1: preflight-check  → 返回 { file_name, file_ext, file_size, media_type, content_type, pass }
GATE 3: check_repeated_names (openapi/wiki/v1/check_repeated_names)
         body: { knowledge_base_id, folder_id, params:[{name, media_type}] }
         ⚠️ folder_id 传到这里，**不是**到 add_knowledge
GATE create_media (openapi/wiki/v1/create_media)
         body: { file_name, file_size, content_type, knowledge_base_id, file_ext }
         响应: { data: { media_id, cos_credential: { cos_key, bucket_name, region, secret_id, secret_key, token, start_time, expired_time } } }
         ⚠️ cos_* 字段全部嵌套在 cos_credential，**顶层只有 media_id**
GATE 5: cos-upload  → 走腾讯云 COS SDK PUT 文件，用 create_media 返回的临时 token（不是 .env 里的 API key）
GATE 2: add_knowledge (openapi/wiki/v1/add_knowledge)
         body: { media_type, media_id, title, knowledge_base_id, file_info: { cos_key, file_size, file_name } }
         title 必须 == file_name
```

## 3. 实战踩坑

### 3.1 跨命名空间 folder_id 混用 → 310001

`import_doc` 报 `code:310001 文件夹不存在`：100% 是把 wiki folder id (`YOUR_TARGET_FOLDER_ID`) 传给了 `import_doc`。它要的是 note notebook id (`folder<32hex>`)。

### 3.2 `ima new-doc --help` → 误创空标题笔记

CLI 不拦截子命令的 `--help`，把它当 $1 content 传进去。`new-doc` 用 $1 $2 $3 做 content/folder_id/title，参数错位就创建了 `content="--help" folder_id="" title=""` 的空笔记。

**正确看 help**：`ima --help`（不带子命令）。
**误创后处理**：
- 不能删（OpenAPI 无 delete_doc）
- IMA App 手工删
- 临时方案：`ima rename-note <note_id> "[待删-MD]误创-help"` 改标题做标记

### 3.3 add-knowledge 笔记模式不带 folder_id；文件模式 v10 修复后带

`bin/ima add-knowledge` case 根据 $1 是不是 `--note` 分两种 body：
- `--note` 模式（笔记挂 KB）：`{media_type:11, note_info:{content_id}, title, knowledge_base_id}` — 无 folder_id → KB 根（**OpenAPI 真没这字段**）
- 文件模式：`{media_type, media_id, title, knowledge_base_id, folder_id?, file_info:{...}}` — **v10 修复后**带 `folder_id`，CLI 第 3 参数 `fid` 会被序列化进去

**两种模式的 folder_id 形式要求**（v10 实测）：
- 文件模式要 **带 `folder_` 前缀**（`YOUR_TARGET_FOLDER_ID`）—— 与 `create_folder` 接受纯数字**相反**
- 传纯数字 → `code:222000 文件夹不存在`
- CLI 接受 `[folder_id]` 但 `add_knowledge` body 是否真的带，**必须 grep 验证**：`grep -n 'if \[\[ -n "\$fid" \]\]' bin/ima`（修复"心跳"）

**所以**：想进 KB 子文件夹**必须**走 `upload-file` 封装（它内含 v10 修复），且 folder_id 一定要带 `folder_` 前缀。`add-knowledge` 单独调（不走 upload-file 封装）= 无法进子文件夹。

### 3.4 不要只看 1 个 API 就下结论

本会话的真实错：先看 `add-knowledge`（笔记模式）发现没 folder_id，**就**断定"IMA 不能进 KB 子文件夹"——**没**回头看 `upload-file` 封装。**正确做法**：写操作前**先看完整 SKILL.md "写入"段**（本 skill 现在第 4 节），再下手。

## 4. 错位汇报三栏模板

发现操作错位时，按这个格式汇报（**不要**自我修复，**不要**省略）：

```
# 现状汇报

## 正确（已做）
- <note_id / media_id>「<title>」 @ <位置>

## 错位（已做）
- <note_id>「<title>」 @ <错的位置> — <错的原因，1 句话>

## 需要常总手工处理（agent 做不了）
1. 在 IMA App 把 X 拖到 Y
2. 在 IMA App 删 Z（<note_id>「<title>」）
```

## 5. 已验证 vs 未验证

**✅ 已实测（2026-06-04）**：
- `add-knowledge --note` 笔记模式：code:0 创建 KB 根笔记
- `move-kb-item` 空壳：code:0 但 `move_results={}`，文件位置不变
- `import_doc` folder_id 跨命名空间：实测 2 次 → `code:310001 文件夹不存在`
- `ima new-doc --help` 误创：实测 1 次（note_id 7468267522237257，title=`--help`）
- `upload-file` 完整跑到 KB 子文件夹：v10 修复后实测成功（传 `YOUR_TARGET_FOLDER_ID` 形式 → 落「方案跑通」✓；传纯数字 → 222000）

**❌ 未亲手跑通**：
- `rename_note` 真生效（v8 探针只验证了 RAW 响应长度，未跑真实改名）
- `add_knowledge` 文件模式**单独**调（不走 upload-file 封装）—— 理论上 v10 修复后也能工作，但本会话没单独验证

**🟡 SKILL.md 注释佐证未亲手验**：
- `move_knowledge` 3 类场景（KB 内移 / 跨 KB 移 / 跨 KB+folder）全无效
- `create_folder` 第 3 参数 `folder_id` 字段名正确（v8 探针验证）

## 6. 相关资源

- `~/.hermes/skills/ima/SKILL.md` line 58-63：v9 探针关键约束
- `~/.hermes/skills/ima/SKILL.md` line 4 节"写入操作必读"：本会话沉淀的核心约束
- `~/.hermes/skills/ima/bin/ima` 行 288+：upload-file 4 步封装
- `~/.hermes/skills/ima/knowledge-base/scripts/preflight-check.cjs`：GATE 1 实现
- `~/.hermes/skills/ima/knowledge-base/scripts/cos-upload.cjs`：GATE 5 实现
- `~/.hermes/skills/ima/references/official-endpoint-coverage.md`：官方 16 端点 + 5 探针端点全表
