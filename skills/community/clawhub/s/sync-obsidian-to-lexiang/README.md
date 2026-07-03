# sync-obsidian-to-lexiang

将 [Obsidian](https://obsidian.md/) vault 单向同步到[腾讯乐享知识库](https://lexiangla.com/)的 Agent Skill，支持**全量同步**与**增量同步**，覆盖目录结构、Markdown 文档、图文混排、独立附件（PDF/Office/图片等）。

> 这是一个为 [WorkBuddy](https://www.codebuddy.cn/) / QClaw 等内置「乐享连接器」的 AI Agent 设计的 Skill。

## ✨ 核心特性：零配置 + 零 token

不同于「让 Agent 逐篇读文档、逐条调 API」的传统做法，本 Skill 的同步逻辑**全部封装在 Python 脚本里，直接复用 Agent 内置乐享连接器的 OAuth 鉴权调用乐享 MCP 端点**。

- **零配置**：用户只要在 Agent 里授权过乐享连接器即可，无需申请 `app_key`/`app_secret`，无需配置环境变量。
- **零 token**：扫描、转换、建目录、导入文档、上传图片、写状态、生成报告全部由脚本自主完成，**文档内容从不进入大模型上下文**。即使同步几百篇含图文档，正式同步的 token 消耗 ≈ 0。

大模型只在两个时点介入：① 唤起 Skill、确认参数；② 同步完成后展示报告。

## 🏗️ 实现机制

```
┌─────────────────────────────┐
│  AI Agent（仅确认参数 + 看报告）│
└──────────────┬──────────────┘
               │ 一条命令：python3 sync.py ...
               ▼
┌─────────────────────────────┐
│   sync.py  同步执行器（纯脚本）  │
│   扫描 vault → 对比 manifest    │
│   → 调连接器 → 写状态 → 报告     │
└──────────────┬──────────────┘
               │ 复用连接器 OAuth token
               │ X-Oneid-Access-Token 头
               ▼
   https://mcp.lexiang-app.com/mcp（乐享 MCP 端点）
               │
               ▼
        腾讯乐享知识库
```

### 鉴权：复用 Agent 内置连接器

脚本自动发现 Agent 内置连接器的 OAuth token（`~/.workbuddy/connectors/<profile>/tokens/lexiang-ol.txt`），用 `X-Oneid-Access-Token` 请求头直连乐享 MCP 端点。token 由 Agent 后台自动刷新，脚本每次读取最新值。

### 状态管理：manifest 跟随 vault

同步状态全部存在 vault 内部 `{vault}/.obsidian/plugins/sync-obsidian-to-lexiang/`：

| 文件 | 作用 |
|------|------|
| `manifest.json` | 源端相对路径 → 乐享 entry_id + content_hash 映射（跨会话事实源） |
| `config.json` | 目标知识库、目录、冲突策略等配置 |
| `.sync.lock` | 运行锁（防并发，结束自动删除） |
| `reports/` | 每次同步的人可读报告（自动保留最近 10 份） |

因为状态跟随 vault 而非会话，**任意会话、任意时间、甚至换设备**打开同一 vault，读写的都是同一份 manifest —— 跨会话续传天然成立。

## 📁 支持的知识类型

递归扫描 vault 下所有子目录，自动检测各层级的新增/更新，按类型分派：

| 源端文件 | 同步为 | 处理方式 |
|---------|--------|---------|
| 纯文本 `.md` | 乐享 **page** | 传 markdown 原文，服务端解析为正文 blocks |
| 图文 `.md`（含本地内嵌图） | 乐享 **page**（图文混排） | 文本/图片切片，图片走 block 附件上传内嵌为 image block |
| PDF / Office / 独立图片 / 其他 | 乐享 **file** 条目 | 原文件上传（apply → PUT → commit） |
| 目录 | 乐享 **folder** | 按层级递归创建，保持目录树 |
| `.canvas` / `.DS_Store` / 隐藏文件 | 跳过 | 系统/Obsidian 内部文件 |

### 图文内嵌（正文里的本地图片）

当 `.md` 正文引用了存在的本地图片（`![[img.png]]` 或 `![](path.png)`）时，脚本会把图片**真正内嵌到乐享正文**（image block），而非留下一行路径文字：

1. 把 markdown 按本地图片切成有序片段：`文本 / 图片 / 文本 …`
2. 文本片段 → 乐享 `block_convert_content_to_blocks` → `block_create_block_descendant`
3. 图片片段 → `block_apply_block_attachment_upload` 拿 session_id → PUT 上传 → image block
4. 严格保持原始顺序，文图穿插不错位

> 公网图片 `![](https://...)` 由乐享服务端在导入时自动抓取，无需脚本处理。

## 🔁 同步模式

- **全量同步** `--mode full`：首次或需要完整镜像时使用。
- **增量同步** `--mode incremental`：仅处理新增/变更内容。变更检测基于 `content_hash`（SHA256）+ `mtime`。

## 🛡️ 一致性与异常处理

| 场景 | 处理 |
|------|------|
| **中断恢复** | 每项成功立即落盘 manifest + try/finally 兜底；重跑增量同步不重不漏 |
| **目的端 entry 被删除** | 复用前 `probe_entry` 探活，失效则自动重建 |
| **目的端被移动** | `respect_move` 开关：默认尊重移动（不重建），可切换为强制归位 |
| **跨会话并发** | `.sync.lock` 文件锁，第二个进程被拒（退出码 2），陈旧锁自动接管 |
| **源端删除** | 跳过，不触发乐享侧删除（安全第一） |

冲突策略（`conflict_strategy`）：

- `lexiang_wins`（默认）：乐享侧在上次同步后有独立编辑时，跳过覆盖，保护协作成果。
- `obsidian_wins`：Obsidian 变更始终覆盖乐享。

详见 [`references/conflict-strategy.md`](references/conflict-strategy.md)。

## 🚀 使用方式

本 Skill 由 AI Agent 自动唤起。对 Agent 说「把 Obsidian 同步到乐享」即可。也可手动运行脚本：

```bash
# 初始化配置（写入 vault 的 .obsidian/plugins/ 下）
python3 scripts/sync.py --init \
    --target-space-id <知识库ID> --target-folder-id <目标目录ID>

# 全量同步
python3 scripts/sync.py --mode full \
    --target-space-id <知识库ID> --target-folder-id <目标目录ID>

# 增量同步（之后日常使用）
python3 scripts/sync.py --mode incremental \
    --target-space-id <知识库ID> --target-folder-id <目标目录ID>

# 预览（不实际写入）
python3 scripts/sync.py --mode incremental --target-space-id <ID> --dry-run
```

### 常用参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--mode` | `full` / `incremental` | — |
| `--vault-path` | Obsidian vault 路径 | 自动检测 |
| `--source-dirs` | 仅同步指定子目录（空=全部） | 全部 |
| `--target-space-id` | 目标乐享知识库 ID | — |
| `--target-folder-id` | 目标目录 entry_id（空=根目录） | 根目录 |
| `--conflict-strategy` | `lexiang_wins` / `obsidian_wins` | `lexiang_wins` |
| `--respect-move` / `--no-respect-move` | 是否尊重目的端移动 | 尊重 |
| `--dry-run` | 仅预览不执行 | 关闭 |

## 📂 项目结构

```
sync-obsidian-to-lexiang/
├── SKILL.md                       # Skill 描述（Agent 加载入口）
├── README.md
├── scripts/
│   ├── sync.py                    # 同步执行器（扫描 + 调连接器 + 写状态 + 报告）
│   ├── lexiang_api.py             # 乐享连接器客户端（token 发现 + MCP 调用 + 文档/图片操作）
│   ├── manifest.py                # manifest/config 读写 + 文件锁
│   ├── converter.py               # Wikilink→Markdown 转换、图文切片
│   ├── report.py                  # 同步报告生成、旧报告清理
│   ├── cleanup_test_entries.py    # 测试遗留目录归拢清理工具
│   └── test_sync.py               # 单元 + 集成测试（83 个用例，全离线）
└── references/
    └── conflict-strategy.md       # 冲突与一致性策略详解
```

## 🧪 测试

```bash
python3 scripts/test_sync.py -v
```

83 个用例，全部离线运行（dry-run + FakeConnector），不触网、不建真实条目。

## ⚠️ 已知限制

- 乐享 MCP 连接器**没有删除 entry 的工具**（只能删 block / 移动 entry）。源端删除文档不会触发乐享侧删除；测试遗留目录可用 `cleanup_test_entries.py` 归拢后人工删除。
- 单向同步：Obsidian → 乐享。不支持反向同步。

## 📄 License

MIT
