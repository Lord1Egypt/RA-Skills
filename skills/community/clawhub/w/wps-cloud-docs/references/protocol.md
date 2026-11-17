# WPS SkillHub MCP 协议（实测记录）

来源：反查 WorkBuddy `kdocs` 连接器（`~/.workbuddy/plugins/cache/workbuddy-connector-plugins-official/kdocs/*/`）+ 直连实测，2026-11-15。

## 1. 端点

| 用途 | 地址 |
| --- | --- |
| MCP 服务 | `https://mcp-center.wps.cn/skill_hub/mcp` |
| 授权引导页 | `https://mcp-center.wps.cn/kdocs-auth/auth-guide?auth_code=<uuid4>` |
| 换取 token | `POST https://api.wps.cn/office/v5/ai/skill_hub/wps_auth/exchange` body `{"code":"<uuid4>"}` |

## 2. 请求头

```
Content-Type: application/json
Accept: application/json, text/event-stream
X-Request-Source: workbuddy      # 官方占位值，非 workbuddy 也可用
X-Skill-Version: 1.6.14
X-Client-Id: <16位 hex，本地生成并固定>
Authorization: Bearer <skill_hub token>   # 未登录可省略，仅 tools/list 可用
mcp-session-id: <initialize 响应头回传>    # 后续请求必带
```

## 3. 握手顺序

1. `initialize`（JSON-RPC，`protocolVersion: 2024-11-05`）→ 响应头拿到 `mcp-session-id`
   - 未登录也返回 200 + `serverInfo: SkillHub MCP 1.0.0`
   - 同时响应头带 `x-kso-auth-status: notLogin`、`x-kso-auth-raw-error: userNotLogin`
2. `tools/list` → 未登录可读全量（实测 **638** 个工具，单次响应约 450KB JSON/SSE）
3. `tools/call` → 需 token；无 token 时业务层返回未授权/`userNotLogin`
4. 登录成功后响应头 `x-kso-auth-status: login` ← 判断 token 有效性的最可靠信号

## 4. token 交换返回

```json
{"code":200,"data":{"token":"<...>","expires_in":<秒>}}
```

| 返回码 | 含义 | 处理 |
| --- | --- | --- |
| 200 + token | 成功 | 写入 `WPS_KDOCS_TOKEN` |
| 202 | 用户还没完成登录 | 继续轮询 |
| 403 | 当前是 **企业账号**，不支持 | 切个人账号重来 |
| 409 | 用户取消授权 | 结束 |
| 5xx | 服务端临时错误 | 继续轮询 |

## 5. 工具分组（638 个）

- `aippt.*` — AI 生成 PPT（多轮会话协议）
- `auto_sheet.*` — 表格自动化流程（DSL 编译 + 校验 + 试跑）
- `dbsheet.*` — 多维表格：schema / 记录 / 字段 / 视图 / 仪表盘 / 权限 / webhook
- `create_file_with_content` · `create_empty_file` · `create_folder` · `upload_new_file`
- `search_files` · `check_file_name` · `batch_get_file_info` · `copy_file`
- `drive.*` — 云盘：搜索、下载、分享、版本、标签、收藏、回收站
- `wps.*` / `otl.*` — 文字文档：正文块、文本格式、表格、图形、页眉页脚、批注、修订、目录、水印、导出
- `sheet.*` — 表格：数据、筛选、条件格式、数据校验、工作表
- `pdf.*` — 转换、拆分合并、翻译、检视
- `kwiki.*` / `form.*` / `wpp.*` — 知识库、收集表、演示文稿

## 6. WorkBuddy 侧对照

| WorkBuddy 步骤 | 等价的 Hermes 实现 |
| --- | --- |
| `mcporter config add kdocs-workbuddy <url> --header ...` | `wps_mcp.py` 直接拼 header |
| `bash skills/scripts/setup.sh` | 不需要（无 mcporter 依赖） |
| `node get-token.js` | `scripts/wps_auth.py`（Python 等价实现） |
| `mcporter call kdocs-workbuddy.<tool>` | `python3 wps_mcp.py call <tool> '<json>'` |

WorkBuddy 的 `setup.sh` 用一次探针调用（`search_files keyword=__kdocs_token_probe__`）判断 token 是否失效，判定依据是返回 `"code": 400006`。Hermes 版改用 `x-kso-auth-status` 头，少一次调用。
