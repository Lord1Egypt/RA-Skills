---
name: zenvfx-cli
description: Use this skill when the user needs to create AI videos, manage canvases, nodes, files, or interact with the ZenVFX platform via CLI. Trigger keywords include "画布", "视频生成", "zenvfx", "canvas", "node", "AI视频", "文生视频".
metadata: {"openclaw": {"emoji": "🎬", "os": ["darwin", "linux"], "requires": {"bins": ["zenvfx"], "env": ["ZENVFX_MCP_TOKEN"]}, "primaryEnv": "ZENVFX_MCP_TOKEN", "install": [{"id": "npm", "kind": "command", "command": "npm install -g @tencent/zenvfx-cli --registry https://mirrors.tencent.com/npm/", "bins": ["zenvfx"], "label": "Install ZenVFX CLI (npm)"}]}}
---

# ZenVFX CLI Skill

## 概述

ZenVFX CLI 是 AI 视频创作平台的命令行工具，通过画布（Canvas）中的节点（Node）+ 连线（Edge）构建 AI 生成任务。

- **CLI 入口**：`zenvfx <command>`
- **输出协议**：stdout 纯 JSON（`{"ok":true,"data":{...}}` / `{"ok":false,"error":{...}}`），解析时用 `2>/dev/null` 过滤 stderr
- **优先级**：系统中若同时存在 `zenvfx-mcp`，**一律优先使用 `zenvfx` CLI**，不要混用两者操作同一画布

**架构原则（v3）**：
- **万物皆批处理**：所有编辑操作均接收 JSON 数组 / 逗号分隔 ID 列表，无论操作 1 个还是 N 个对象，底层统一为批量调用。
- **运行节点支持同步/异步双模式**：`canvas:run` 默认异步，加 `--wait` 进入同步模式（daemon 内部轮询直到所有节点 completed/failed 才返回）。
- **Partial Success**：批量操作逐项执行，某项失败不影响其余，返回 `results` 数组逐项标注状态。

---

## 版本与升级

- **当前最新版本**：`0.9.1`
- **包名**：`@tencent/zenvfx-cli`
- **Registry**：`https://mirrors.tencent.com/npm/`（腾讯内网 npm 镜像）

### 安装 / 升级到最新

```bash
# 首次安装 或 升级到 registry 上的最新版（@latest 等价于不写 tag）
npm install -g @tencent/zenvfx-cli@latest --registry https://mirrors.tencent.com/npm/

# 升级到指定版本
npm install -g @tencent/zenvfx-cli@0.9.1 --registry https://mirrors.tencent.com/npm/
```

> 注意：必须带 `--registry`，公网 `registry.npmjs.org` 上没有这个包。

### 如何确认已经是最新版

按下面三步对比，三个版本号一致即说明已装到最新：

```bash
# 1. 本地已安装版本
zenvfx --version
# 输出形如：@tencent/zenvfx-cli/0.9.1 linux-x64 node-v20.x

# 2. registry 上当前 latest 版本
npm view @tencent/zenvfx-cli version --registry=https://mirrors.tencent.com/npm/
# 输出形如：0.9.1

# 3. 全局安装包元信息（确认安装路径与版本，排除多版本污染）
npm ls -g @tencent/zenvfx-cli --registry=https://mirrors.tencent.com/npm/
```

若 `zenvfx --version` 比 `npm view` 拿到的版本旧，重新执行上面的 `npm install -g ...@latest` 即可；若 `zenvfx` 命令找不到，检查 `npm config get prefix` 下的 `bin` 是否在 `PATH` 里。

升级后建议再跑一次 `zenvfx auth:verify <token>`，确认本地配置仍然可用。

---

## 认证与安装

```bash
# 安装（详见上一节"版本与升级"）
npm install -g @tencent/zenvfx-cli@latest --registry https://mirrors.tencent.com/npm/

# 认证（自动保存 mcpToken/defaultProject/defaultWorkspace 等配置）
zenvfx auth:login <token>          # 可选 --host <host-url>

# 仅校验 token（不切换默认项目/workspace）
zenvfx auth:verify <token>
```

`auth:login` 返回 `saved` 字段标识各配置是否已自动设置。若 `saved.defaultProject` 或 `saved.defaultWorkspace` 为 `false`，需手动补全：

```bash
zenvfx project:list 2>/dev/null              # 查看可用项目
zenvfx project:switch <project-id>           # 一键切换项目（自动更新 workspace）
```

`project:switch` 自动解析 workspace 的规则（仅依赖 `userId`，不依赖 `username`，因为 username 是用户可自定义的别名）：
1. **精确匹配**：`/{projectId}/用户空间/` 下目录名以 `_{userId}` 结尾
2. **模糊匹配**：目录名包含 `userId`
3. 均未命中则清空 `defaultWorkspace`，需手动设置

也可手动设置：
```bash
zenvfx config:set defaultProject <project-id>
zenvfx config:set defaultWorkspace "/<project-id>/用户空间/xxx"
```

也可通过环境变量：`ZENVFX_MCP_TOKEN`、`ZENVFX_PROJECT`

---

## 命令速查

### 配置

