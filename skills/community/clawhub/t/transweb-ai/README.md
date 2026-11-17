# transweb-ai

一个跨客户端的 Agent Skill：用 **transweb.cn 自己的 API Key** 调用账号下的任意 AI Skill/应用。适用于任何支持 `SKILL.md` 的 Agent Skills 客户端。

默认支持生成**网页版 PPT、可视化图表、3D 手办建模、3D 动画和小游戏**；安装 `transweb-create` 后可无限拓展新功能，打造个人专属智能工具集。

- 识别到做 PPT/幻灯片/演示文稿的需求，自动走 `ppt` 命令（固定官方演示文稿应用）
- 默认覆盖网页版 PPT、可视化图表、3D 手办建模、3D 动画、小游戏等生成场景
- 其他需求优先通过 `/user/getLoginedData` 列出自己账号下的可用应用 ID（`pptItem.documentId`）
- 自己的应用没有匹配时，自动回退 `/user/getPublishedList`（公开市场）的 ID
- 按需求选择一个或多个 ID
- 单例执行，或按顺序链式执行（上一步输出作为下一步输入）
- 每步自动查询文档存档、设置可访问权限，返回 `?solo=true&dataView=true&dataId=...` 链接

> 创建 Agent/Skill 应用（资料转 Agent、需求转 Skill）已拆到独立技能 **`transweb-create`**；本技能只负责使用已有应用和生成 PPT。

## 安装

把 `transweb-ai/` 整个目录放到客户端扫描的 skills 目录。常见位置：

```text
Claude Code:   ~/.claude/skills/transweb-ai/
OpenClaw:      ~/.openclaw/skills/transweb-ai/
其他客户端:    <客户端 skills 目录>/transweb-ai/
```

只要客户端支持 `SKILL.md` 约定即可，不依赖特定运行时。

## 离线预览（沙箱 / 审核 / 无 API Key）

无需凭据、无需网络即可演示完整工作流：

```bash
python3 scripts/transweb_ai.py demo --json
python3 scripts/transweb_ai.py demo ppt --json
python3 scripts/transweb_ai.py ppt --input "做一份季度汇报 PPT" --dry-run --json
python3 scripts/transweb_ai.py selftest --json
```

`demo` / `--dry-run` 返回应用清单、串联执行步骤、PPT 页大纲等结构化预览；
`sample:true`、`created:false`、`network:false`、无真实链接，明确表示没有访问账号或创建文档。
真实执行请配置 API Key 后去掉 `--dry-run`。

## 配置

需要显式配置 Key；技能包**不包含默认 API Key**。`transweb-ai` 与 `transweb-create` 共用同一份 `transweb-ai.json` 配置。

```bash
python3 scripts/transweb_ai.py config show
```

需要重新配置时：

```bash
python3 scripts/transweb_ai.py configure --verify
# 或
python3 scripts/transweb_ai.py configure --api-key ak_live_xxx --verify
```

也支持 `TRANSWEB_API_KEY` 环境变量。配置位置（权限 `0600`），按以下顺序查找：

1. 自定义：`--config <path>` / `TRANSWEB_CONFIG`
2. 项目通用：`<项目>/.transweb-ai.json` 或 `<项目>/.transweb/transweb-ai.json`
3. 旧版项目兼容：`<项目>/.dsh/transweb-ai.json`
4. 用户级：`~/.config/transweb-ai/config.json`（遵循 `XDG_CONFIG_HOME`）
5. 旧版用户级兼容：`~/.dsh/transweb-ai.json`

`transweb-ai` 与 `transweb-create` 共用同一份配置。

Key 的 scope：

| scope | 用途 |
| --- | --- |
| `doc:read` | `list`（`/user/getLoginedData` 等标注接口） |
| `ai:chat` | `run`（`/gpt/aiGatewayRequest`） |
| `account:read` | 可选，`whoami`（`/user/getUserData`） |

注意：只有声明 `requiredScope` 的接口会校验。`getPublishedList`、`getDocumentData`、`publishPptItem`、`setDocumentStatus`、bucket 上传等不校验 scope；`doc:write` 当前未接入。

