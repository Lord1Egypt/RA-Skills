# xiaoai-ha-control

一个可分享的 OpenClaw skill，用于通过 **Home Assistant + Xiaomi Miot** 控制小爱音箱，并可选支持 **小爱 → OpenClaw** 的语音桥接。

它包含两部分能力：

1. **OpenClaw → 小爱音箱（下行控制）**
   - `say`：让小爱播报文本
   - `exec`：让小爱执行文本指令
   - `play`：让小爱播放 URL 音频
2. **小爱音箱 → OpenClaw（上行桥接，可选）**
   - 通过 Home Assistant conversation sensor 捕获小爱语音文本
   - 转发到宿主机 `bridge_server.py`
   - 命中白名单后再交给 OpenClaw main 处理

这份 README 按 **从零开始** 的方式写，方便其他人照着一步步搭建。

---

## 一、这个 skill 能做什么

### 1. OpenClaw 控制小爱音箱
适合这些场景：

- 让小爱播报一句话
- 让小爱执行一句文本命令
- 通过小爱控制米家设备
- 让小爱播放一个 mp3 / TTS / 音频 URL

示例：

```bash
bash scripts/xiaoai.sh say "你好，我是小叮当。"
bash scripts/xiaoai.sh exec "关闭客厅灯"
bash scripts/xiaoai.sh play "http://example.com/test.mp3"
```

### 2. 小爱把语音请求转给 OpenClaw
适合这些场景：

- 对小爱说：“问一下研究员，现在几点了？”
- 对小爱说：“告诉管家，明天提醒我开会。”
- 对小爱说：“问下邮差，有没有新邮件。”

这条链路不是必须的，属于 **可选增强能力**。

---

## 二、整体架构

### 模式 A：只用下行控制（最简单，推荐先跑通）

```text
OpenClaw → xiaoai.sh → Home Assistant API → 小爱音箱
```

### 模式 B：加上语音桥接（完整方案）

```text
小爱语音 → Home Assistant conversation sensor → shell_command → bridge_server.py → OpenClaw main
                                                                      ↓
                                                           xiaoai.sh say / exec / play
```

建议顺序：

1. 先跑通 **OpenClaw → 小爱**
2. 再接入 **小爱 → OpenClaw**

不要一上来就两条都一起调，排障会很痛苦。

---

## 三、前置条件

在开始前，请确认你已经具备以下环境：

1. 已安装并启动 **Home Assistant**
2. 已安装 **HACS**
3. 已安装 **Xiaomi Miot** 集成
4. 已将 **小爱音箱** 接入 Home Assistant
5. 已创建 **Home Assistant Long-Lived Access Token**
6. 已找到以下实体：
   - `play_text` 文本播报实体
   - `execute_text_directive` 文本指令实体
   - `media_player` 实体（用于播放 URL 音频，可选但推荐）

---

## 四、从零开始搭建

# 第 1 步：安装 Home Assistant

参考官方文档：

- Home Assistant: <https://www.home-assistant.io/installation/>

如果你已经有 HA，可以跳过。

---

# 第 2 步：安装 HACS

参考：

- HACS: <https://www.hacs.xyz/docs/use/download/download/>

---

# 第 3 步：安装 Xiaomi Miot

参考：

- Xiaomi Miot: <https://github.com/al-one/hass-xiaomi-miot>

安装后，把你的小爱音箱接入 HA。

---

# 第 4 步：确认小爱相关实体

进入 Home Assistant：

- **开发者工具 → 状态**

搜索这些关键词：

- `play_text`
- `execute_text_directive`
- `media_player`

如果接入成功，通常能看到类似：

```text
text.xiaomi_xxx_play_text
text.xiaomi_xxx_execute_text_directive
media_player.xiaomi_xxx_play_control
```

注意：
- 不同设备型号，实体名可能不同
- 你必须使用自己环境中的实体 ID，不能照搬别人的

---

# 第 5 步：安装 skill 文件

把 skill 放到：

```bash
~/.openclaw/skills/xiaoai-ha-control/
```

例如：

```bash
mkdir -p ~/.openclaw/skills/xiaoai-ha-control
cp -R xiaoai-ha-control/* ~/.openclaw/skills/xiaoai-ha-control/
chmod +x ~/.openclaw/skills/xiaoai-ha-control/scripts/*.sh
```