| 命令 | 用途 |
|------|------|
| `auth:login <token>` | 一键认证，可选 `--host` |
| `auth:verify <token>` | 仅校验 token 合法性并写入 `mcpToken`，不切换项目/workspace |
| `config:set <key> <value>` | 手动设置（key：`host`/`wsHost`/`mcpToken`/`defaultProject`/`defaultUsername`/`defaultUserId`/`defaultWorkspace`） |
| `config:get <key>` / `config:list` | 读取配置 |
| `project:list` | 列出项目 |
| `project:switch <projectId>` | 切换项目（自动更新 defaultProject + defaultWorkspace，workspace 匹配仅依赖 `userId`，不依赖 `username`），可选 `--no-workspace` |

### 文件系统（路径格式：`/<projectId>/目录/文件名`）

| 命令 | 用途 |
|------|------|
| `file:stat --path <p>` | 文件/目录详情 |
| `file:readdir --path <p>` | 目录内容（不递归） |
| `file:mkdir --path <p>` | 创建目录（默认递归） |
| `file:rm --path <p>` | 删除文件/目录 |
| `file:tree --path <p>` | 目录树，可选 `--max-depth` |
| `file:path-to-id --path <p>` | 路径转内部 ID |
| `file:id-to-path --id <id>` | 内部 ID 转路径 |
| `file:upload --local-file <本地路径> --project-id <id> [--file-path <ZenFS路径>] [--title <名称>]` | 上传本地文件到 COS 并注册素材；`--file-path` 可省略（仅上传不写 ZenFS） |

### 画布管理

标注 `[S]` 的命令**必须携带 `--canvas <path>` 参数**。系统会根据 `--canvas` 路径**自动执行 `canvas:open`**（如果尚未打开），无需手动调用。

> ⚠️ **`--data` / `--value-json` 的 JSON 值直接裸写，不加单引号或双引号包裹**。
> 命令解析器使用空格切分（`split(/\s+/)`），不支持引号转义。
> - ✅ `--data [{"type":"image_generator"}]`
> - ❌ `--data '[{"type":"image_generator"}]'`（单引号成为 JSON 值的一部分 → `JSON 解析失败`）

| 命令 | 用途 |
|------|------|
| `canvas:create --name <名称>` | 创建画布，可选 `--path`（默认 `defaultWorkspace`） |
| `canvas:list` | 列出画布（不递归），可选 `--list-path` |
| `canvas:open --canvas <path>` `[S]` | 显式打开画布（一般无需手动调用，其他 `[S]` 命令会自动触发） |
| `canvas:info --canvas <path>` `[S]` | 查看画布信息 |
| `canvas:save --canvas <path>` `[S]` | 保存画布（编辑命令已自动保存，通常不需要） |
| `canvas:run --ids <id1,id2,...> --canvas <path>` `[S]` | 批量运行节点；默认异步立即返回 `query_hint`，加 `--wait` 进入同步模式 |

#### canvas:run 同步/异步模式

| 模式 | 触发 | 返回时机 | 适用场景 |
|------|------|----------|----------|
| **异步**（默认） | `canvas:run --ids ...` | 立即返回，含 `submitted`/`results[].taskId`/`query_hint` | 长链路、并发多节点；调用方按 `query_hint.command` 自行轮询 |
| **同步** | `canvas:run --ids ... --wait` | 在 daemon 内部轮询直到全部 `completed`/`failed` 才返回最终结果（含 `outputs[].url`） | 单节点或短链路调试；脚本希望一次拿到结果 |

- `--timeout <秒>` 仅在 `--wait` 时生效，默认 **1800（30 分钟）**。
- 异步 IPC 超时按 `节点数 × 15s + 60s` 自动放宽，最低 120s。
- 同步模式返回结构：
  ```json
  {
    "submitted": true,
    "mode": "sync",
    "timedOut": false,
    "elapsed": 62025,
    "results": [
      { "taskId": "...", "status": "completed", "nodes": [{ "nodeId": "...", "status": "completed", "outputs": [...], "textOutputs": [] }] }
    ]
  }
  ```

```bash
# 同步等待两个图片节点跑完
zenvfx canvas:run --ids image_generator-aaa,image_generator-bbb --wait --timeout 600 --canvas "$CANVAS_PATH"

# 异步触发，自己轮询
RUN=$(zenvfx canvas:run --ids node1,node2 --canvas "$CANVAS_PATH" 2>/dev/null)
# 取 query_hint.command 后定期 zenvfx task:status ...
```

### 节点操作 `[S]`

编辑类命令执行后**自动保存**画布。

> ⚠️ **`--canvas` 是必填参数**：所有标注 `[S]` 的命令都**必须**携带 `--canvas <path>` 参数指定画布路径（或通过环境变量 `ZENVFX_CANVAS` 提供）。

| 命令 | 用途 |
|------|------|
| `canvas:node:list --canvas <path>` | 列出所有节点 |
| `canvas:node:info --ids <id1,id2> --canvas <path>` | 批量查看节点详情（pins、options、taskId/taskStatus） |
| `canvas:node:add --data <JSON数组> --canvas <path>` | 批量添加节点 |
| `canvas:node:remove --ids <id1,id2> --canvas <path>` | 批量删除节点 |
| `canvas:node:set --data <JSON数组> --canvas <path>` | 批量设置节点参数 |
| `canvas:node:set --id <id> --option <name> --value <val> --canvas <path>` | 快捷模式：单节点单参数设置 |
| `canvas:node:move --data <JSON数组> --canvas <path>` | 批量移动节点位置 |
| `canvas:node:move --id <id> --position <x,y> --canvas <path>` | 快捷模式：单节点移动 |
| `canvas:node:prompt --id <id> --prompt <text> --canvas <path>` | 解析 prompt 中的 @占位符（如 `@首帧图1`），可选 `--model` |
| `node:model <nodeTypes>` | 查询节点支持的模型与参数枚举（支持逗号分隔多个类型） |
| `node:list` | 列出所有可用节点类型定义（本地，不需网络） |
| `node:defs` | 一站式返回所有节点完整定义（本地 schema + 后端模型/参数），AI Agent 加载节点知识首选 |

