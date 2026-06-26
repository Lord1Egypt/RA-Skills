---
name: uds-diagnostic-test
version: "2.9.0"
description: "UDS 诊断测试技能。Use when: 收到诊断调查表、UDS diagnostic survey table、生成 UDS 测试脚本、基于诊断资料生成测试、执行 UDS 诊断测试、CAN 测试、DID 测试、DTC 测试、IOControl 测试、RoutineControl 测试、诊断服务测试、diagnostic test script generation and execution via SocketCAN"
argument-hint: "提供诊断调查表文件路径，或描述需要测试的诊断服务"
---

# UDS 诊断测试技能

## 目标

这个 skill 只解决三件事：

1. 用固定 Python 环境解析调查表
2. 生成并验证 UDS 测试脚本
3. 在 SocketCAN 环境下执行测试

详细驱动安装、WSL2 USB 透传、SecurityAccess 替代方案、NRC 说明、调查表默认值参考，统一放在 `README.md`，不要在当前技能主流程里重复展开。

## 唯一规则

- 唯一环境入口：先进入 skill 根目录，再执行 `bash ./scripts/setup_env.sh`
- 唯一环境来源：`~/.uds_env`
- 唯一 CAN 后端：SocketCAN（`can0` / `can1`），不要使用 `PCAN_*`
- 唯一正确包名：`python-can`，不要执行 `pip install can`
- 环境修复默认只允许重跑 `setup_env.sh`；除非用户明确要求，否则不要手工执行 `pip uninstall/install`
- 默认工作目录：`$HOME/.uds_workspace`

## 高频错误快查

| 现象 | 处理 |
|------|------|
| `Invalid CAN Bus Type - None` | 先修 Python 环境，不要先查硬件；先进入 skill 根目录，再执行 `bash ./scripts/setup_env.sh` |
| `No module named 'can'` / `can.interfaces.socketcan` | 先进入 skill 根目录，再执行 `bash ./scripts/setup_env.sh` |
| pip 只能装出 `can-0.0.0` 或 `python-can 1.5.x` | 不要循环重装；这是包源/镜像问题。停止重试，把当前 pip 源异常报告给用户 |
| 装成 `can-0.0.0` | 先重跑 `bash ./scripts/setup_env.sh`；如果脚本仍然报告 `can-0.0.0` 或 `python-can 1.5.x`，停止重试并报告包源异常 |
| `No such interface: can0` / `Network is down` | 执行 `"$PYTHON" "$UDS_SKILL_DIR/scripts/can_init.py"` |
| `SyntaxError: closing parenthesis` 执行 `.sh` 脚本 | `.sh` 文件不能用 `python3` 执行。改用 `"$PYTHON" "$UDS_SKILL_DIR/scripts/can_init.py"` |
| `Permission denied` | 用 `sudo` 执行 `can_init.py` |
| `zipfile.BadZipFile` | 调查表文件损坏或加密，要求用户提供无密码文件 |
| 生成器拒绝生成（关键CAN参数使用默认值） | 调查表缺少 TX/RX CAN ID 或波特率。向用户展示缺失参数表格，获取确认后使用 `--confirmed` 重新生成 |
| `./scripts/setup_env.sh` 不存在 / `SKILL.md` 缺失 | 技能目录不完整。不要手工补目录或补文件，重新获取完整的 `uds-diagnostic-test` 目录 |

## 会话初始化

每次开始任务前，只做这一段：

```bash
source ~/.uds_env 2>/dev/null || { echo "[ERROR] ~/.uds_env 不存在，请先进入 skill 根目录，再执行 bash ./scripts/setup_env.sh"; exit 1; }
PYTHON="$UDS_PYTHON"
SKILL_DIR="$UDS_SKILL_DIR"
UDS_WORK="${UDS_WORK:-$HOME/.uds_workspace}"
test -x "$PYTHON" || { echo "[ERROR] UDS_PYTHON 无效: $UDS_PYTHON"; exit 1; }
[ -f "$SKILL_DIR/SKILL.md" ] || { echo "[ERROR] UDS_SKILL_DIR 无效: $SKILL_DIR"; exit 1; }
mkdir -p "$UDS_WORK"
```

## 标准流程

### 1. 环境准备

前提：当前目录必须是包含 `SKILL.md` 和 `scripts/` 的 `uds-diagnostic-test` 目录。

执行命令：

```bash
bash ./scripts/setup_env.sh
```

### 2. 解析调查表

```bash
source ~/.uds_env
PYTHON="$UDS_PYTHON"
SKILL_DIR="$UDS_SKILL_DIR"
UDS_WORK="${UDS_WORK:-$HOME/.uds_workspace}"
mkdir -p "$UDS_WORK"

"$PYTHON" "$SKILL_DIR/scripts/uds_survey_parser.py" \
  --input "<调查表文件路径>" \
  --output "$UDS_WORK/uds_parsed.json"
```

