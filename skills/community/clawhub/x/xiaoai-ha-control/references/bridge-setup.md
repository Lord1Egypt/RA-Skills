# bridge-setup.md

这个文件专门说明 **小爱音箱 → OpenClaw** 的桥接搭建方式。

如果你只想使用：

- `say`
- `exec`
- `play`

那么可以先忽略本文件。

桥接属于增强能力，建议在 **OpenClaw → 小爱** 已经稳定后再接入。

---

## 一、桥接目标

希望实现：

```text
小爱语音 → Home Assistant → bridge_server.py → OpenClaw main
```

例如用户对小爱说：

- `问一下研究员，现在几点了？`
- `告诉管家，明天提醒我开会。`

由 bridge 判断是否放行到 OpenClaw。

---

## 二、推荐分层

### 1. Home Assistant
只做入口：

- 监听 conversation sensor
- 触发 automation
- 优先使用 `rest_command` 把文本 POST 给 bridge

不要在 HA 里堆复杂语义判断。

### 2. bridge_server.py
做宿主机网关：

- 记录原始文本
- 判断是否命中白名单
- 命中才转给 OpenClaw
- 未命中则终止，让小爱原生处理
- 记录状态与日志
- 计算 planned spoken（建议口播内容）

> 2026-03-30 起，bridge 默认**不再自动执行 `say`**，而是由 main 统一决定并执行小爱口播。只有在 `whitelist.json` 中显式设置 `bridge_auto_say_enabled: true` 时，bridge 才会恢复自动播报。

### 3. OpenClaw main
做统一调度：

- 解释来自小爱的请求
- 必要时转给子 agent
- 子 agent 结果先回 main
- 再由 main 决定聊天回复与小爱口播

推荐链路：

```text
小爱 → bridge → main → 指定子 agent → main → 小爱
```

---

## 三、bridge 的核心原则

### 白名单放行
bridge 推荐使用：

- **默认拒绝**
- **命中白名单才放行**

原因：

如果不这样做，大量小爱原生命令也会被误转给 OpenClaw，例如：

- 打开客厅灯
- 播放音乐
- 设置提醒
- 查天气

而这些通常应该让小爱自己处理。

### 当前推荐白名单风格

放行：

- `告诉管家...`
- `问一下研究员...`
- `研究员，看看这个...`
- `告诉邮差...`

不放行：

- `打开客厅灯`
- `五分钟后提醒我洗碗`
- `今天天气怎么样`

---

## 十、如何自定义触发关键词和白名单

白名单配置集中在 `whitelist.json` 里（从 `whitelist.json.example` 复制），不需要改 Python 代码。

```bash
cp ~/.openclaw/skills/xiaoai-ha-control/whitelist.json.example \
   ~/.openclaw/skills/xiaoai-ha-control/whitelist.json
```

然后编辑 `whitelist.json`，常用自定义项：

### `whitelist_targets` — 目标关键词
想要小爱把哪些词当作"转发给 OpenClaw"的信号。例如加上"小爱"：

```json
"whitelist_targets": ["管家", "研究员", "小爱"]
```

### `whitelist_verbs` — 动作词
配合 targets 使用，句子里同时出现 target + verb 才会放行。例如加上"问"：

```json
"whitelist_verbs": ["让", "告诉", "问一下", "问"]
```

### `subagent_targets` — 子 agent 名称
如果你的子 agent 有其他名字，在这里加上：

```json
"subagent_targets": ["研究员", "邮差", "码农", "产品", "运维", "教练", "运营", "我的AI助手"]
```

### `dedup_window_sec` — 去重时间窗口
同一句话在多少秒内不重复处理，建议 120 秒：

```json
"dedup_window_sec": 120
```

### `max_spoken_len` — 小爱口播最大字数
超过这个长度的回复不会口播，只发文字：

```json
"max_spoken_len": 60
```

### `bridge_auto_say_enabled` — 是否允许 bridge 自动口播
控制 bridge 是否在 worker 完成后直接调用 `say`：

```json
"bridge_auto_say_enabled": false
```

推荐值：
- `false`：默认推荐，由 main 统一决定并执行小爱口播
- `true`：恢复旧行为，由 bridge 自动播报

修改后需要重启 bridge 服务（如果已启动的话）。

---

### 快速验证 whitelist 是否生效

启动时日志里会显示用的是哪个配置：

```json
{"updated_at": "...", "service": "xiaoai-ha-control-bridge", ...}
```

如果 `whitelist.json` 存在，使用的是 `whitelist.json`；如果不存在，用内置默认值。

也可以直接查看 `requests.log`，每次请求里 `matched_subagent` 会显示匹配到了哪个目标。

---

## 四、Home Assistant 示例思路

