---
name: sync-obsidian-to-lexiang
description: >-
  Obsidian vault 到腾讯乐享知识库的单向同步工具。支持全量同步和增量同步两种模式，
  能够将 Obsidian 中的目录结构和 Markdown 文档（含图片/附件）同步到乐享知识库。
  当用户提到「同步 Obsidian 到乐享」「把笔记同步到知识库」「Obsidian 乐享同步」
  「obsidian sync lexiang」等意图时触发此 skill。
version: "1.0.0"
category: productivity
tags: obsidian, lexiang, sync, markdown, chinese, knowledge-base
agent_created: true
---

# sync-obsidian-to-lexiang

将 Obsidian vault 的目录和文档同步到腾讯乐享知识库，支持全量同步和增量同步。

## ⚡ 核心设计：零配置 + 零 token

**脚本直接复用 Agent 内置乐享连接器的 OAuth 鉴权，调用乐享 MCP 端点完成全部同步。**

- **零配置**：用户只要在 WorkBuddy/QClaw 里授权过乐享连接器，脚本就能用，无需获取任何 app_key/secret，无需安装额外 skill。
- **零 token**：扫描、转换、创建目录、导入文档、上传附件、写 manifest、生成报告，全部由脚本自主完成，文档内容从不进入对话上下文。

LLM（你）只负责两件事：
1. **唤起 skill + 明确输入参数**（vault 路径、目标知识库/目录、冲突策略）
2. **同步完成后展示报告**

**绝对禁止**：逐篇读取文档内容、逐条调用乐享 MCP 工具导入。那会消耗大量 token，违背本 skill 设计初衷。

## 鉴权机制（技术细节）

脚本自动发现 Agent 内置连接器的 OAuth token：

```
~/.workbuddy/connectors/<profile>/tokens/lexiang-ol.txt   (WorkBuddy)
~/.qclaw/connectors/<profile>/tokens/lexiang-ol.txt        (QClaw)
~/.codebuddy/connectors/<profile>/tokens/lexiang-ol.txt    (CodeBuddy)
```

- 自动选择「未过期且有效期最长」的 token（多 profile 时）
- 调乐享 MCP（`https://mcp.lexiang-app.com/mcp`）时使用 **`X-Oneid-Access-Token`** 请求头（不是 `Authorization`）
- token 由 Agent 后台自动刷新（约 20 分钟一次），脚本每次读取最新值
- 可用环境变量 `LEXIANG_ONEID_TOKEN` 显式覆盖

> ⚠️ token 过期会返回 401，此时引导用户在 WorkBuddy「集成」页面重新授权乐享连接器即可。

## 前置条件

- Agent 已授权乐享连接器（连接状态为 connected）
- Obsidian vault 路径已知（自动从 `~/Library/Application Support/obsidian/obsidian.json` 检测）

## 使用流程（标准操作）

### 第一步：明确参数

与用户确认以下参数（缺失则询问，可推断则推断）：

| 参数 | 说明 | 默认 |
|------|------|------|
| `--mode` | `full`=全量，`incremental`=增量 | 首次用 full，之后 incremental |
| `--target-space-id` | 目标乐享知识库 space_id（**必填**） | 无 |
| `--target-folder-id` | 目标目录 entry_id | 空=知识库根目录 |
| `--vault-path` | Obsidian vault 路径 | 自动检测 |
| `--source-dirs` | 要同步的目录（空格分隔） | 空=全部 |
| `--conflict-strategy` | `lexiang_wins` / `obsidian_wins` | `lexiang_wins` |
| `--respect-move` / `--no-respect-move` | 目的端移动处理 | `respect_move=true` |
| `--dry-run` | 仅预览不执行 | 关闭 |

> 用户提供乐享链接时，从中提取 space_id（`/spaces/{id}`）/ folder entry_id（`/pages/{id}`）。

### 第二步：执行同步（一条命令，零 token）

```bash
python3 ~/.workbuddy/skills/sync-obsidian-to-lexiang/scripts/sync.py \
    --mode incremental \
    --target-space-id <SPACE_ID> \
    --target-folder-id <FOLDER_ID>
```

脚本会：
1. 自动发现并读取连接器 OAuth token
2. 扫描 vault（对比 manifest 判断新增/更新/跳过）
3. 创建目录 → 上传附件 → 导入/更新文档（直接调乐享 MCP，markdown 原文上传，服务端解析）
4. 按冲突策略处理乐享侧已更新的文档
5. 写入 manifest.json
6. 生成 Markdown 同步报告
7. **stdout 仅输出 JSON 摘要 + 报告路径**（不输出文档内容）

进度信息走 stderr 可实时查看；最终摘要走 stdout。

### 第三步：展示报告

读取 stdout 返回的 `report_path`，用 `present_files` 向用户展示同步报告。

### 建议：先 dry-run 预览

正式同步前，可加 `--dry-run` 预览将要执行的操作（不实际写入、不写 manifest、不需要 token）：

```bash
python3 .../sync.py --mode incremental --target-space-id <ID> --dry-run
```