然后读取 `$UDS_WORK/uds_parsed.json`，检查以下三项并展示给用户：

- `can_config`: 调查表中的 CAN 配置（TX/RX ID、波特率、CAN FD 等）
- `defaults_used`: 使用了默认值的 DID/IO/Routine 字段
- `missing_attributes`: 调查表中完全缺失的属性

### 2.5 强制确认（阻断点）

**在生成脚本之前，必须执行以下检查，缺一不可：**

1. 如果 `can_config` 缺少 `tx_id`、`rx_id` 或 `bitrate`，**必须**询问用户提供真实值
2. 如果 `defaults_used` 非空，**必须**以表格展示给用户确认
3. 如果 `missing_attributes` 非空，**必须**告知用户哪些属性缺失

**确认表格必须包含：**

| 参数 | 调查表值 | 将使用的值 | 来源 |
|------|---------|-----------|------|
| TX CAN ID | 0x671 / 缺失 | 0x7E0 | 调查表 / 硬编码默认 |
| RX CAN ID | 0x679 / 缺失 | 0x7E8 | 调查表 / 硬编码默认 |
| CAN FD | Y/N / 未指定 | Classic CAN | 调查表 / 默认 |
| 仲裁域波特率 | 500000 / 未指定 | 500000 | 调查表 / 硬编码默认 |
| 采样点 | 0.8 / 未指定 | 0.8 | 调查表 / 硬编码默认 |
| 是否需要 $27 | Y/N | Y/N | 调查表 |
| 安全日志输出 | 路径 / 无 | 路径 / 无 | 调查表 |

**用户明确确认后**，生成命令必须带上 `--confirmed` 标志。未确认**禁止**跳过此步骤直接生成。

### 3. 生成脚本

```bash
source ~/.uds_env
PYTHON="$UDS_PYTHON"
SKILL_DIR="$UDS_SKILL_DIR"
UDS_WORK="${UDS_WORK:-$HOME/.uds_workspace}"

"$PYTHON" "$SKILL_DIR/scripts/uds_test_generator.py" \
  --input "$UDS_WORK/uds_parsed.json" \
  --output "$UDS_WORK/uds_test.py" \
  --confirmed

"$PYTHON" -m py_compile "$UDS_WORK/uds_test.py"
```

### 4. 初始化 CAN

默认 CAN FD 模式（向下兼容 Classic CAN，无需区分）：

```bash
source ~/.uds_env
"$PYTHON" "$UDS_SKILL_DIR/scripts/can_init.py"
```

如 ECU 明确只支持 Classic CAN，加 `--classic` 参数。

### 5. 验证连接

```bash
source ~/.uds_env
PYTHON="$UDS_PYTHON"
UDS_WORK="${UDS_WORK:-$HOME/.uds_workspace}"

"$PYTHON" -c "import can, importlib.metadata as md; print('python-can', md.version('python-can'), '@', can.__file__)"
"$PYTHON" "$UDS_WORK/uds_test.py" --test-connection
```

### 6. 执行测试

```bash
source ~/.uds_env
PYTHON="$UDS_PYTHON"
UDS_WORK="${UDS_WORK:-$HOME/.uds_workspace}"

"$PYTHON" "$UDS_WORK/uds_test.py" \
  --report "$UDS_WORK/uds_report.md" \
  --can-log "$UDS_WORK/can_trace_$(date +%Y%m%d_%H%M%S).asc"
```

## 何时使用 pipeline

只有在用户明确要求“直接生成并执行，不需要中间确认”时，才使用：

```bash
source ~/.uds_env
PYTHON="$UDS_PYTHON"
SKILL_DIR="$UDS_SKILL_DIR"
UDS_WORK="${UDS_WORK:-$HOME/.uds_workspace}"

"$PYTHON" "$SKILL_DIR/scripts/uds_pcan_runner.py" pipeline \
  --input "<调查表文件路径>" \
  --output-dir "$UDS_WORK/pipeline_output"
```

默认不要直接走 pipeline。默认流程始终是：解析 → 用户确认（阻断点） → 生成（带 --confirmed） → 验证 → 执行。**跳过确认直接生成是不可接受的。**

## 详细资料

以下内容不要继续堆在当前技能主流程里，统一去 `README.md`：

- WSL2 USB 透传
- 原生 Linux 驱动安装
- SecurityAccess Linux 替代方案
- NRC 0x78 / P2 / P2* 说明
- 调查表属性默认值表
- 深度 CAN 故障排查
- Agent 在确认阶段如发现 DLL 路径以 `.dll` 结尾且运行在 Linux，**必须主动告知用户此限制**