#### 参数校验错误提示（节点命令通用）

| 场景 | 错误信息 | 错误码 |
|------|----------|--------|
| `--data` JSON 解析失败 | `--data JSON 解析失败，请检查格式: <原始输入>` | `INVALID_JSON` |
| `--data` 不是非空数组 | `--data 必须是非空 JSON 数组` | `INVALID_JSON` |
| `node:add` 缺少 type | `参数校验失败: data[N].type 是必填项` | `MISSING_VALUE` |
| `node:set` 批量模式缺少 id | `参数校验失败: data[N].id 是必填项` | `MISSING_VALUE` |
| `node:set` 批量模式 options 不是对象 | `参数校验失败: data[N].options 必须是对象` | `MISSING_VALUE` |
| `node:set` 快捷模式缺少 --id | `参数校验失败: 必须提供 --data（批量模式）或 --id + --option + --value（快捷模式）` | `MISSING_VALUE` |
| `node:set` 快捷模式缺少 --option | `参数校验失败: 快捷模式需要 --option 指定选项名称` | `MISSING_VALUE` |
| `node:set` 快捷模式缺少值 | `参数校验失败: 快捷模式必须提供 --value 或 --value-json` | `MISSING_VALUE` |
| `--value-json` JSON 解析失败 | `--value-json JSON 解析失败，请检查格式: <原始输入>` | `INVALID_JSON` |
| `node:info/remove` --ids 为空 | `参数校验失败: --ids 至少需要包含一个节点 ID` | `MISSING_VALUE` |
| `node:move` 批量缺少 nodeId/position | `参数校验失败: data[N].nodeId 是必填项` / `data[N].position 是必填项` | `MISSING_VALUE` |
| `node:move` 快捷模式缺少 --id 或 --position | `参数校验失败: 快捷模式需要 --position 指定目标位置` | `MISSING_VALUE` |

#### canvas:node:add --data 格式

```json
[
  {
    "type": "string",     // [必填] 节点类型，如 "image_generator", "normal_video_generator"
    "name": "string",     // [选填] 节点名称
    "position": "string", // [选填] 坐标位置，如 "100,200"，默认 "0,0"
    "options": {}         // [选填] 节点配置参数（如 prompt, model, clarity, ratio, duration 等），
                          //        创建后立即设置，无需再单独调用 canvas:node:set
  }
]
```

**示例**：
```bash
# 基础：只创建节点
zenvfx canvas:node:add --data [{"type":"normal_video_generator","position":"0,0"},{"type":"image_input","position":"400,0","name":"首帧图"}] --canvas "$CANVAS_PATH"

# 带 options：创建并设置参数（省去 canvas:node:set）
zenvfx canvas:node:add --data [{"type":"normal_video_generator","name":"文生视频","position":"0,0","options":{"prompt":"傍晚海边小孩嬉戏","model":"kling","clarity":"RESOLUTION_720P","ratio":"16:9","duration":5}}] --canvas "$CANVAS_PATH"
```

#### canvas:node:set 两种模式（互斥）

**模式 1 — 批量模式 `--data`**（多节点多参数）：
```json
[
  {
    "id": "string",       // [必填] 节点 ID
    "options": {           // [必填] 要设置的参数对象
      "prompt": "赛博朋克",
      "model": "kling-video-o1"
    }
  }
]
```
```bash
zenvfx canvas:node:set --data [{"id":"node1","options":{"prompt":"赛博朋克","model":"kling-video-o1"}}] --canvas "$CANVAS_PATH"
```

**模式 2 — 快捷模式**（单节点单参数，LLM 友好，无需构造 JSON）：
```bash
zenvfx canvas:node:set --id node-abc --option prompt --value "一只银渐层胖猫咪" --canvas "$CANVAS_PATH"
# JSON 值使用 --value-json
zenvfx canvas:node:set --id node-abc --option config --value-json {"width":1024} --canvas "$CANVAS_PATH"
```

> ⚠️ `--data` 与 `--id + --option + --value` 互斥。传了 `--data` 则忽略快捷模式参数。

#### canvas:node:move 两种模式（互斥）

```bash
# 批量
zenvfx canvas:node:move --data [{"nodeId":"n1","position":"100,200"},{"nodeId":"n2","position":{"x":300,"y":400}}] --canvas "$CANVAS_PATH"

# 快捷
zenvfx canvas:node:move --id node-abc --position "100,200" --canvas "$CANVAS_PATH"
zenvfx canvas:node:move --id node-abc --position {"x":100,"y":200} --canvas "$CANVAS_PATH"
```

> **节点位置**：添加多个节点时用 `position` 指定坐标，避免叠加。建议水平间隔 400px：`"0,0"`、`"400,0"`、`"800,0"`。

### 打组操作 `[S]`