下面给的是思路示例，不同环境的实体 ID 需要自己替换。

### automation 示例思路

监听：

- `sensor.xiaomi_xxx_conversation`

当该 sensor 更新时，触发 shell_command。

### rest_command 示例思路（推荐）

把 conversation 内容 POST 给 bridge：

```yaml
rest_command:
  xiaoai_to_butler_http:
    method: POST
    url: http://192.168.10.105:8765/xiaoai-to-butler
    content_type: application/json
    payload: >
      {"text": "{{ state_attr('sensor.xiaomi_lx06_30cb_conversation', 'content') | default('', true) | trim }}", "source": "xiaoai-speaker"}
```

建议：
- 优先使用宿主机局域网 IP（如 `192.168.10.105`）
- 不要依赖 `host.docker.internal`（VPN / DNS 环境下容易失败）
- 优先使用 `rest_command` 而非 `shell_command`，避免 shell 层的 JSON / 转义问题

---

## 五、bridge_server.py 提供什么

推荐 bridge 提供：

- `POST /xiaoai-to-butler`
- `GET /health`

并记录：

- `requests.log`
- `status.json`
- 最近一次收到的文本
- 最近一次是否放行
- 最近一次失败原因
- `spoken`（planned spoken，建议口播内容）
- `bridge_auto_say` / `bridge_say_executed`

从 2026-03-30 起，查看日志时要区分：
- `spoken`：bridge 计算出的建议口播内容
- `bridge_say_executed=true/false`：bridge 这次是否真的执行了 `say`

---

## 六、如果消息里点名了子 agent

当 bridge 命中小爱来源消息，且文本中明确点名了某个子 agent（例如研究员、邮差、码农、产品、运维、教练、运营等），推荐处理规则是：

1. bridge 把命中的目标 agent 提示给 main
2. main 必须将任务分配给对应子 agent
3. 子 agent 完成后先回 main
4. 再由 main 统一决定聊天回复与小爱口播

bridge 不应该直接跳过 main 去找子 agent。

---

## 七、排障顺序

如果你发现“小爱说了，但 OpenClaw 没收到”，按下面顺序排查：

### 1. conversation sensor 有没有更新
先看 Home Assistant 中 `sensor.xiaomi_xxx_conversation` 是否真的拿到了文本。

### 2. automation 有没有触发
确认 automation 是否执行。

### 3. rest_command / automation 有没有真的发出去
看 HA 日志里是否有：

- 模板渲染错误
- 网络错误
- automation 重复触发

### 4. 容器能不能访问宿主机
如果 HA 在 Docker 里，重点检查：

- 宿主机局域网 IP
- 防火墙
- 端口监听
- 不要默认依赖 `host.docker.internal`

### 5. bridge 有没有收到
看：

- `requests.log`
- `status.json`
- `ha_conversation_content.txt`

### 6. 是没收到，还是收到了但被白名单挡掉
如果 bridge 收到了，但 `forwarded=false`，那说明是白名单逻辑拦住了，而不是桥没通。

---

## 八、已知常见坑

### 1. Xiaomi Miot conversation 拉取超时
可能导致文本为空，或者根本没更新。

### 2. `state` 与 `attributes.content` 混用
如果 condition 用的是 `attributes.content`，但 payload 发的是 `states(sensor)`，会导致重复触发或空文本问题。推荐统一使用 `attributes.content`。

### 3. Docker 到宿主机地址不可达
这是最常见的桥接失败原因之一。推荐使用宿主机局域网 IP，不要默认依赖 `host.docker.internal`。

### 4. launchd 环境缺少 `openclaw` / `node`
如果 bridge 用 launchd 常驻运行，需要显式补齐：
- `OPENCLAW_BIN`
- `PATH`

否则可能出现：
- `FileNotFoundError: openclaw`
- `env: node: No such file or directory`

### 5. 同时让 bridge 和 main 承担口播
这会导致双播。默认应由 main 统一口播；bridge 仅记录 planned spoken。

### 6. 把过多语义判断堆在 HA 里
后面会越来越难维护。推荐把白名单逻辑收在 bridge 里。

### 7. 让 bridge 直接找子 agent
这会绕过 main，破坏统一出口原则，不推荐。

---

## 九、推荐给使用者的最小联调流程

1. 先跑通：

```bash
bash scripts/xiaoai.sh say "你好"
bash scripts/xiaoai.sh exec "关闭客厅灯"
```

2. 再启动 bridge：

```bash
bash scripts/start_bridge.sh
curl http://127.0.0.1:8765/health
```

3. 再验证 HA 能不能 POST 到 bridge

4. 最后再测试真实小爱语音：

- `告诉管家，现在几点了？`
- `问一下研究员，现在几点了？`