### 换 API Key / 多账号

```bash
# 替换当前 profile 的 Key
python3 scripts/transweb_ai.py configure --api-key ak_live_NEW --verify

# 新建 profile 并切过去
python3 scripts/transweb_ai.py configure --profile work --api-key ak_live_WORK --verify

# 查看 / 切换 / 删除 profile
python3 scripts/transweb_ai.py config list
python3 scripts/transweb_ai.py config use work
python3 scripts/transweb_ai.py config remove work

# 单次命令临时使用某个 profile
python3 scripts/transweb_ai.py ppt --profile work --input "..."
python3 scripts/transweb_ai.py list --profile work --query "PPT"
```

- 默认 profile 为 `default`，旧版扁平配置会自动识别为 `default`。
- `configure` 不带 `--profile` 更新当前 active；带 `--profile` 创建/更新并切换。
- `--api-key` / `TRANSWEB_API_KEY` 对单次命令优先级最高；`TRANSWEB_PROFILE` 可指定 profile。
- 配置文件结构：`{"active":"work","profiles":{"default":{...},"work":{...}}}`。

### 离线自检

```bash
python3 scripts/transweb_ai.py selftest --json
python3 scripts/transweb_ai.py --version
python3 -m unittest discover -s tests -v
```

不需要 API Key，不会发起网络请求。

## 使用

### 0. PPT 需求（自动映射）

用户提到 PPT、幻灯片、演示文稿、slides、deck、汇报材料、路演材料时，直接用 `ppt` 命令，不需要先 `list`：

```bash
python3 scripts/transweb_ai.py ppt   --input "主题、章节、每页要点或完整需求描述"   --json
```

固定使用「演示文稿」应用 `76f7de9504bad022a8978e9fe084df0f`，输出：

```json
{
  "ok": true,
  "link": "https://transweb.cn/?solo=true&dataView=true&dataId=...&id=76f7...",
  "dataId": "...",
  "documentId": "76f7de9504bad022a8978e9fe084df0f",
  "title": "演示文稿标题",
  "slides": 12,
  "pointsCost": 250,
  "archived": true,
  "accessible": true,
  "elapsedMs": 113000
}
```

支持 `--file` / `--stdin`、`--wait`、`--timeout`、`--share`。原 `transweb-ppt` 技能已并入本技能；需要可下载的 `.pptx` 文件时改用 `office-pptx`。

### 1. 列出可用应用（非 PPT 需求）

```bash
# 默认 auto：先自建，自建无匹配再公开市场
python3 scripts/transweb_ai.py list --query "PPT" --limit 10
python3 scripts/transweb_ai.py list --query "商业方案" --limit 10

# 显式来源
python3 scripts/transweb_ai.py list --source mine --limit 50
python3 scripts/transweb_ai.py list --source published --query "数据分析" --limit 10
python3 scripts/transweb_ai.py list --source both --query "PPT" --limit 10
```

`--source`：

| 值 | 行为 |
| --- | --- |
| `auto`（默认） | 先 `getLoginedData`，无匹配回退 `getPublishedList` |
| `mine` | 只查自己账号 |
| `published` | 只查公开市场 |
| `both` | 同时查，自建优先去重 |

自建默认只列已发布（`publishStatus: "true"`）；`--all` 会包含未发布。公开市场当前约 65 个。

返回每个应用的 `id`、`title`、`description`、`type`、`tags`、`category`、`appLabel`、`publishStatus`、`source`、`owner`、`folderName`。顶层看 `selectedSource` 和 `fallback`：

- `selectedSource: "mine"`：用了自建应用。
- `selectedSource: "published"` + `fallback: true`：自建无匹配，已回退公开市场。
- `selectedSource: "both"`：两类都返回，看 `apps[].source`。

### 应用类型：agent vs skill

`run` 会先调用 `/user/getDocumentData` 读取 `documentType`：

- `documentType: "agent"`：输出**字符串结果**，不生成链接、不查存档；
- `documentType: "skill"`：保持原来的**链接**输出（`dataId` + `?solo=true&dataView=true...`）；
- 缺失/未知：按 `skill` 兼容。

