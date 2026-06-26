# UDS Diagnostic Test Skill

UDS（Unified Diagnostic Services）诊断自动化测试工具，基于 SocketCAN + python-can，支持解析诊断调查表、生成测试脚本、通过 CAN 硬件执行测试并输出报告。

## 功能

- 解析诊断调查表（Excel/CSV/JSON），自动提取 DID、DTC、IOControl、Routine、CAN 配置
- 生成 100% 覆盖率的 UDS 测试脚本（会话验证/安全访问/边界值/NRC 验证）
- 通过 SocketCAN 执行测试，支持 Classic CAN 和 CAN FD
- 输出 Markdown 测试报告 + CAN 通信日志（.asc 格式，兼容 CANoe/CANalyzer）
- 支持 $27 SecurityAccess 自动解锁（Vector SeedKey DLL）

## 硬件要求

- **CAN 适配器**（任一即可）：
  - PEAK PCAN-USB / PCAN-USB FD（推荐）
  - Kvaser USBcan
  - Vector VN16xx
  - 其他 SocketCAN 兼容设备（gs_usb、mttcan 等）
- **Linux 环境**：原生 Linux 或 WSL2（内核需编译 SocketCAN + 对应驱动模块）
- **CAN 总线**：连接目标 ECU

## 安装

### 1. 安装 CAN 驱动

#### 1.1 Linux 内核依赖

至少要保证以下 SocketCAN 相关内核模块可用：

```bash
sudo modprobe can
sudo modprobe can_raw
sudo modprobe peak_usb

# 检查模块是否已加载
lsmod | grep -E "can|can_raw|peak_usb"
```

#### 1.2 原生 Linux：编译安装 PEAK 驱动

> **仅适用于原生 Linux**。WSL2 不支持编译安装第三方内核模块，请跳转到 1.3 节。

先安装构建依赖：

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

编译并安装 peak-linux-driver：

```bash
git clone https://github.com/linux-can/peak-linux-driver.git
cd peak-linux-driver
make
sudo make install
sudo modprobe peak_usb
```

安装完成后验证：

```bash
lsusb | grep -i peak
ip link show
lsmod | grep peak_usb
```