> ⚠️ 同样**必须**携带 `--canvas <path>` 参数。所有写操作执行后**自动保存**。
>
> **打组必须一次做到完整收尾**：当用户要求"打组/分组/整理成组"时，优先只调用 `canvas:node:group`。该命令内部会自动完成：创建组 → 对新组/受影响父组执行组排序 → 检查顶层重叠 → 必要时整体平移避免重叠。不要在打组后停在"已创建组"，需根据返回的 `sortedGroups` / `overlapCheck` 确认布局已收尾；只有用户明确要求重新排序某个已有组时，才额外调用 `canvas:node:group:sort`。

| 命令 | 用途 |
|------|------|
| `canvas:node:group --node-ids <id1,id2,...> [--name <name>] --canvas <path>` | 将一批节点打包为新组（自动剥离原父组成员、自动派生组的边/实体引用，并自动排序/检查重叠/必要时避让） |
| `canvas:node:ungroup --group-id <id> --canvas <path>` | 解散组，成员上浮到父级 |
| `canvas:node:group:info --group-id <id> --canvas <path>` | 查询组信息（id/name/members/color/bounds，**只读**） |
| `canvas:node:group:members --group-id <id> --node-ids <id1,id2,...> --canvas <path>` | 全量替换组成员，自动重派生 edges/entities |
| `canvas:node:group:color --group-id <id> --color <颜色> --canvas <path>` | 修改组颜色标签，可选值：`gray` / `red` / `orange` / `yellow` / `green` / `cyan` / `blue` / `purple` / `none`（清除颜色） |
| `canvas:node:group:sort --group-id <id> --canvas <path>` | 对组内节点执行依赖流自动排序布局（基于内部边自动调整位置） |
| `canvas:node:group:execute --group-id <id> --canvas <path>` | 按依赖顺序执行组内所有可执行节点（异步触发，进度通过 `task:status` 查询） |
| `canvas:node:group:cancel --group-id <id> --canvas <path>` | 取消组的按序执行（停止组内所有进行中或 pending 的子节点） |

**示例**：

```bash
# 1. 把 3 个节点打成一个组并命名（自动完成组排序 + 顶层重叠检查/避让）
zenvfx canvas:node:group --node-ids n1,n2,n3 --name "场景A" --canvas "$CANVAS_PATH"
# → { groupId: "group_xxx", status: "ok", sortedGroups: [...], overlapCheck: { checked, movedGroups, overlapsBefore, overlapsAfter } }

# 2. 查询组详情
zenvfx canvas:node:group:info --group-id group_xxx --canvas "$CANVAS_PATH"

# 3. 改颜色 / 清除颜色
zenvfx canvas:node:group:color --group-id group_xxx --color blue --canvas "$CANVAS_PATH"
zenvfx canvas:node:group:color --group-id group_xxx --color none --canvas "$CANVAS_PATH"

# 4. 改成员（全量替换）
zenvfx canvas:node:group:members --group-id group_xxx --node-ids n1,n4 --canvas "$CANVAS_PATH"

# 5. 组内自动排序
zenvfx canvas:node:group:sort --group-id group_xxx --canvas "$CANVAS_PATH"

# 6. 按依赖顺序执行组内节点（异步）
zenvfx canvas:node:group:execute --group-id group_xxx --canvas "$CANVAS_PATH"
# 查进度：zenvfx task:status --ids <taskIds> --canvas-id <canvasId>

# 7. 取消执行
zenvfx canvas:node:group:cancel --group-id group_xxx --canvas "$CANVAS_PATH"

# 8. 解散
zenvfx canvas:node:ungroup --group-id group_xxx --canvas "$CANVAS_PATH"
```

**参数校验错误提示（打组命令）**：

| 场景 | 错误信息 | 错误码 |
|------|----------|--------|
| `--node-ids` 为空 | `参数校验失败: --node-ids 至少需要包含一个节点 ID` | `MISSING_VALUE` |
| 任一 nodeId 不存在 | `Node not found: <id>` | `NODE_NOT_FOUND` |
| `--group-id` 对应节点不是 group 类型 | `Node <id> is not a group` | `NODE_VALIDATION_FAILED` |
| `groupNodes` 归一化后成员为空 | `No valid nodes to group` | `NODE_VALIDATION_FAILED` |
| `--color` 取值非法 | 由 oclif options 拒绝并列出可选值 | — |

> 💡 **打组语义提示**：
> - `canvas:node:group` 的 `--node-ids` **可以混合普通节点和已有的组**。当传入的节点是另一个组的成员时，工具会自动从原父组中剥离，避免重复归属。
> - `canvas:node:group` 默认会自动执行布局收尾：排序新组/受影响父组，并检查顶层重叠；若 `overlapCheck.overlapsAfter > 0`，需要继续使用 `canvas:node:move` 或再次组织布局，不能直接宣称布局完美。
> - `canvas:node:group:members` 是**全量替换**而非增量；想加成员请先 `info` 查出当前 members，合并后再传入。
> - `canvas:node:group:sort` 仅对组的**直接成员**做布局，不会递归子组内部；普通打组场景无需再额外调用，因为 `canvas:node:group` 已自动收尾。

### 连线操作 `[S]`

> ⚠️ 同样**必须**携带 `--canvas <path>` 参数。