`list` 默认不带类型；需要时加 `--with-document-type`。

### 2. 单例执行

```bash
python3 scripts/transweb_ai.py run \
  --ids 76f7de9504bad022a8978e9fe084df0f \
  --input "生成一份关于 AI 数字劳动力的演示文稿" \
  --json
```

### 3. 链式执行

```bash
python3 scripts/transweb_ai.py run \
  --ids dcd76a6c644295cdc29b33bdbe825017,76f7de9504bad022a8978e9fe084df0f \
  --input "为一家 SaaS 公司做年度商业方案，并生成汇报 PPT" \
  --json
```

`--chain-mode`：

| 值 | 下一步输入 |
| --- | --- |
| `result`（默认） | 上一步输出 |
| `requirement` | 原始需求 |
| `both` | 原始需求 + 上一步输出 |

### 4. 选项

| 选项 | 说明 |
| --- | --- |
| `--wait` | 等待存档秒数，默认 15 |
| `--timeout` | 单步生成超时，默认 360 秒 |
| `--share` | 显式把存档设为公开可访问（默认私有、不分享） |
| `--json` | 输出 JSON |
| `--quiet` | 不输出进度 |

成功返回：

```json
{
  "ok": true,
  "link": "https://transweb.cn/?solo=true&dataView=true&dataId=...&id=...",
  "finalAppId": "...",
  "steps": [
    {"index": 1, "appId": "...", "link": "...", "dataId": "...", "accessible": true, "pointsCost": 250}
  ],
  "pointsCost": 250,
  "elapsedMs": 113000
}
```

失败时会保留已完成步骤：

```json
{
  "ok": false,
  "error": "...",
  "completed": [{"index": 1, "link": "..."}],
  "failedAppId": "...",
  "failedIndex": 2
}
```

## 工作方式

```text
PPT 需求 → ppt 命令（固定 76f7...）
        → 生成 / 存档 / 权限 / 链接

其他需求：
list  → 先 POST /user/getLoginedData（自建）
      → 有匹配：用自建 documentId
      → 无匹配：GET /user/getPublishedList（公开市场）
      → 取 pptItem.documentId 作为应用 ID

run   → 对每个 ID：
        POST /gpt/aiGatewayRequest {documentId, context}
        → 返回 usage.result
        → 服务端异步归档到 questionData
        → GET /user/queryQuestionData 匹配存档，取 _id
        → （仅 --share 时）POST /user/setDocumentStatus 设置 isShare=true
        → 拼接 ?solo=true&dataView=true&dataId=<_id>&id=<应用ID>
      → 下一步输入 = 上一步结果（默认）
```

HTTP 传输优先使用系统 `curl`（避免部分 macOS Python/OpenSSL 的 `SSL: UNEXPECTED_EOF_WHILE_READING`），无 curl 时回退 `urllib`。

## 排障

| 现象 | 处理 |
| --- | --- |
| `未登录` / Key 无效 | 重新创建 Key 并 configure |
| `缺少 scope` | 仅 `requiredScope` 接口会报；按接口补 `doc:read`/`ai:chat`/`account:read`，写接口不靠 scope 拦截 |
| 积分不足 | 充值；链式减少步数 |
| `list` 返回 0 条 | 换关键词；用 `--source both` 或 `--all` 查看 |
| `ppt` 缺少 slides | 上游模型输出异常；重试或把大纲写具体 |
| `auto` 只返回自建 | 没带 `--query`，无法判断“适合” | 加 `--query`，或 `--source published` |
| 找不到存档 | 加 `--wait 30`；确认积分/计费正常 |
| 下游结果不对 | 改用 `--chain-mode requirement`，或先单例确认输出 |
| `accessible: false` | 查看 `accessError`；可能非存档所有者 |

更细的接口字段见 [`references/api.md`](references/api.md)。

## 安全

- 不要在对话、代码或日志中回显完整 Key。
- Key 只保存在本地 `0600` 配置或环境变量中。
- 默认把每步存档保持私有、不分享；只有显式 `--share` 才会设为公开可访问。
- 每次生成、链式每一步都会消耗 transweb.cn 账号积分。