## 冲突策略

详见 `references/conflict-strategy.md`。

- `lexiang_wins`（默认）：文档在乐享侧上次同步后有独立更新时，跳过本次覆盖（保护乐享编辑）
  - 判断方式：对比乐享 `edited_at` 与 manifest 的 `last_sync_at`
- `obsidian_wins`：Obsidian 变更始终覆盖乐享，不检查乐享侧

## 初始化配置（可选）

```bash
python3 .../sync.py --init --target-space-id <ID> --target-folder-id <ID>
```

在 vault 的 `.obsidian/plugins/sync-obsidian-to-lexiang/` 下生成 `config.json`。
之后执行同步可省略对应参数（从 config.json 读取）。

## 异常处理与一致性保证

### 1. 中断恢复（不重不漏）

- **增量落盘**：每成功创建/更新一篇文档或一个目录，立即把映射写入 `manifest.json`（不是等全部跑完才写一次）。
- **断点续传**：脚本启动时总是加载已有 manifest（即便 full 模式）。中途被 Ctrl+C / 崩溃 / token 过期中断后，重跑增量同步会：
  - 已同步且内容未变的 → 命中 content_hash 跳过
  - 未完成的 → 继续创建
  - **绝不重复创建**已存在的条目
- **兜底保存**：`try/finally` 确保异常退出时也保存 manifest，并输出 `status: interrupted/error` 摘要提示可重跑续传。

### 2. 目的端 entry 失效（被删除）

复用 manifest 中的 entry_id 前，先 `probe_entry` 探活。若该 entry 在乐享侧已被删除（返回 403/不存在），自动清除旧映射并**重新创建**，不会因指向失效 parent 而报错。
（探活结果带缓存，同一 entry 不重复请求。）

### 3. 目的端文件夹/文档被移动

`probe_entry` 同时返回条目当前的 `parent_id`，据此检测是否被移出目标目录。由 `respect_move` 开关控制：

| 配置 | 行为 |
|------|------|
| `respect_move=true`（默认） | **尊重移动**：仍更新原 entry（内容跟着走），不在目标目录重建。符合「用户主动整理」的直觉 |
| `respect_move=false` | **强制归位**：在目标目录重新创建一份，被移走的旧副本保留（对齐 iwiki 方案 S 的「移动后重建」） |

> 注：乐享侧的 entry_id 在移动后不变，所以默认策略下移动不会造成重复或丢失。

### 4. 跨会话 / 多进程并发（文件锁）

同步状态全部存在 vault 内（`manifest.json`），不绑定任何会话。**任意会话、任意时间、甚至换电脑**，只要打开同一 vault，读写的都是同一份 manifest，因此「换会话续传」天然成立，由上述 entry_id 幂等 + content_hash 跳过保证不重不漏。

唯一风险是**两个进程同时**对同一 vault 跑同步（并发覆盖 manifest）。为此引入文件锁：

- 同步开始时在 `.obsidian/plugins/sync-obsidian-to-lexiang/.sync.lock` 原子创建锁（`O_CREAT|O_EXCL`），写入 pid + host + 时间戳。
- 运行中第二个进程获取锁失败 → 输出 `status: locked` 并以退出码 **2** 退出，不会破坏正在进行的同步。
- 正常结束 / 异常 / Ctrl+C 均通过上下文管理器自动释放锁。
- **陈旧锁自动接管**：同机持锁进程已死，或持锁超过 1 小时（`LOCK_STALE_SECONDS`），或锁文件损坏 → 判定为陈旧，新进程接管。避免崩溃后死锁。
- dry-run 不写状态，不加锁。

> 实践建议：跨会话使用时**串行执行**（一次只跑一个同步任务）。锁是兜底保护，不是用来支持并发同步的。

## 中间产物（均在 vault 内，跟随 vault）

```
{vault}/.obsidian/plugins/sync-obsidian-to-lexiang/
├── config.json              # 同步配置
├── manifest.json            # 源端路径 → 乐享 entry_id 映射 + content_hash（跨会话事实源）
├── .sync.lock               # 同步运行锁（防并发，结束自动删除）
└── reports/                 # 同步报告目录
    └── sync_report_YYYYMMDD_HHMMSS.md   # 自动保留最近 10 份
```

## 核心脚本

| 文件 | 职责 |
|------|------|
| `scripts/sync.py` | 同步执行器（扫描 + 调连接器 + 写 manifest + 报告） |
| `scripts/lexiang_api.py` | 乐享连接器客户端（token 发现 + MCP 调用 + 文档/附件操作） |
| `scripts/manifest.py` | manifest.json / config.json 读写 |
| `scripts/converter.py` | Wikilink→Markdown 转换、图片/附件引用解析 |
| `scripts/report.py` | 同步报告生成、旧报告清理 |
| `scripts/test_sync.py` | 单元测试 + 集成测试（回归用，83 个用例） |
| `scripts/cleanup_test_entries.py` | 归拢乐享侧测试遗留目录到「_待删除-测试遗留」夹，便于人工一键删 |