---

# 第 6 步：配置 `.env`

复制模板：

```bash
cp ~/.openclaw/skills/xiaoai-ha-control/.env.example ~/.openclaw/skills/xiaoai-ha-control/.env
```

编辑 `.env`：

```bash
HA_URL="http://your-home-assistant:8123"
HA_TOKEN="your-long-lived-access-token"
XIAOAI_PLAY_TEXT_ENTITY_ID="text.your_xiaoai_play_text"
XIAOAI_EXECUTE_TEXT_ENTITY_ID="text.your_xiaoai_execute_text_directive"
XIAOAI_MEDIA_PLAYER_ENTITY_ID="media_player.your_xiaoai_media_player"
```

### 每个字段的含义

#### `HA_URL`
你的 Home Assistant 地址，例如：

```bash
http://192.168.1.10:8123
```

#### `HA_TOKEN`
在 Home Assistant 用户页面生成 Long-Lived Access Token。

#### `XIAOAI_PLAY_TEXT_ENTITY_ID`
让小爱播报文本使用的实体。

#### `XIAOAI_EXECUTE_TEXT_ENTITY_ID`
让小爱执行文本命令使用的实体。

#### `XIAOAI_MEDIA_PLAYER_ENTITY_ID`
让小爱播放 URL 音频使用的实体。

---

## 五、先验证 OpenClaw → 小爱音箱

这是最基础、也最重要的一步。

### 1. 测试播报（say）

```bash
bash ~/.openclaw/skills/xiaoai-ha-control/scripts/xiaoai.sh say "你好，我是小叮当。"
```

### 2. 测试执行命令（exec）

```bash
bash ~/.openclaw/skills/xiaoai-ha-control/scripts/xiaoai.sh exec "关闭客厅灯"
```

### 3. 测试播放 URL 音频（play）

```bash
bash ~/.openclaw/skills/xiaoai-ha-control/scripts/xiaoai.sh play "http://example.com/test.mp3"
```

如果这三步至少前两步能通，说明 skill 的下行控制基本正常。

---

## 六、OpenClaw 中如何理解“小爱”

在当前推荐规则下：

- **带有 `【来自小爱】` / `【来自小爱语音】` 标识**
  - 视为：**小爱控制 OpenClaw**
- **不带上述标识，且普通聊天消息中出现 `小爱` / `小爱同学`**
  - 视为：**OpenClaw 控制小爱**

### 普通聊天中的下行控制映射

- 明确“说 / 播报 / 通知” → `say`
- 明确“播放音频 / 链接 / mp3” → `play`
- 其他默认 → `exec`

示例：

- `告诉小爱同学，5分钟后该我洗碗` → `exec`
- `让小爱播报一句：开会啦` → `say`
- `让小爱播放这个 mp3` → `play`

---

## 七、可选：接入“小爱 → OpenClaw”语音桥

如果你希望用户直接对小爱说话，再由 OpenClaw 处理，可以继续配置这一部分。

### 目标效果

用户对小爱说：

- `问一下研究员，现在几点了？`
- `告诉管家，明天提醒我开会。`

然后链路变成：

```text
小爱 → Home Assistant → bridge_server.py → OpenClaw main
```

---

## 八、桥接方案设计原则

### 1. HA 只做入口
Home Assistant 只负责：

- 监听 conversation sensor
- 把文本 POST 给宿主机 `bridge_server.py`

### 2. bridge_server.py 做网关判断
bridge 负责：

- 记录原始文本
- 判断是否命中白名单
- 命中后才转给 OpenClaw
- 未命中则终止，让小爱原生处理
- 计算 planned spoken（建议口播内容）并写入日志 / 状态

### 3. main 统一调度
OpenClaw main 负责：

- 统一理解小爱来源消息
- 必要时分配给子 agent
- 子 agent 完成后先回 main
- 再由 main 统一决定聊天结果与小爱口播

不要让 bridge 直接跳过 main 去找子 agent。

> 2026-03-30 更新：默认配置下，bridge **不再自动执行 `say`**，而是由 main 统一负责小爱口播，避免 bridge 与 main 同时播报导致双播。若确实需要恢复旧行为，可在 `whitelist.json` 中设置 `bridge_auto_say_enabled: true`。

