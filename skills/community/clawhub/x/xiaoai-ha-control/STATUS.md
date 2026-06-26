# XiaoAI ↔ OpenClaw Bridge Status

## Current Positioning

这个 skill 现在包含两层能力：

1. **OpenClaw → 小爱音箱（基础能力）**
   - `say`
   - `exec`
   - `play`
2. **小爱音箱 → OpenClaw（可选桥接能力）**
   - 通过 Home Assistant conversation sensor 捕获小爱语音文本
   - 通过 `bridge_server.py` 转交给 OpenClaw main

对外分享时，建议把 **下行控制** 视为核心能力，把 **上行桥接** 视为可选增强模块。

---

## Current Architecture

正式推荐链路：

```text
小爱语音 → Home Assistant conversation sensor → rest_command → bridge_server.py → OpenClaw main
```

> ⚠️ 2026-03-28 更新：Docker 容器内 HA 访问宿主机 bridge 应使用宿主机局域网 IP（如 `192.168.10.105`），而不是 `host.docker.internal`（DNS 解析会失败）；同时推荐使用 `rest_command` 而非 `shell_command`，避免 Jinja tojson 在 shell 单引号内的转义 bug。
>
> ⚠️ 2026-03-30 更新：bridge 默认**不再自动口播**，改为由 **main 统一决定并执行小爱口播**。`bridge_server.py` 仍会记录 `spoken`（计划口播内容），但只有在 `whitelist.json` 中显式开启 `bridge_auto_say_enabled: true` 时，bridge 才会实际执行 `say`。

设计原则：

- HA 只做入口
- `bridge_server.py` 做白名单放行、状态记录、planned spoken 计算
- main 统一调度子 agent 和最终出口（包括默认的小爱口播）
- 避免 bridge 与 main 同时承担口播职责，防止双播

---

## Rule Source of Truth

规则来源以以下文件为准：

- `SKILL.md`：skill 触发与下行控制说明
- `README.md`：从零搭建与完整架构说明
- `bridge_server.py`：桥接白名单与网关逻辑

如果当前工作区内还存在更强的本地行为规则（如使用者自己的 `AGENTS.md`），应以使用者本地规则为准；对外分享时不要依赖个人工作区规则才能理解 skill。

---

## Legacy / Debug Scripts

以下脚本主要保留用于早期调试或兼容验证：

- `scripts/xiaoai_to_butler.sh`
- `scripts/run_xiaoai_to_butler.sh`

它们已尽量去掉固定本机路径，但仍属于 legacy/debug 入口，不建议继续作为正式桥接入口。

推荐正式入口：

- `bridge_server.py`
- `scripts/start_bridge.sh`

---

## Known Limitations

### 1. 小米会话同步并不总是稳定
`conversation sensor` 可能因 Xiaomi Miot / 云端接口超时而拉取失败。

### 2. Docker 到宿主机的网络连通性需要单独验证
如果 Home Assistant 跑在 Docker 里，容器访问宿主机 bridge 时：
- ⚠️ 不要使用 `host.docker.internal`（DNS 解析在 VPN 环境下会失败）
- ✅ 推荐使用宿主机局域网 IP（如 `192.168.10.105`）
- ✅ 推荐使用 `rest_command` 而非 `shell_command`（避免 Jinja tojson 转义 bug）

### 3. launchd 环境与交互 shell 不同
如果 bridge 通过 launchd 常驻运行：
- 不要再给 `bridge_server.py` 叠加 `--daemon`，否则会出现 launchd 与子进程脱钩的问题
- 需要在 launchd 环境里显式提供 `OPENCLAW_BIN` 和 `PATH`
- 否则可能出现：
  - `FileNotFoundError: openclaw`
  - `env: node: No such file or directory`

### 4. 日志里的 `spoken` 默认表示“计划口播内容”
在当前默认配置下（`bridge_auto_say_enabled: false`）：
- `spoken` 仅表示 bridge 计算出的建议口播内容
- 真正是否口播、口播什么，由 main 决定
- `requests.log` 应结合 `bridge_auto_say` / `bridge_say_executed` 一起看，不能只看 `spoken`

### 3. 小爱原生能力可能先于桥接处理
例如天气、时间、设备控制、提醒等，小爱可能直接自己回答或执行。
因此推荐使用更明确的转交句式，例如：

- `告诉管家...`
- `问一下研究员...`

### 4. 白名单需要因人而异
`bridge_server.py` 中的放行白名单只是一个基础版本，分享给别人时需要提醒他们根据自己的 agent 命名和使用习惯调整。

---

## Recommended Sharing Guidance

如果你要把这个 skill 分享出去，建议明确告诉使用者：

1. 先跑通 `say / exec / play`
2. 再考虑接语音桥接
3. bridge 白名单不是万能规则，需要自己调
4. Docker / 宿主机网络连通性是最常见的坑
5. 不要假设所有小爱型号都暴露同样的实体
