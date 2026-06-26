---
name: VacuumControl
description: >
  教 OpenClaw 如何安装、配置和使用 roborock-cli（石头扫地机 CLI 控制工具）。
  涵盖：uv 安装、认证流程、15 个 CLI 命令的使用、设备控制、错误诊断与恢复。
  当用户提到"扫地机"、"roborock"、"扫地"、"拖地"、"清洁机器人"、"回充"、"集尘"、
  "洗拖布"、"勿扰模式"、"roborock-cli"、"石头扫地机"、"扫地机器人"时触发本 skill。
  也适用于用户想编写扫地机自动化脚本、定时清洁、集成 roborock-cli 到其他系统的场景。
---

# Roborock CLI — Agent 操作手册

本 skill 指导你（OpenClaw）如何安装和使用 roborock-cli 来控制石头扫地机。
所有命令输出格式化 JSON，可直接用 `jq` 解析。

## 前置检查（每次操作前）

```
用户想做什么？
├─ 安装 roborock-cli → §1 安装流程
├─ 首次使用 / 认证问题 → §2 认证流程
├─ 查询设备信息 → §3 查询命令
├─ 控制扫地机 → §4 控制命令
├─ 故障排除 → §5 错误处理
└─ 编写自动化脚本 → §6 脚本集成
```

---

## §1 安装流程

### 1.1 检查 uv 是否已安装

```bash
uv --version
```

- 成功：输出版本号 → 跳到 1.3
- 失败：`command not found` → 执行 1.2

### 1.2 安装 uv

**macOS / Linux**：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**：
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装后验证：`uv --version`

### 1.3 安装 roborock-cli

```bash
uv tool install roborock-cli
```

验证：
```bash
roborock-cli --version
```

- 成功：输出 `roborock-cli x.y.z`
- 失败（Windows `os error 4551`）：→ §5.4

### 1.4 更新

```bash
uv tool upgrade roborock-cli
```

### 1.5 卸载

```bash
uv tool uninstall roborock-cli
rm -rf ~/.cache/roborock-cli/    # 清理认证和缓存
```

---

## §2 认证流程

认证是所有其他命令的前置条件。认证信息保存在 `~/.cache/roborock-cli/user_data.json`。

### 2.1 执行认证

```bash
roborock-cli auth
```

**要求**：必须在交互式 TTY 终端执行（不支持管道/非交互环境）。

**流程**：
1. 运行 `roborock-cli auth`，提示用户输入 Roborock 账号邮箱
2. 等待用户输入邮件中收到的验证码
3. 认证信息自动保存
- 账号邮箱可以在Roborock APP中查看、设置和修改"

**⚠️ 重要：避免重复运行 `roborock-cli auth`**

每次运行 `roborock-cli auth` 都会发送新的验证码，导致之前的验证码立即失效。正确做法：

- 只运行一次 `roborock-cli auth`，然后等待用户提供验证码
- 如果验证码输入后验证失败，先询问用户："验证失败，是否需要重新发送验证码？"
- 只有用户确认同意后，才再次运行 `roborock-cli auth`
- **绝对不要**在用户还没输入验证码时就重新运行 `roborock-cli auth`

### 2.2 验证认证是否有效

```bash
roborock-cli devices
```

- 成功：输出设备 JSON → 认证有效
- 失败（exit_code=2）：认证过期 → 重新执行 `roborock-cli auth`

---

## §3 查询命令

查询命令不改变设备状态，可安全执行。

### 命令总览

| 命令 | 用途 | 关键输出 |
|------|------|----------|
| `devices` | 列出设备 | `devices[].name` → `-d` 参数 |
| `status -d DEV` | 设备状态 | `rooms[].segment_id` → `start-clean -s` |
| `routines -d DEV` | 智能场景 | `routines[].id` → `execute-routine` |
| `map -d DEV` | 地图信息 | 位置坐标、可选保存 PNG |

### 数据流（命令间依赖）

```
devices → name ──────────────────────► 所有命令的 -d 参数（模糊匹配）
status  → rooms[].segment_id ───────► start-clean -s（指定房间）
status  → dnd_enabled/start/end ────► set-dnd（修改勿扰）
status  → volume.value ────────────► set-volume（修改音量）
routines → routines[].id ──────────► execute-routine（执行场景）
```

### 设备选择规则（`-d` 参数）

- 单设备：可省略 `-d`，自动选择
- 多设备：必须指定 `-d`，否则报 exit_code=4（ParamError）
- 匹配方式：子串匹配，不区分大小写（`-d 客厅` 匹配 "客厅扫地机"）

### 典型查询序列

```bash
# 1. 获取设备名
roborock-cli devices | jq '.devices[].name'

# 2. 获取设备状态（含房间列表）
roborock-cli status -d "设备名" | jq '.rooms.value'

# 3. 获取场景列表
roborock-cli routines -d "设备名" | jq '.routines[]'
```

完整的命令参数和输出字段规格，参见 `references/commands.md`。

---

## §4 控制命令

所有控制命令成功返回 `{"status": "ok", ...}`。执行前应确认设备状态。

