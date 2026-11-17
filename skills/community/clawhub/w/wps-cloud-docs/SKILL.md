---
name: wps-cloud-docs
description: Use when 操作 WPS/金山文档云文档：新建、读改、表格、权限、导出。
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [wps, kdocs, 金山文档, cloud-doc, mcp]
    category: productivity
    author: 芦名竹
    name: WPS 知识库连接器（kdocs）
---

# WPS / 金山文档 连接器（Hermes 版）

## When to Use

需要读写 WPS 云文档（kdocs）时：新建文档/表格/多维表格、写入正文、批量改单元格、加协作者、导出 Markdown/PDF、搜索云盘、管评论标签。
不适用：企业 WPS 账号（服务端 403 拒绝）、线下 .docx 本地文件（用 microsoft-office 技能）。

## 一句话原理

WorkBuddy 的 `kdocs` 连接器就是一层壳，真实能力在 WPS 官方 **SkillHub MCP 服务**：
`https://mcp-center.wps.cn/skill_hub/mcp`（streamable-http，JSON-RPC 2.0）。
本技能自带客户端直连该服务，无需 WorkBuddy、无需 mcporter、无需 npm。

## 认证（唯一需要人工的一步）

1. 跑授权：`python3 <skill>/scripts/wps_auth.py`
   - 自动打开 `https://mcp-center.wps.cn/kdocs-auth/auth-guide?auth_code=<code>`
   - 必须用 **WPS 个人账号** 登录；企业账号返回 403，切账号后重跑
   - **在 Hermes 里必须以受管后台进程跑**：`terminal(command="cd <skill>/scripts && python3 -u wps_auth.py", background=true, notify=true)`，然后用 `process_manage(action="poll", session_id=...)` 读输出拿 auth 链接甩给用户。脚本是前台轮询型的，前台调用会吃满 300s 超时；`nohup`/`disown`/`setsid` 会被 Hermes 直接拒绝，且被拒后日志不会落在你重定向的文件里，只能从 process_manage 读。
   - 窗口 300s。用户没赶上就重跑脚本换新 auth_code（旧 code 失效）。
2. 脚本轮询 `api.wps.cn/.../wps_auth/exchange` 拿到 token，写入本技能的 token 文件（`WPS_KDOCS_TOKEN`，权限 0600）
3. 校验：`python3 <skill>/scripts/wps_mcp.py whoami` → `登录有效；工具数 638`
4. token 会过期（服务端给 `expires_in`，通常数十小时）。`whoami` 报「token 无效」就重跑授权。

`<skill>` = 本技能根目录（脚本/references 都放在这里）。

## 用法

```bash
S=<skill>/scripts

python3 $S/wps_mcp.py list                     # 全部 638 个工具
python3 $S/wps_mcp.py list --grep drive        # 按关键字筛
python3 $S/wps_mcp.py schema create_file_with_content   # 看入参 schema（调用前必看）
python3 $S/wps_mcp.py call create_file_with_content '{"name":"周报.otl","content":"# 本周进展\n..."}'
python3 $S/wps_mcp.py call <tool> --file args.json      # 参数太长时落文件
```

**调用铁律**：不确定参数就先 `schema`。WPS 工具描述里写明了必填项和后缀对应字段，硬猜会 400。

## 文档目录与整合规范（知识库交付）

知识库最终只推 **一个总档文档**，不要分主题/分篇推多个文件。

- 目录第一级：`Hermes agent`、`Obsidian` 两个主题；
- 同主题下按 `01-总览 → 02-安装与配置 → 03-核心机制 → 04-现有功能及用法 → 05-常见坑与排错 → 06-实战案例 → 07-延伸与参考` 的固定 8 节结构排列；
- 每篇文章的小节在**同一篇 .otl 文档内**连续排列，标题级别：主题一级，文章二级。

### 净化清理规则（推新文档前必须执行）

源文件里可能带内部残留，推新文档前必须逐个清掉：