| 命令 | 用途 |
|------|------|
| `canvas:edge:list --canvas <path>` | 列出所有连线 |
| `canvas:edge:add --data <JSON数组> --canvas <path>` | 批量连接节点 |
| `canvas:edge:remove --ids <id1,id2> --canvas <path>` | 批量删除连线 |

#### canvas:edge:add --data 格式

```json
[
  {
    "source": "string",        // [必填] 源节点 ID
    "sourceHandle": "string",  // [必填] 源节点输出 handle（pinName）
    "target": "string",        // [必填] 目标节点 ID
    "targetHandle": "string"   // [必填] 目标节点输入 handle（pinName）
  }
]
```

**示例**：
```bash
zenvfx canvas:edge:add --data [{"source":"n1","sourceHandle":"output","target":"n2","targetHandle":"ref_images"}] --canvas "$CANVAS_PATH"
```

**参数校验错误提示（连线命令）**：

| 场景 | 错误信息 | 错误码 |
|------|----------|--------|
| `edge:add` JSON 解析失败 | `--data JSON 解析失败，请检查格式: <原始输入>` | `INVALID_JSON` |
| `edge:add` 不是非空数组 | `--data 必须是非空 JSON 数组` | `INVALID_JSON` |
| `edge:add` 缺少必填字段 | `参数校验失败: data[N].source 是必填项` 等 | `MISSING_VALUE` |
| `edge:remove` --ids 为空 | `参数校验失败: --ids 至少需要包含一个边 ID` | `MISSING_VALUE` |

### 任务查询（不需 Session）

| 命令 | 用途 |
|------|------|
| `task:status --ids <taskId1,taskId2> --canvas-id <id>` | 批量查询任务状态（`--ids` 和 `--canvas-id` 均为必填） |

**查询命令参数校验**：

| 场景 | 错误信息 | 错误码 |
|------|----------|--------|
| `node:model` 未提供 nodeType | `参数校验失败: nodeTypes 是必填项，请提供至少一个节点类型` | `MISSING_VALUE` |
| `node:model` 未知类型 | `未知的节点类型: <xxx>`（返回 validTypes 列表，不中断） | — |
| `task:status` --ids 为空 | `参数校验失败: --ids 至少需要包含一个任务 ID` | `MISSING_VALUE` |
| `task:status` project 未配置 | `参数校验失败: project 未配置，请通过 auth:login 或 config:set defaultProject 设置` | `MISSING_CONFIG` |
| `canvas:run` --ids 为空 | `参数校验失败: --ids 至少需要包含一个节点 ID` | `MISSING_VALUE` |

### 守护进程

| 命令 | 用途 |
|------|------|
| `daemon:ping` / `daemon:status` / `daemon:stop` | 检测/查看/停止 daemon |

---

## 重要规则

### 1. 连线 handle 必须使用 pinName

`sourceHandle` 和 `targetHandle` **必须用节点定义中的 pinName**，不是后端 API 的 field_path。用错会导致连线保存成功但前端不显示。

通过 `node:list` 或 `node:defs` 查询正确的 pinName。常用速查：

| 节点类型 | 输入 pinName | 输出 pinName |
|----------|-------------|-------------|
| `image_generator` | `prompt`, `referenceImage` | `outputImage` |
| `normal_video_generator` | `referenceImage`, `prompt` | `outputVideo` |
| `composite_video_generator` | `inputVideo`, `inputImage`, `prompt` | `outputVideo` |
| `first_to_last_video_generator` | `firstReferenceImage`, `lastReferenceImage`, `prompt` | `outputVideo` |
| `comprehensive_reference_generator` | `inputVideo`, `inputImage`, `inputAudio`, `prompt` | `outputVideo` |

### 2. 编辑命令自动保存 — 不要重复 save

`canvas:node:add`、`canvas:node:remove`、`canvas:node:set`、`canvas:node:move`、`canvas:edge:add`、`canvas:edge:remove`、`canvas:node:group*` 系列执行成功后**自动保存画布**，无需额外调用 `canvas:save`。

> 注：旧版的 `canvas:node:props` 已下线，统一通过 `canvas:node:set` 设置参数。

### 3. 画布路径

`canvas:create` 返回的 `canvasPath` 不含 `.canvas` 后缀，canvas 类命令带不带后缀均可。`file:stat` 等文件命令需要完整文件名（带 `.canvas`）。

### 4. canvas:open 一般无需手动调用

所有 `[S]` 命令在执行时会**自动按 `--canvas` 路径打开/复用 Session**。只有在你需要显式预热 daemon、提前感知错误时才调用 `canvas:open`。

### 5. 批量传参约定（多 ID / 多对象）

CLI 对"多个对象"的批量传参分两种风格，**不混用**：

| 风格 | 适用命令 | 用法 |
|------|----------|------|
| `--ids` 逗号分隔 | `canvas:run` / `canvas:node:remove` / `canvas:node:info` / `task:status` 等"只需要 ID"的命令 | `--ids "n1,n2,n3"`，逗号两侧空格会被 trim，空段会被过滤 |
| `--data` JSON 数组 | `canvas:node:add` / `canvas:node:set` / `canvas:edge:add` / `canvas:edge:remove` 等"需要传字段"的命令 | `--data '[{...},{...}]'`，每项校验必填字段，partial success |

> 升级 CLI 后建议 `daemon:stop` 一次，避免老 daemon 仍按旧协议解析参数（详见"已知问题 #1"）。

---

## 核心流程：生成 AI 视频