**其他设备：** 参考 [linux-can 文档](https://github.com/linux-can) 安装对应驱动。

**设置开机自动加载（可选）：**
```bash
echo -e "can\ncan_raw\npeak_usb" | sudo tee /etc/modules-load.d/can.conf
```

#### 1.3 WSL2：使用内核自带 peak_usb 模块

> WSL2 **不支持**编译安装第三方内核模块（如 peak-linux-driver）。
> 必须依赖 WSL 内核自带的 `peak_usb` 模块（WSL 内核 5.10.60.1+ 已内置）。

**前提：更新 WSL 内核到最新版本**

```bash
# Windows PowerShell
wsl --update
wsl --shutdown
# 重新打开 WSL 后检查内核版本
uname -r
```

**通过 usbipd 将 PCAN-USB 附加到 WSL**

```bash
# Windows PowerShell（管理员）— 首次需 bind
usbipd list
usbipd bind --busid <BUSID>

# Windows PowerShell（普通即可，保持一个 WSL shell 已打开）
usbipd attach --wsl --busid <BUSID>
```

**WSL 内加载模块并验证**

```bash
sudo modprobe can can_raw peak_usb
lsusb | grep -i peak
ip link show
```

如果 `modprobe peak_usb` 报错 "not found"，说明 WSL 内核版本过旧，请先执行 `wsl --update`。

#### 1.4 WSL/USB 重连说明

以下场景通常需要重新附加 USB 设备：

- 重启 WSL（如执行 `wsl --shutdown`）
- 物理拔插 PCAN-USB 设备
- Windows 更新或 usbipd 服务重启

推荐重连步骤：

```bash
# Windows PowerShell
usbipd list
usbipd attach --wsl --busid <BUSID>

# WSL 内再次确认
lsusb
ip link show
```

如果 `attach` 失败，可先执行：

```bash
# Windows PowerShell
usbipd detach --busid <BUSID>
usbipd attach --wsl --busid <BUSID>
```

### 2. 配置 sudo 免密（推荐，避免每次输入密码）

```bash
echo "$(whoami) ALL=(root) NOPASSWD: /sbin/ip link set can* type can *, /sbin/ip link set can* up, /sbin/ip link set can* down, /sbin/modprobe can*, /usr/bin/fuser -k /sys/class/net/can*" | sudo tee /etc/sudoers.d/can-setup
sudo chmod 440 /etc/sudoers.d/can-setup
```

### 3. 安装 Python 依赖

前提：当前目录必须是包含 `SKILL.md` 和 `scripts/` 的 `uds-diagnostic-test` 目录。

```bash
# 进入 skill 根目录后执行一键环境准备
bash ./scripts/setup_env.sh

# 读取目标机器上的持久化变量
source ~/.uds_env

# 预检：解释器路径 + Python 依赖层 + SocketCAN Python 后端层
test -x "$UDS_PYTHON" || { echo "[ERROR] UDS_PYTHON 无效: $UDS_PYTHON"; exit 1; }
$UDS_PYTHON -c "import can, openpyxl, can.interfaces.socketcan, importlib.metadata as md; print('Python deps OK, python-can', md.version('python-can'), 'module', can.__file__)"
```

`setup_env.sh` 会自动在目标机器上解析 skill 根目录、选择或创建 Python 环境，并把 `UDS_PYTHON`、`UDS_SKILL_DIR`、`UDS_WORK` 写入 `~/.uds_env`。这比手工 `export UDS_PYTHON=...` 更适合跨机器使用。

对 agent 而言，环境修复的默认动作也应该只有这一条：重跑 `bash ./scripts/setup_env.sh`。除非用户明确要求，否则不要把 `pip uninstall/install` 当作常规恢复流程。

**重要：不要执行 `pip install can`。**
Python 模块名虽然叫 `can`，但正确的 pip 包名是 `python-can`。如果装成了错误的 `can-0.0.0`，会出现 `can.interfaces.socketcan` 缺失、`__version__` 异常、或只看到 `pcan` 后端等问题。

如需手工修复：

```bash
source ~/.uds_env
"$UDS_PYTHON" -m pip uninstall -y can python-can
"$UDS_PYTHON" -m pip install --no-cache-dir -U python-can openpyxl
```

## 快速开始

### 1. 验证 CAN 环境

```bash
source ~/.uds_env

# 确认 CAN 设备已识别
lsusb | grep -i peak

# 确认内核模块已加载
lsmod | grep -E "can|can_raw|peak_usb"

# 初始化 CAN 接口
bash scripts/can_init.sh

# 确认接口已启用
ip -details link show can0
```

### 2. 解析诊断调查表

```bash
source ~/.uds_env
"$UDS_PYTHON" "$UDS_SKILL_DIR/scripts/uds_survey_parser.py" --input survey.xlsx --output "$UDS_WORK/parsed.json"
```

### 3. 生成测试脚本

```bash
source ~/.uds_env
"$UDS_PYTHON" "$UDS_SKILL_DIR/scripts/uds_test_generator.py" --input "$UDS_WORK/parsed.json" --output "$UDS_WORK/test_uds.py"
```

### 4. 验证连通性（可选）

```bash
source ~/.uds_env
"$UDS_PYTHON" "$UDS_WORK/test_uds.py" --test-connection
```

### 5. 执行测试

```bash
source ~/.uds_env
bash "$UDS_SKILL_DIR/scripts/can_init.sh"          # 初始化 CAN
"$UDS_PYTHON" "$UDS_WORK/test_uds.py" --report "$UDS_WORK/report.md"
```

### 6. 一步到位（Pipeline 模式）

```bash
source ~/.uds_env
"$UDS_PYTHON" "$UDS_SKILL_DIR/scripts/uds_pcan_runner.py" pipeline \
  --input survey.xlsx \
  --output-dir ./output
```

## `can_init.sh` 参考

| 命令 | 说明 |
|------|------|
| `bash scripts/can_init.sh` | Classic CAN, 500kbps, 80% SP |
| `bash scripts/can_init.sh --fd` | CAN FD, 仲裁500k/数据2M, 双80% SP |
| `bash scripts/can_init.sh --fd --bitrate 500000 --dbitrate 2000000 --sp 0.800 --dsp 0.800` | CAN FD 自定义参数 |
| `bash scripts/can_init.sh --channel can1` | 指定 CAN 通道 |
| `bash scripts/can_init.sh --force` | 强制释放占用后初始化 |
| `bash scripts/can_init.sh --help` | 查看完整帮助 |

### CAN FD 默认参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 仲裁段波特率 | 500000 (500kbps) | `--bitrate` |
| 数据段波特率 | 2000000 (2Mbps) | `--dbitrate` |
| 仲裁段采样点 | 0.800 (80%) | `--sp` |
| 数据段采样点 | 0.800 (80%) | `--dsp` |

## 文件结构

```
uds-diagnostic-test/
├── SKILL.md                      # AI Agent 技能定义
├── README.md                     # 本文件
├── requirements.txt              # Python 依赖
├── scripts/
│   ├── uds_survey_parser.py      # 诊断调查表解析器
│   ├── uds_test_generator.py     # 测试脚本生成器
│   ├── uds_pcan_runner.py        # 测试执行器（含 Pipeline 模式）
│   └── can_init.sh               # CAN 接口初始化脚本
└── references/
    └── uds_nrc_reference.md      # UDS NRC 参考
```

## UDS 服务覆盖

| 服务 | SID | 说明 |
|------|-----|------|
| DiagnosticSessionControl | 0x10 | 会话切换 |
| ECUReset | 0x11 | ECU 复位 |
| ClearDiagnosticInformation | 0x14 | 清除 DTC |
| ReadDTCInformation | 0x19 | 读取 DTC |
| ReadDataByIdentifier | 0x22 | 读取 DID |
| SecurityAccess | 0x27 | 安全访问解锁 |
| WriteDataByIdentifier | 0x2E | 写入 DID |
| IOControlByIdentifier | 0x2F | IO 控制 |
| RoutineControl | 0x31 | 例程控制 |
| TesterPresent | 0x3E | 保活 |
| ControlDTCSetting | 0x85 | DTC 设置控制 |

## 测试报告示例

```markdown
# UDS 诊断测试报告
**日期**: 2026-05-05 19:50:43
**ECU**: Example_ECU
**CAN 通道**: can0
**CAN ID**: TX=0x7E0, RX=0x7E8

## 测试汇总
| 指标 | 数量 |
|------|------|
| 总测试用例 | 480 |
| 通过 (PASS) | 452 |
| 失败 (FAIL) | 3 |
| 跳过 (SKIP) | 25 |
| 通过率 | 94.2% |
```

## 故障排查

| 问题 | 检查方法 |
|------|----------|
| CAN 设备未识别 | `lsusb \| grep -i peak` |
| 驱动未加载 | `lsmod \| grep -E "peak_usb\|can_raw"` |
| WSL 没有附加 USB 设备 | Windows 下执行 `usbipd list` / `usbipd attach --wsl --busid <BUSID>` |
| WSL 重启后设备丢失 | 重新执行 `usbipd attach --wsl --busid <BUSID>` |
| 接口不存在 | `ip link show can0` |
| 接口被占用 | `bash scripts/can_init.sh --force` |
| `~/.uds_env` 不存在 | 先进入 skill 根目录，再执行 `bash ./scripts/setup_env.sh` |
| UDS_PYTHON / UDS_SKILL_DIR 无效 | 先进入 skill 根目录，再执行 `bash ./scripts/setup_env.sh` |
| `./scripts/setup_env.sh` 不存在 / `SKILL.md` 缺失 | 技能目录不完整，不要手工补文件；重新获取完整的 `uds-diagnostic-test` 目录 |
| pip 只能装出 `can-0.0.0` 或 `python-can 1.5.x` | 不要循环重装；这是包源/镜像问题，改查 pip 源而不是继续排查硬件 |
| 装成了错误的 `can-0.0.0` | 先重跑 `bash ./scripts/setup_env.sh`；如果脚本仍然报告 `can-0.0.0` 或 `python-can 1.5.x`，停止重试并报告包源异常 |
| Python 缺少依赖 | 先进入 skill 根目录，再执行 `bash ./scripts/setup_env.sh`；不要默认切到手工 `pip install` |
| 权限不足 | 确认 sudoers 配置或手动 `sudo` |
| ECU 无应答 | 检查 CAN ID (TX/RX)、波特率、ECU 供电 |

## 参考链接

- PEAK Linux 驱动仓库: https://github.com/linux-can/peak-linux-driver
- Linux CAN 主页: https://github.com/linux-can
- Microsoft WSL USB 连接指南: https://learn.microsoft.com/windows/wsl/connect-usb
- usbipd-win WSL 支持说明: https://github.com/dorssel/usbipd-win/wiki/WSL-support
- usbipd-win 故障排查: https://github.com/dorssel/usbipd-win/wiki/Troubleshooting

## 联系方式
邮箱：1430336713@qq.com
微信/电话：17612130154

## License

MIT