1. 内部路径：`/a-home/`, `/Users/lumz/a-home/...` → 删除或改为“你的知识库工作目录”
2. 内部命令：`cp "$1" /Users/lumz/a-home/...` → 删掉或改成“`cp <源文件> <目标目录>`”
3. 脚手架注释：`# 00-收件箱`、`# 01-主题索引`、`# 02-主题` 这类目录说明 → 删除
4. 内部引用：`$base$/50-项目/...` → 改成真实相对路径，或直接删掉
5. 机型/版本号错位：如果有“Python 3.xx/0.11.28”这种看起来不对的值，改“3.9.6/0.11.28”

## 写整篇 Markdown 的正确姿势（实测踩过）

**`create_file_with_content` 会把 YAML frontmatter 当正文渲染**（`---\ntitle: ...\n---` 变成一颗大标题），交付文档必须先剥：

```python
def strip_fm(t):
    if t.startswith("---"):
        p = t.split("---", 2)
        if len(p) >= 3: return p[2].lstrip("\n")
    return t
```

改已存在文档正文（不新建重复文件）的三步：

1. `otl.convert` params `{"content": md, "format": "markdown"}` → `data.detail.result.blocks`
   - ⚠️ 必须传 `format: "markdown"`，只传 `type: "markdown"` 报 `Invalid parameter: format is invalid`
2. 去掉首块（convert 会把第一个 `#` 生成 heading），改由自己给 title
3. `otl.block_update` params:**列表**，每项 `{"operation":"update_content","blockId":"doc","content":[{"type":"title",...}, ...blocks]}`
   - `blockId=doc` 时 content 首个子节点**必须是 title**
   - 缺 `operation` 或写成 `content`/`blocks` 直挂 → `code 400100`

读回验证：`otl.block_query` `{"file_id": fid}` → `data.detail.result.blocks`。

## 合并成单一文档 + 多级标题（实测踩过）

用户要「所有内容收进一个文档」时：

1. **不要一次性把整本 markdown 丢给 `otl.convert`**。内容大（>~60KB）时 convert 会把后半段降级成一整块纯文本（标题全丢）。**逐篇 convert，再把 blocks 数组拼接**，最后一次 `otl.block_update`。1179 块 / 420KB 参数实测可通过。
2. **标题层级**：如果要「一级 = 主题、二级 = 篇、三级起 = 篇内小节」，那 markdown 里主题用 `#`、文章标题用 `##`、文章内原 `##` 降为 `###`（原 `###` → `####`）。
3. **降级时必须跳过代码块**：逐行状态机跟踪 ``` 围栏，代码块内的 `# 注释` 不是标题，否则会被误改。
4. 文档标题交给 `blockId=doc` 的第一块 `title`，正文里不要再重复写文档名 H1。

清理旧的多文件副本：MCP **没有文件删除接口**（只有 `list_deleted_files` / `restore_deleted_file`）。能做的：`create_folder` 建归档子目录 → `move_file` 移入。`move_file` 对文件夹报 `400100 不支持的文件类型`，只能移文件。`rename_file` 的字段名是 `dst_name`（不是 `name`）。

## 高频工具速查（638 个中的常用组）

| 目的 | 工具 |
| --- | --- |
| 新建并写正文 | `create_file_with_content`（`.otl`/`.docx` 用 `content`；`.xlsx` 用 `sheets`） |
| 列目录 | `list_files`（**必填 `parent_id`**；根目录用 `list_my_files`，别传 `"0"`） |
| 新建空白文档/文件夹 | `create_empty_file` / `create_folder` |
| 云盘搜索 | `search_files`（`keyword`、`type`） |
| 读文档/下载 | `drive.read_and_download` 组、`drive.search` |
| 改正文（按块） | `otl.block_insert` / `otl.block_update` / `otl.block_query` |
| 表格批量写 | `sheet.data` 组（`sheet.data.*`） |
| 多维表格 | `dbsheet.*`（先 `get_schema` 再 `create_records`） |
| 权限/分享 | `cancel_share`、`cancel_collaborator_permissions`、`drive.share` |
| 导出 | `wps.export`（转 pdf/docx）、`pdf.convert` |
| 中文命名坑 | 文件名与目录名可中文；`check_file_name` 先查重名 |

## 可选：把 WPS 工具挂进 Hermes 原生工具列表

默认不挂——638 个工具会让工具注册表变重。要挂的话在 Hermes 的配置文件（`config.yaml`）里的 `skills` / `mcp_servers` 里配置。