```
0. auth:login <token>                                      （一次性）
1. canvas:create --name "xxx"                              （自动使用 defaultWorkspace）
2. canvas:node:add --data [{"type":"normal_video_generator","position":"0,0","options":{"prompt":"...","model":"kling","clarity":"RESOLUTION_720P"}}] --canvas "${CANVAS_PATH}"
3. 选 A 或 B 运行：
   A. 同步：canvas:run --ids $NODE_ID --wait --timeout 600 --canvas "${CANVAS_PATH}"
      → 阻塞返回最终 outputs，最简单
   B. 异步：canvas:run --ids $NODE_ID --canvas "${CANVAS_PATH}"
      → 立即返回 query_hint，再用 task:status 轮询
```

### 同步 vs 异步选择

| 场景 | 推荐 |
|------|------|
| 单节点 / 短链路 / 想"一行命令拿结果" | `canvas:run --wait --timeout 600` |
| 多节点并发触发，调用方自己控制轮询节奏 | 默认异步 + `task:status` |
| LLM Agent 想避免长时间阻塞主进程 | 默认异步，把 `query_hint` 保存到任务上下文 |
| 在 shell 脚本里串联多个步骤 | `--wait` 更直观；超时按节点类型设置（图片 300s、视频 1800s） |

### 异步轮询最佳实践

异步模式 `canvas:run` 立即返回，结果中包含 `query_hint`：

```json
{
  "submitted": true,
  "mode": "async",
  "results": [
    { "nodeId": "node1", "taskId": "abc1234", "status": "pending" }
  ],
  "query_hint": {
    "command": "task:status --ids abc1234 --canvas-id xxx",
    "instruction": "请使用上述命令批量查询任务结果，建议间隔 15s"
  }
}
```

**轮询步骤**：

1. `canvas:run --ids <nodeId1,nodeId2>` — 立即返回 `results` 和 `query_hint`
2. 直接执行 `query_hint.command`（已自动拼接所有 taskId）
3. 每 **15 秒**轮询一次 `task:status --ids <taskIds> --canvas-id <canvasId>`
4. 当所有任务 `status` 为 `completed` / `failed` 时停止，最长 **30 分钟**

> `outputs` 中有效 URL 在 `url` 字段（带 COS 签名），`download_url` 可能为空。

### 完整示例（同步等待版）

```bash
# 0. 认证
zenvfx auth:login <your-mcp-token>

# 1. 创建画布
CREATE_RESULT=$(zenvfx canvas:create --name "测试画布" 2>/dev/null)
CANVAS_PATH=$(echo $CREATE_RESULT | grep -o '"canvasPath":"[^"]*"' | sed 's/"canvasPath":"//;s/"$//')

# 2. 批量添加节点（canvas:open 自动执行，无需手动调用）
RESULT=$(zenvfx canvas:node:add --data [{"type":"normal_video_generator","name":"文生视频","position":"0,0","options":{"prompt":"傍晚的海边，小孩子嬉戏玩水","model":"kling","clarity":"RESOLUTION_720P","ratio":"16:9","duration":5}}] --canvas "${CANVAS_PATH}" 2>/dev/null)
NODE_ID=$(echo $RESULT | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"$//')

# 3. 同步运行（阻塞等待最终结果）
zenvfx canvas:run --ids $NODE_ID --wait --timeout 1200 --canvas "${CANVAS_PATH}"
```

### 完整示例（异步轮询版）

```bash
# 1~2 同上

# 3. 异步运行
RUN_RESULT=$(zenvfx canvas:run --ids $NODE_ID --canvas "${CANVAS_PATH}" 2>/dev/null)
# 从 query_hint 获取轮询命令
QUERY_CMD=$(echo $RUN_RESULT | grep -o '"command":"[^"]*"' | head -1 | sed 's/"command":"//;s/"$//')

# 4. 轮询任务状态（每 15s 一次）
while true; do
  STATUS=$(zenvfx $QUERY_CMD 2>/dev/null)
  if echo "$STATUS" | grep -qE '"status":"(completed|failed)"'; then
    echo "$STATUS"
    break
  fi
  sleep 15
done
```

---

## 节点参数

> **重要**：model/clarity/ratio/duration 的值**必须通过 `node:model <nodeType>` 或 `node:defs` 动态查询**，不要硬编码。

> **视频节点建议**：模型 `kling` + 分辨率 `RESOLUTION_720P`（比 1080P 快 2-3 倍）。

> **node:model 支持批量查询**：`node:model normal_video_generator,image_generator` 一次返回多个类型的模型列表。

> **node:defs 一站式知识**：`node:defs` 同时返回本地 schema（pin/option）+ 后端模型枚举/参数，AI Agent 启动期一次拉取即可，避免后续多次往返。

通过 `--data` 批量模式或 `--option` + `--value` 快捷模式传参：

| 参数 | 类型 | 说明 |
|------|------|------|
| `prompt` | string | 提示词 |
| `model` | string | 模型 ID（**必须通过 `node:model <type>` 查询**） |
| `clarity` | string | 分辨率枚举 |
| `ratio` | string | 画幅比例 |
| `duration` | number | 时长秒数（仅视频节点） |

**节点类型**（`type` 必须是下列英文 snake_case 枚举之一，写错会报 `NODE_TYPE_INVALID`）：