---

## 九、桥接白名单原则

为了避免把“小爱原生命令”误转给 OpenClaw，bridge 使用 **白名单放行**：

- 命中白名单 → 转给 OpenClaw
- 未命中 → 留给小爱自己处理

### 典型会放行的表达

- `告诉管家，明天提醒我开会`
- `问一下研究员，现在几点了`
- `研究员，看看这个问题`

### 典型不会放行的表达

- `打开客厅灯`
- `播放音乐`
- `设置一个五分钟后的提醒`

这一步非常重要。不要在 HA 里堆复杂语义判断，白名单放到 bridge 里更容易维护。

---

## 十、如果消息里点名了子 agent

当消息带有 `【来自小爱】` / `【来自小爱语音】` 标识，且文本中明确点名了某个子 agent（例如研究员、邮差、码农、产品、运维、教练、运营等），推荐遵守以下规则：

1. **main 必须将任务分配给对应子 agent**
2. **子 agent 完成后，结果必须先回 main**
3. **由 main 统一负责聊天回复与小爱口播**

推荐链路：

```text
小爱 → bridge → main → 指定子 agent → main → 小爱
```

---

## 十一、如何启动桥接服务

**方式一：直接启动（推荐）**

```bash
bash ~/.openclaw/skills/xiaoai-ha-control/scripts/start_bridge.sh
```

脚本内部自动 fork 到后台运行，启动后立即返回，bridge 在后台独立运行。默认监听：

```text
0.0.0.0:8765
```

**方式二：手动 daemon 模式**

```bash
python3 ~/.openclaw/skills/xiaoai-ha-control/bridge_server.py --daemon
```

效果与方式一相同。

**方式三：launchd / systemd（长期运行）**

在 Mac 上使用 launchd 或 Linux 上使用 systemd，可以让服务开机自启：

- Mac（launchd）：将 `scripts/com.shinechen.xiaoai-bridge.plist` 复制到 `~/Library/LaunchAgents/`，然后 `launchctl load`（仅供参考，请根据实际情况修改 Label 和路径）
- Linux（systemd）：创建对应的 service unit

### launchd 注意事项（重要）

如果你使用 launchd 常驻运行 bridge：

1. **不要**在 plist 里再给 `bridge_server.py` 追加 `--daemon`
   - launchd 自己已经是进程管理器
   - 再 daemonize 会导致 launchd 与真实工作进程脱钩，不利于重启和排障
2. 建议显式注入环境变量：
   - `OPENCLAW_BIN`
   - `PATH`
3. 否则常见报错包括：
   - `FileNotFoundError: openclaw`
   - `env: node: No such file or directory`

健康检查：

```bash
curl http://127.0.0.1:8765/health
```

### bridge 关键运行配置（whitelist.json）

建议在 `whitelist.json` 中至少关注这几个字段：

```json
{
  "dedup_window_sec": 120,
  "max_spoken_len": 60,
  "bridge_auto_say_enabled": false
}
```

含义：
- `dedup_window_sec`：同一句在多长时间内视为重复，建议 120 秒
- `max_spoken_len`：planned spoken 的最大长度
- `bridge_auto_say_enabled`：是否允许 bridge 自动执行 `say`
  - `false`：默认推荐，由 main 统一决定并执行口播
  - `true`：恢复旧行为，由 bridge 在 worker 完成后自动播报

### requests.log 怎么看

从 2026-03-30 起，`requests.log` 里的 `WORKER_DONE` 重点看：
- `final_reply`：OpenClaw 最终回复
- `spoken`：bridge 计算出的建议口播内容
- `bridge_auto_say`：当前是否允许 bridge 自动播报
- `bridge_say_executed`：bridge 这次是否真的执行了 `say`

当 `bridge_auto_say=false` 时，`spoken` 只表示“建议播报内容”，**不代表 bridge 已经播过**。

---

## 十二、Home Assistant 示例思路

### automation
监听：

- `sensor.xiaomi_xxx_conversation`

### shell_command
把 conversation 文本 POST 到 bridge：

```bash
POST http://host.docker.internal:8765/xiaoai-to-butler
```

