# NOTES.md

## 这个 skill 的分享定位

对外分享时，推荐把它定位成：

> 一个通过 Home Assistant + Xiaomi Miot 控制小爱音箱的 OpenClaw skill，支持 `say / exec / play`，并可选扩展为“小爱语音 → OpenClaw”的桥接方案。

不要把它一上来就描述成“完整小爱语音中控系统”，否则新用户很容易高估默认能力范围。

---

## 推荐的使用顺序

### 第一阶段：先跑通下行控制
先验证：

- `say`
- `exec`
- `play`

即：

```bash
bash scripts/xiaoai.sh say "你好"
bash scripts/xiaoai.sh exec "关闭客厅灯"
```

只要这一步没稳定，就不要急着上桥接。

### 第二阶段：再接语音桥接
桥接链路涉及：

- Xiaomi Miot conversation sensor
- Home Assistant automation / shell_command
- Docker 到宿主机网络
- `bridge_server.py`
- OpenClaw main 分流

排障复杂度明显更高。

---

## 已验证能力

### 1. say（播报）
通过 `play_text` 实体可以让小爱播报文本。

### 2. exec（执行文本指令）
通过 `execute_text_directive` 实体可以向小爱发送文本命令。

### 3. play（播放 URL 音频）
通过 `media_player.play_media` 可以让小爱播放 URL 音频。

---

## 已验证结论

- 直接让小爱“播报一句控制命令”并不会让它执行该命令
- 真正执行命令应优先走 `execute_text_directive`
- `exec` 是否成功，取决于命令文本是否能被小爱理解，以及米家设备命名是否匹配
- `play` 是否成功，取决于音频 URL 是否能被小爱访问

---

## 语音桥接的推荐原则

### 1. HA 只做入口
不要在 HA 里堆大量语义判断。

### 2. bridge 做网关
`bridge_server.py` 负责：

- 白名单放行
- 记录日志
- 写状态
- 计算 planned spoken（建议口播内容）
- 把来源和命中的目标 agent 提示给 main

### 3. main 统一调度与统一口播
不要让 bridge 直接找子 agent。

推荐链路：

```text
小爱 → bridge → main → 指定子 agent → main → 小爱
```

**当前默认行为（2026-03-30 起）：**
- `bridge_auto_say_enabled: false`
- bridge 默认**不自动播报**
- main 统一决定是否对小爱口播、播什么

这样做的原因是：如果 bridge 和 main 同时承担 `say`，很容易出现双播。

---

## 兼容性边界

以下情况目前**未保证通用**：

1. 所有小爱型号都暴露相同实体
2. 非 Xiaomi Miot 接入方式适用
3. 所有命令都能通过 `exec` 成功执行
4. 所有设备都支持 `media_player` 播放 URL 音频
5. 所有 Docker / 宿主机网络环境都能直接复用同样的地址配置

因此，共享给别人时要明确：

- `.env` 里的实体 ID 必须自己查
- Home Assistant 地址、Docker 网络、桥接白名单都需要按自己环境调整

---

## 语义方向规则（推荐）

### 带小爱来源标识
如果消息带：

- `【来自小爱】`
- `【来自小爱语音】`

则视为：

- **小爱控制 OpenClaw**

### 不带来源标识，但文本中有“小爱 / 小爱同学”
则优先视为：

- **OpenClaw 控制小爱**

这条规则对外说明时要写清楚，否则用户容易把两个方向理解反。

---

## 对外分享时建议提醒的坑

1. 新用户不要一上来就配 bridge
2. Docker 里的 HA 到宿主机 bridge 的网络连通性经常出问题
3. Xiaomi Miot 的 conversation 拉取可能会超时
4. 白名单放行是为了避免误接管小爱原生命令
5. bridge 只是网关，不应该越权直接分配子 agent
6. 如果用 launchd 常驻运行，不要再给 `bridge_server.py` 叠加 `--daemon`
7. launchd 环境需要显式补齐 `OPENCLAW_BIN` 与 `PATH`，否则可能找不到 `openclaw` / `node`
8. `spoken` 不一定等于“已经由 bridge 播报”，要结合 `bridge_auto_say_enabled` 和 `bridge_say_executed` 看
