---
name: xiaoai-ha-control
description: 通过 Home Assistant + Xiaomi Miot 控制小爱音箱，并可选支持“小爱语音 → OpenClaw”的桥接。适用于两类场景：1) 用户要求“让小爱说一句… / 播报… / 通知…”、“告诉小爱… / 让小爱执行…”、“让小爱播放音频 / mp3 / 链接”时，使用本 skill 进行下行控制；2) 已接入小爱语音桥时，处理带有 `【来自小爱】` / `【来自小爱语音】` 标识的上行消息。只要任务涉及小爱音箱控制、通过小爱执行命令、通过小爱播报结果，或小爱来源消息的桥接与分流，就应使用此 skill。
---

# xiaoai-ha-control

这个 skill 提供两层能力：

1. **OpenClaw → 小爱音箱（核心能力）**
   - `say`：让小爱播报文本
   - `exec`：让小爱执行文本指令
   - `play`：让小爱播放 URL 音频
2. **小爱音箱 → OpenClaw（可选桥接能力）**
   - 通过 Home Assistant conversation sensor + `bridge_server.py` 把小爱语音文本转给 OpenClaw

优先把它理解为一个 **小爱控制 skill**；语音桥接是可选增强，不是所有用户都必须启用。

## 何时使用

### A. 普通聊天中，用户想让 OpenClaw 控制小爱
当消息**不带** `【来自小爱】` / `【来自小爱语音】` 标识，并且文本中出现：

- `小爱`
- `小爱同学`

优先按 **OpenClaw 控制小爱** 处理。

推荐映射：

- 明确“说 / 播报 / 通知” → `say`
- 明确“播放音频 / 链接 / mp3” → `play`
- 其他默认 → `exec`

示例：

- `告诉小爱同学，5分钟后该我洗碗` → `exec`
- `让小爱播报一句：开会啦` → `say`
- `让小爱播放这个 mp3` → `play`

### B. 消息带有小爱来源标识
当消息中明确带有：

- `【来自小爱】`
- `【来自小爱语音】`

说明这是 **小爱控制 OpenClaw** 的上行请求。

此时：

- 不要把它当普通聊天消息理解
- 若环境已接入 bridge，应按桥接规则处理
- 若桥接环境未配置，则只说明当前未接入该能力，不要假装已经收到真实小爱入口事件

## 前置条件

使用本 skill 前，通常需要：

1. 已安装并启动 Home Assistant
2. 已安装 HACS
3. 已安装 Xiaomi Miot
4. 已将小爱音箱接入 HA
5. 已找到以下实体：
   - `play_text`
   - `execute_text_directive`
   - `media_player`（可选但推荐）
6. 已配置 `.env`：
   - `HA_URL`
   - `HA_TOKEN`
   - `XIAOAI_PLAY_TEXT_ENTITY_ID`
   - `XIAOAI_EXECUTE_TEXT_ENTITY_ID`
   - `XIAOAI_MEDIA_PLAYER_ENTITY_ID`

详细搭建步骤见 `README.md`。

## 推荐调用

### say

```bash
bash scripts/xiaoai.sh say "你好，我是小叮当。"
```

### exec

```bash
bash scripts/xiaoai.sh exec "关闭客厅灯"
```

### play

```bash
bash scripts/xiaoai.sh play "http://example.com/test.mp3"
```

## 语音桥接规则（启用 bridge 时）

如果已启用 `bridge_server.py`：

- HA 只做入口转发
- `bridge_server.py` 负责白名单放行
- 命中白名单才继续交给 OpenClaw
- 未命中则终止，让小爱原生处理

若带小爱来源标识的文本中**明确点名了某个子 agent**（如研究员、邮差、码农、产品、运维、教练、运营等），推荐规则是：

1. `main` 必须将任务分配给对应子 agent
2. 子 agent 完成后先回 `main`
3. 再由 `main` 统一决定聊天回复与小爱口播

不要让 bridge 直接跳过 main 去找子 agent。

## 重要注意事项

- `say` 用于播报，不负责设备控制
- `exec` 用于让小爱理解一条文本命令，能否成功取决于小爱本身是否能理解该命令
- `play` 用于播放 URL 音频，要求小爱音箱能访问该 URL
- 不同设备型号、不同 Xiaomi Miot 接入方式，暴露的实体可能不同
- 如果要对外分享，请提醒使用者：先跑通 `say / exec / play`，再考虑语音桥接

## 文档导航

- `README.md`：从零搭建、完整架构、桥接说明
- `NOTES.md`：兼容性边界、分享注意事项
- `STATUS.md`：当前架构定位与已知限制