### 决策树：用户想控制什么？

```
用户意图
├─ 清洁
│  ├─ 全屋清洁 → start-clean
│  ├─ 指定房间 → 先 status 获取 segment_id → start-clean -s ID [-r N]
│  ├─ 暂停 → pause-clean
│  ├─ 恢复 → resume-clean
│  └─ 停止 → stop-clean
├─ 回充电座 → go-home
├─ 基座操作
│  ├─ 集尘 → dock-action start_collect_dust / stop_collect_dust
│  └─ 洗拖布 → dock-action start_wash / stop_wash
├─ 声音与勿扰
│  ├─ 调节音量 → set-volume N（0-100）
│  ├─ 发声寻找机器人 → find-robot（让机器人发出"滴滴"声，不返回坐标）
│  └─ 勿扰模式 → set-dnd enable --start HH:MM --end HH:MM / set-dnd disable
└─ 场景 → 先 routines 获取 id → execute-routine ID
```

### 控制前检查模式

在执行控制命令前，建议先检查设备状态：

```bash
# 检查设备是否空闲
STATE=$(roborock-cli status -d "设备名" | jq -r '.state.value')
# state=charging / idle → 可以开始清洁
# state=cleaning → 正在清洁中
# state=error → 有错误，检查 error_code
```

### 指定房间清洁完整流程

```bash
# 1. 获取房间 segment_id
roborock-cli status -d "设备名" | jq '.rooms.value[] | "\(.segment_id) → \(.name)"'

# 2. 执行清洁（segment_id=16，清洁 2 遍）
roborock-cli start-clean -d "设备名" -s 16 -r 2

# 3. 验证已开始
roborock-cli status -d "设备名" | jq '.state.value'
# 期望输出: "cleaning"
```

完整的命令参数规格，参见 `references/commands.md`。

---

## §5 错误处理

### 退出码速查

| 退出码 | 含义 | 恢复动作 |
|--------|------|----------|
| 0 | 成功 | — |
| 1 | 通用错误（连接超时等） | 检查网络 → 重试 |
| 2 | 认证错误 | `roborock-cli auth` 重新认证 |
| 3 | 设备错误 | `roborock-cli devices` 确认设备名 |
| 4 | 参数无效 | 检查参数范围（音量 0-100、时间 HH:MM） |
| 5 | 内部错误 | 报告给用户 |
| 130 | 用户中断 | Ctrl+C，无需处理 |

错误输出格式：`{"error": "描述", "exit_code": N}`

### 5.1 连接超时（exit_code=1）

```
{"error": "连接超时（30.0秒）", "exit_code": 1}
```

排查步骤：
1. 确认网络连接正常
2. 确认设备在线（通过 Roborock App）
3. 重试命令

### 5.2 认证过期（exit_code=2）

```bash
roborock-cli auth    # 重新认证即可
```

### 5.3 API 频率限制（9002 错误）

Roborock API 限制 `get_home_data` 调用 5 次/小时、40 次/天。

诊断：
```bash
ls -la ~/.cache/roborock-cli/device_cache.pkl
# 正常 ~3KB，0 字节说明缓存写入失败
```

修复：
```bash
rm ~/.cache/roborock-cli/device_cache.pkl
roborock-cli devices    # 重建缓存
```

### 5.4 Windows `os error 4551`

Windows 安全策略阻止 uv 缓存目录下的 Python 解释器。

修复方法 1（推荐）：
```bash
uv cache clean
uv tool install roborock-cli
```

修复方法 2：
```bash
uv tool install --python python3.12 roborock-cli
```

---

## §6 脚本集成

### 退出码检查

```bash
if roborock-cli start-clean -s 16 >/dev/null; then
  echo "清洁已启动"
else
  echo "启动失败，退出码: $?"
fi
```

> 注意：roborock-cli 的正常输出和错误 JSON 都输出到 stdout，不输出到 stderr。抑制输出用 `>/dev/null`，不是 `2>/dev/null`。

### JSON 输出解析

所有正常输出为格式化 JSON（`indent=2, ensure_ascii=False`），可用 `jq` 处理：

```bash
# 获取电池电量
roborock-cli status -d "设备名" | jq '.battery.value'

# 获取所有房间名和 ID
roborock-cli status -d "设备名" | jq '.rooms.value[] | {name, segment_id}'

# 获取场景 ID 和名称
roborock-cli routines -d "设备名" | jq '.routines[] | "\(.id) → \(.name)"'
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ROBOROCK_AUTH_CACHE` | `~/.cache/roborock-cli/user_data.json` | 认证缓存路径 |
| `ROBOROCK_DEVICE_CACHE` | `~/.cache/roborock-cli/device_cache.pkl` | 设备缓存路径 |

### V1 协议要求

除 `auth` 和 `devices` 外，所有命令要求设备支持 V1 协议。不支持时返回 exit_code=3。绝大多数近年 Roborock 设备均支持。

---

## 参考资料

- 完整命令规格（参数、输出字段、示例）：读取 `references/commands.md`
- 需要某个命令的详细参数或输出字段时，读取该文件的对应章节