如果你的 HA 跑在 Docker Desktop for Mac 里，通常推荐优先试：

```text
host.docker.internal
```

如果你的部署环境不同，宿主机访问地址可能需要自己调整。

---

## 十三、延伸文档

- `README.md`：从零搭建总览
- `references/bridge-setup.md`：小爱语音桥接的单独搭建说明
- `NOTES.md`：兼容性边界、分享注意事项
- `STATUS.md`：当前架构定位与已知限制

如果你只想先用 `say / exec / play`，看完本 README 就够了。
如果你要继续接“小爱 → OpenClaw”桥接，请继续阅读：

- `references/bridge-setup.md`

## 十四、目录结构

```text
xiaoai-ha-control/
├── SKILL.md
├── README.md
├── NOTES.md
├── STATUS.md
├── bridge_server.py
├── .env.example
├── .gitignore
├── references/
│   └── bridge-setup.md
└── scripts/
    ├── start_bridge.sh             # 自动 fork 后台运行（推荐）
    ├── xiaoai.sh
    ├── xiaoai_say.sh
    ├── xiaoai_execute.sh
    ├── xiaoai_play.sh
    ├── xiaoai_to_butler.sh        # legacy/debug
    └── run_xiaoai_to_butler.sh    # legacy/debug
```

说明：
- `xiaoai_to_butler.sh` / `run_xiaoai_to_butler.sh` 主要保留给早期调试或兼容验证
- 推荐正式桥接入口是 `bridge_server.py`
- `bridge_server.py` 现在按**相对自身文件位置**查找 `scripts/xiaoai.sh`，不再依赖固定的本机绝对路径
- `openclaw` 默认直接从 PATH 查找；如有需要，可通过环境变量 `OPENCLAW_BIN` 覆盖

---

## 十四、常见问题

### 1. `.env` 配了，但脚本说 token 没设置
检查：

- `.env` 是否放在 skill 根目录
- 变量名是否拼写正确
- 是否有引号、空格、换行问题

### 2. `exec` 发送了，但小爱没执行
可能原因：

- 小爱本身听不懂这句话
- 设备命名与米家里实际名称不一致
- 该命令不适合通过 `execute_text_directive` 执行

### 3. 小爱说的话没进入 bridge
优先排查：

1. Home Assistant conversation sensor 是否更新
2. HA 的 `shell_command` 是否真的发出请求
3. Docker 到宿主机地址是否可达
4. `bridge_server.py` 是否监听在正确端口

### 4. bridge 收到了，但没转给 OpenClaw
看 `requests.log` / `status.json`：

- 如果是 `not_in_bridge_whitelist`
  - 说明这句被判定为留给小爱原生处理
- 如果是 `empty_text`
  - 说明 HA 发过来的 conversation 内容为空

### 5. 为什么不把所有小爱消息都转给 OpenClaw？
因为这样会误接大量小爱原生命令，比如：

- 打开灯
- 播音乐
- 设提醒
- 查天气

所以推荐用 **bridge 白名单放行**，而不是全量接管。

---

## 十五、安全提醒

`.env` 中包含你的 Home Assistant Token，请勿泄露、截图分享或提交到公开仓库。
如果 token 已泄露，请立即在 Home Assistant 中删除并重新生成。

---

## 十六、分享建议

如果你打算把这个 skill 分享给别人，建议同时说明：

1. **只用下行控制** 和 **加语音桥接** 是两种不同复杂度的用法
2. 新手请先跑通 `say / exec / play`
3. 语音桥接是增强功能，依赖更多环境细节
4. `bridge_server.py` 的白名单策略需要根据个人使用习惯调整
5. Docker / 宿主机网络连通性是桥接链路里最常见的坑

---

## 十七、最小可用路径（推荐给新用户）

如果你只是想先用起来，推荐只做这 4 步：

1. 装好 HA + HACS + Xiaomi Miot
2. 找到 `play_text` / `execute_text_directive` 实体
3. 配好 `.env`
4. 运行：

```bash
bash scripts/xiaoai.sh say "你好"
bash scripts/xiaoai.sh exec "关闭客厅灯"
```

先别急着上桥接。

当这两步稳定后，再继续接 `bridge_server.py`。