```yaml
mcp_servers:
  wps_kdocs:
    enabled: true
    url: https://mcp-center.wps.cn/skill_hub/mcp
    headers:
      X-Request-Source: workbuddy
      X-Skill-Version: "1.6.14"
      X-Client-Id: "<16位hex>"
      Authorization: "Bearer ${WPS_KDOCS_TOKEN}"
```

`${WPS_KDOCS_TOKEN}` 需在运行环境中设置（通过 `wps_mcp.py whoami` 验证），未设置会 fail-closed 报 `missing_credentials`。

## 已实测（2026-11-15）

- `initialize` 未登录也成功，返回 `mcp-session-id`
- `tools/list` 未登录可读，共 **638** 个工具（`aippt.*`、`dbsheet.*`、`auto_sheet.*`、`create_file_with_content`、`search_files`、`drive.*`、`wps.*`、`otl.*`、`sheet.*`、`pdf.*`）
- 未登录时响应头带 `x-kso-auth-status: notLogin`、`x-kso-auth-raw-error: userNotLogin`；登录后该头变 `login`
  → 这就是判断 token 是否有效的可靠信号

## 坑

1. **企业账号 403**：WPS 企业/团队账号不能授权。必须个人账号。企业场景改用 WPS365 CLI。
2. **不要用 mcporter**：WorkBuddy 走 mcporter，本技能自写 HTTP 客户端，少一层依赖。
3. **SSE 响应**：MCP 可能回 `text/event-stream`，取最后一行 `data:` 解析；脚本已处理。
4. **`mcp-session-id` 必须回传**：后续 `tools/list`/`tools/call` 不带这个头会 400。
5. **参数别硬猜**：先 `schema`。WPS 的多维表格工具要求先 `get_schema` 拿 field id。
6. **token 只放 `.env`**，别写进 config.yaml 明文，也别贴聊天里。
7. **不覆盖用户已有内容前先读**：`otl.block_query` / `drive.read_and_download` 拿到现状再改。
8. **授权是唯一人工阻塞点，别绕它**：token 拿不到就别去黑 WorkBuddy 的 mcporter 配置或翻它的登录态文件——那边也是同一套 exchange 接口，没有可用凭证。直接把 auth 链接给用户，一次性完成。

## 发布与分享（让所有人搜得到）【2026-11-20 新增】

本技能是 Hermes 的 **skill**（含 SKILL.md + scripts/ + references/），不是独立「连接器插件」；真实能力是 WPS SkillHub MCP 的 **638 个工具**，需挂进 `mcp_servers` 才出现在工具里。

### 能让所有用户搜到，必须上 skills 仓库（不是只留在本机）
1. 本机先注册住：`config.yaml` 加 `skills.external_dirs` + `mcp_servers.wps_kdocs`（见「可选：把 WPS 工具挂进 Hermes 原生工具列表」）
2. 推到远端仓库：

```bash
cd <技能目录>
git init -b main
git add -A
git commit -m "wps-cloud-docs skill (芦名竹)"
git remote add origin git@github.com:lumz/wps-connector.git   # 或 https 链
git push -u origin main
```

3. 发布：

```bash
hermes skills publish <技能目录> \
    --to github --repo lumz/wps-connector
```

或手工发 skills.sh/clawhut。别人装后，就可搜到 `wps-cloud-docs`。

### 发布前必须知道
- **fine-grained PAT（`github_pat_...`）不能用作 Git 推送**，会报 `Password authentication is not supported for Git operations`。推需 classic PAT（`ghp_...`，含 `repo` 权限）或 SSH 密钥。
- 仓库名按用户名定：`lumz/wps-connector`（英文名 lumz）。
- 发布前清干净：SKILL.md 内不出现任意环境下的 token 文件路径、真实 token、个人内部路径等。
- 自动化发布有 `mcp-server full` 权限需要：用 classic PAT 需含 `repo` 授权。

## 回答风格（始终如此）
- **先结论**：一句话说清“是什么、怎么做、下一步”。
- **不解释废话**：用户要答案，不要复述流程。
- **不口头科普**：关键事实只给结论（如「这是 skill，不是连接器」）。
- 报错/进展也短句列表，绝不写大段背景。

## 认证（唯一需要人工的一步）