## ⚠️ 测试铁律（开发者必读）

乐享 MCP 连接器**没有删除 entry 的工具**（只有删 block / 移动 entry）。一旦在真实知识库建了测试目录，脚本删不掉，只能让用户在乐享界面手动删 —— 这很烦。因此：

1. **端到端测试一律用本地临时 vault**（`tempfile.mkdtemp()` 造 `.obsidian/` + 几篇 md），dry-run 验证逻辑；需要真实写乐享时，**目标目录也建在一个明确的临时夹**，测完立即归拢。
2. **测完必清**：测试产生的乐享目录，用 `cleanup_test_entries.py` 归拢到「_待删除-测试遗留」，并提醒用户删除该夹。
3. **约定**：所有测试用的乐享目录名以下划线 `_` 开头（如 `_e2e_test`），方便 `cleanup_test_entries.py` 自动识别。
4. 单元/集成测试（`test_sync.py`）默认全部离线（dry-run + FakeConnector），不碰网络、不建真实 entry。

## 同步范围（文件类型）

递归扫描 vault 下所有子目录，自动检测各层级的新增 / 更新：

| 源端文件 | 同步为 | 处理方式 |
|---------|--------|---------|
| 纯文本 `.md` | 乐享 page | 传 markdown 原文，服务端解析为正文 blocks |
| **图文 `.md`（含本地内嵌图）** | 乐享 page（图文混排） | 见下方「图文内嵌」 |
| PDF / Office / 独立图片 / 其他 | 乐享 file 条目 | 原文件上传（apply→PUT→commit），内容变化则重新上传 |
| `.canvas` / `.DS_Store` / 隐藏文件 | 跳过 | 系统/Obsidian 内部文件，不同步 |

### 图文内嵌（正文里的本地图片）

当 `.md` 正文引用了**存在的本地图片**（`![[img.png]]` 或 `![](本地路径)`）时，脚本会把图片真正内嵌到乐享正文（image block），而非留下一行路径文字。机制：

1. `split_into_segments` 把 markdown 按本地图片切成有序片段：`文本 / 图片 / 文本 …`
2. 建空骨架 page → 清空 → 按原始顺序逐片段写入：
   - 文本片段 → `block_convert_content_to_blocks` 转 block → `block_create_block_descendant`
   - 图片片段 → `block_apply_block_attachment_upload`（拿 session_id）→ PUT 上传 → image block（`image.session_id`，服务端自动转 file_id）
3. **顺序严格保持**：逐片段 append，文图穿插不错位

说明：
- **公网图片** `![](https://...)`：保留在文本片段里，乐享 `entry_import_content` 会**服务端自动抓取**并转 image block，无需脚本处理。
- 本地图片走 block 内嵌（上面流程）；独立图片文件（未被任何 md 引用）走 file 条目。
- 受 `sync_attachments` 开关控制（默认 true）。关闭时图文 md 退化为纯文本导入。

> 这解决了「只同步 .md、漏掉独立 PDF/附件」的问题。增量同步会递归发现任意子目录下新增的任意类型文件。

## 关键设计决策

- **鉴权**：复用 Agent 内置连接器 OAuth token（`X-Oneid-Access-Token` 头），零配置零 token
- **递归扫描**：`os.walk` 递归遍历所有子目录，自动检测各层级新增/更新
- **文件类型**：`.md`→page，其他类型→file 条目；系统/隐藏文件自动跳过
- **源端标识**：文件相对路径（相对 vault 根目录），同目录下文件名唯一 → 路径天然唯一
- **变更检测**：content_hash（SHA256）+ mtime，page 与 file 均检测
- **中断安全**：每项成功立即落盘 manifest + try/finally 兜底，重跑增量不重不漏
- **entry 探活**：复用前 probe_entry 校验存在性与父目录（带缓存），失效则重建
- **源端重命名/移动**：视为「旧文件删除 + 新文件创建」
- **目的端移动**：respect_move 开关控制（默认尊重移动，不重建）
- **源端删除**：跳过，不触发乐享侧删除（安全第一）
- **文档导入**：直接传 markdown 原文给乐享 MCP `entry_import_content`，服务端解析为 blocks（无需本地转换）
- **附件**：通过连接器 3 步上传（apply→PUT→commit），`.md` 引用替换为乐享 URL；上传失败不阻断文档同步
- **Wikilink**：`![[img]]` / `[[note]]` 转为标准 Markdown 格式

## 已知限制

- 乐享 MCP 连接器**不提供删除 entry 的工具**（只能删 block）。源端删除的内容需用户在乐享界面手动删除。
- 个人知识库的 OpenAPI（app_key/secret）模式与连接器 OAuth 身份不互通，本 skill 统一走连接器模式。

## 注意事项

- 调乐享 MCP 必须用 `X-Oneid-Access-Token` 头，用 `Authorization: Bearer` 会 401
- 遇 401（token 过期）→ 引导用户在 WorkBuddy 重新授权乐享连接器
- 单次同步大量文档时，进度走 stderr 可实时观察