| `type` | 说明 |
|--------|------|
| `text_input` / `image_input` / `video_input` / `audio_input` | 输入节点（⚠️ **文本节点是 `text_input`，不是 `text`**） |
| `image_generator` | 文/图生图 |
| `normal_video_generator` | 文/图生视频 |
| `first_to_last_video_generator` | 首尾帧视频 |
| `composite_video_generator` | 视频编辑 |
| `comprehensive_reference_generator` | 全能参考生视频 |
| `llm` | 大模型文本节点 |
| `group` | 组节点 |
| `video_process` | 视频处理（变速/帧率转换/冻帧延长/裁切） |
| `frame_extraction` | 视频截帧 |

> 中文（"提示词"、"文本"）是节点 `label`，不是 `type`，传给 `canvas:node:add` 的 `--data` 中会直接失败。

### Prompt 占位符

Prompt 中可以用 `@` 前缀引用**上游节点通过连线传入的输入资源**。占位符直接写在 `canvas:node:set` 的 prompt 值中即可，画布引擎运行时会自动解析。

**支持的占位符**（数字后缀可选，默认 1，如 `@提示词` 等价于 `@提示词1`）：

| 占位符 | 含义 | 上游节点类型 |
|--------|------|------------|
| `@提示词1`、`@提示词2`… | 引用上游 **文本节点** 的文本内容 | `text_input` / `llm` |
| `@参考图`、`@参考图1`… | 引用上游 **图片节点** 的图片 | `image_input` / `image_generator` |
| `@首帧图1`、`@首帧图2`… | 引用首帧参考图 | `image_input` / `image_generator` |
| `@尾帧图1`、`@尾帧图2`… | 引用尾帧参考图 | `image_input` / `image_generator` |
| `@参考视频`、`@参考视频1`… | 引用上游 **视频节点** 的视频 | `video_input` / 视频生成节点 |
| `@参考音频`、`@参考音频1`… | 引用上游 **音频节点** 的音频 | `audio_input` |

**`@提示词` 引用上游文本节点**（最常用）：

用 `text_input` 节点写好提示词文本，连线到生成节点的"提示词"输入口，然后在 prompt 中用 `@提示词1` 引用。画布引擎运行时会**直接替换为上游文本节点的文本内容**。

```bash
# text_input 节点（id=text-001）prompt 值为 "傍晚海边小孩嬉戏"
# 连线：text-001 → video-001 的"提示词1"输入口
zenvfx canvas:node:set --id video-001 --option prompt --value "帮我生成一段视频：@提示词1" --canvas "$CANVAS_PATH"
```

**图片/视频/音频占位符**：

同样直接写在 prompt 中，画布引擎运行时会根据模型自动转换为对应格式。

```bash
zenvfx canvas:node:set --id $VIDEO_NODE_ID --option prompt --value "小孩奔向海浪@首帧图1，夕阳洒在海面@尾帧图1" --canvas "$CANVAS_PATH"
```

> 想看模型最终拿到的 prompt 字面值？先用 `canvas:node:prompt --id <id> --prompt "<原文>" [--model <id>]` 预览解析结果。

---

## 批量返回格式说明

编辑类操作均返回 Partial Success 格式：

```json
{
  "results": [
    { "status": "ok", "id": "xxx", "type": "image_generator", "name": "生图节点", "position": { "x": 0, "y": 0 } },
    { "status": "error", "id": null, "type": "unknown_type", "error": "NODE_TYPE_INVALID" }
  ],
  "successCount": 1,
  "failCount": 1
}
```

- 批量操作中某项失败**不影响**其余项
- 每项通过 `status` 字段标注 `"ok"` / `"error"`
- 顶层返回 `successCount` / `failCount` 汇总

---

## 异常处理

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| `AUTH_REQUIRED` | Token 未配置 | `auth:login <token>` |
| `MCP_TOKEN_INVALID` | Token 无效/过期 | `auth:verify <token>` 或重新 `auth:login` |
| `CANVAS_NOT_FOUND` | 画布不存在 | 检查路径，`file:stat` 确认 |
| `CANVAS_SAVE_FAILED` | 保存失败（server overload） | 系统已内置重试 3 次（间隔 1s/2s/3s），仍失败则手动重试 |
| `NODE_NOT_FOUND` | 节点不存在 | `canvas:node:list` 确认 |
| `NODE_TYPE_INVALID` | 节点类型不合法 | 用 `text_input` / `image_input` / `video_input` / `audio_input` / `image_generator` / `normal_video_generator` / `first_to_last_video_generator` / `composite_video_generator` / `comprehensive_reference_generator` / `llm` / `group` / `video_process` / `frame_extraction`；中文标签不是 `type` |
| `INVALID_JSON` | `--data` / `--value-json` JSON 解析失败 | 检查引号、逗号、括号等 JSON 格式 |
| `MISSING_VALUE` | 必填字段缺失 | 查看报错信息中标注的缺失字段（如 `data[0].type 是必填项`） |
| `MISSING_CONFIG` | 配置缺失（project 等） | 通过 `auth:login` 或 `config:set defaultProject` 设置 |
| `OPTION_NOT_FOUND` | 无该选项 | `canvas:node:info --ids <id>` 查看可用选项 |
| `EDGE_HANDLE_INVALID` | 连线 handle 不合法 | `canvas:node:info --ids <id>` 查看 inputPins/outputPins |
| `DAEMON_TIMEOUT` | daemon 超时 | `daemon:stop` 后重试；若启动直接超时见下文"已知问题 #2 react 缺失" |
| `DAEMON_START_FAILED` | daemon 启动失败 | 检查端口占用，清理后重试 |
| `DAEMON_CONNECTION_FAILED` | daemon 连接失败 | `daemon:stop` 后重试 |
| `TASK_SUBMIT_FAILED` | 任务提交失败 | 检查节点参数，重跑 `node:model <类型>` 对齐参数 |
| `UPLOAD_TOKEN_FAILED` / `UPLOAD_FAILED` / `REGISTER_ASSET_FAILED` | `file:upload` 各阶段失败（已内置 3 次重试） | 查 `error.message` 与 details；多为网络/凭证问题，过段时间重试 |
| `NETWORK_ERROR` | 网络错误 | 检查网络连接，确认 host 配置 |

**daemon 异常强制清理**：
```bash
zenvfx daemon:stop
kill $(cat ~/.config/zenvfx/daemon.pid) 2>/dev/null
rm -f ~/.config/zenvfx/daemon.sock ~/.config/zenvfx/daemon.pid
```

**调试运行节点的请求体**（对照网页协议时常用）：

daemon 会把每次提交后端的 `submitTask` 请求体写到 `~/.config/zenvfx/daemon.log`。可用脚本快速取最近一次：

```bash
bash src/libs/zenvfx-cli/test/scenarios/dump-last-submit.sh           # 最近 1 次
bash src/libs/zenvfx-cli/test/scenarios/dump-last-submit.sh 3         # 最近 3 次
bash src/libs/zenvfx-cli/test/scenarios/dump-last-submit.sh 1 image_generator-xxx   # 按关键词过滤
```

---

## 已知问题与坑位（v0.9.1）

> 这里收录已经踩过的"行为不符合预期 / 必须绕过"的问题。修复后请同步移除对应条目。

### 1. CLI 升级后 `canvas:run --ids "a,b"` 报 `nodeId is required`（**版本错位，不是 bug**）

- **现象**：升级到 0.9.1 后，`zenvfx canvas:run --ids "node1,node2"` 报 `MISSING_VALUE: nodeId is required`。
- **根因**：CLI 二进制升级了，但**老版本 daemon 进程还在跑**——
  - 0.9.1 CLI 走新协议送 `nodeIds: ['node1','node2']`
  - 0.9.0 daemon 仍按旧协议解构单个 `nodeId`，自然为空
  - 报错文案是判断依据：0.9.1 应是 `nodeIds (string[]) is required`，旧文案是 `nodeId is required`
- **正解**：升级 CLI 后强制重启 daemon——
  ```bash
  zenvfx daemon:stop
  zenvfx daemon:status     # 会自动拉起新版本 daemon
  zenvfx canvas:run --ids "node1,node2" --canvas /proj/canvas   # 此时正常
  ```
- **建议**：每次 `npm install -g @tencent/zenvfx-cli@latest` 后顺手 `daemon:stop` 一次。


### 2. daemon 启动报 `DAEMON_TIMEOUT`，日志缺 `react` 模块

- **现象**：`daemon:stop` 后重启 daemon 直接超时，`~/.config/zenvfx/daemon.log` 显示类似：
  ```
  Error: Cannot find module 'react'
      at zustand/react.js
  ```
- **根因**：0.9.1 daemon 用 `zustand` 管状态，`zustand/index.js` 间接 import 了 `zustand/react.js`，但打包时未把 `react` 作为 bundled 依赖打入；Node.js 端无 `react` 即启动失败。
- **绕过**：在全局 CLI 安装目录手动补一个 `react` 即可——
  ```bash
  # 找到全局安装目录
  npm root -g
  # 进入 CLI 包目录补 react（版本不敏感，挂个 18 即可）
  cd "$(npm root -g)/@tencent/zenvfx-cli"
  npm install react@18 --no-save --registry=https://mirrors.tencent.com/npm/

  # 重启 daemon 验证
  zenvfx daemon:stop
  zenvfx daemon:status
  ```
- **彻底修复方向**（待发版）：在 `zenvfx-cli` 的 esbuild 配置里把 `zustand/react` 标为 external 或换用 `zustand/vanilla`，避免引入 react。

### 3. `file:id-to-path` 返回路径多拼了"项目名"层级

- **现象**：
  ```bash
  zenvfx file:id-to-path --id <fileId>
  # 返回:  /d6683tdk40pqu9ruglp0/内部项目体验/用户空间/李智_4866893/xxx
  # 实际:  /d6683tdk40pqu9ruglp0/用户空间/李智_4866893/xxx
  ```
- **根因**：`file:id-to-path` 在 projectId 之后多拼了项目名（如"内部项目体验"），与 VFS 实际路径结构不一致。直接用此路径调用 `canvas:*` / `file:stat` 会得到 `CANVAS_NOT_FOUND` / `FILE_NOT_FOUND`。
- **绕过**：用 `file:readdir` 反查真实路径——
  ```bash
  zenvfx file:readdir --path "/<projectId>/用户空间/<userDir>" 2>/dev/null
  # 或先 file:stat 探测两种路径，哪条 ok 用哪条
  ```
- **修复方向**（待发版）：`file:id-to-path` 拼接时去掉项目名层级，与 `file:readdir` / `file:stat` 路径口径对齐。

