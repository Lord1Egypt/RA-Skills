# TM Robot Skill - 达明机器人控制技能

> OMRON TM5 协作机器人 Python 控制技能，支持 techmanpy SDK、自定义 SVR 解析器

## 🧪 测试环境报告

### 已验证配置

**测试日期**: 2026-03-31  
**测试人员**: RobotQu

| 项目 | 值 |
|------|-----|
| **机器人型号** | OMRON TM5M-700 |
| **臂展** | 700mm |
| **负载** | 5kg |
| **TMflow 版本** | 1.80.5300 |
| **控制器型号** | TM5M-700 |
| **控制器序列号** | BC1934034 |
| **机器人 IP** | 192.168.1.13 |
| **网络** | 有线以太网（千兆）|
| **操作系统** | Windows 11 |
| **Python 版本** | 3.12 |
| **techmanpy 版本** | 1.80+ |

### 测试结果

| 测试项 | 结果 | 备注 |
|--------|------|------|
| SVR 连接 | ✅ 通过 | 自定义解析器 |
| SCT 连接 | ✅ 通过 | techmanpy |
| 读取关节角度 | ✅ 通过 | Joint_Angle |
| 读取笛卡尔位姿 | ✅ 通过 | Coord_Robot_Flange |
| 读取错误码 | ✅ 通过 | Error_Code |
| 读取 IO 状态 | ✅ 通过 | Ctrl_DO/DI |
| 关节运动 | ✅ 通过 | move_joint |
| 回零 | ✅ 通过 | move_joints_zero |
| 数字输出 | ✅ 通过 | set_digital_output |

### 兼容性说明

**理论上兼容的型号**（协议相同，待用户验证）：

| 型号 | 臂展 | 负载 | 状态 |
|------|------|------|------|
| TM5-450 | 450mm | 3kg | ⚠️ 待验证 |
| TM5-700 | 700mm | 5kg | ✅ 已验证 |
| TM5-900 | 900mm | 7kg | ⚠️ 待验证 |
| TM12 | 1300mm | 12kg | ⚠️ 待验证 |
| TM14 | 1400mm | 14kg | ⚠️ 待验证 |
| TM7 系列 | - | - | ❌ 不兼容（新协议）|

> **注意**: TM7 系列使用新协议，需要单独开发。

### 反馈模板

如果你在其他机器人型号上测试成功，请提交反馈：

```markdown
### 测试反馈

**机器人型号**: TM5-900
**TMflow 版本**: 1.80.xxxx
**测试日期**: 2026-xx-xx
**测试结果**: ✅ 通过 / ❌ 失败

**备注**: （可选）
```

---

## 功能特性

| 功能 | 支持状态 | 说明 |
|------|:--------:|------|
| SCT 连接（实时控制） | ✅ | 运动控制、I/O |
| SVR 连接（状态读取） | ✅ | 自定义解析器 |
| 关节运动 (PTP) | ✅ | 所有关节同时运动 |
| 直线运动 (LIN) | ✅ | TCP 直线插补 |
| I/O 控制 | ✅ | 数字输入输出 |
| 碰撞检测 | ✅ | 触发后需手动复位 |
| ROS1 驱动 | ✅ | 官方驱动 |
| ROS2 驱动 | ✅ | 官方驱动 |

## 环境要求

- Python 3.8+
- techmanpy >= 1.80
- TMflow >= 1.80
- 机器人 IP 可达

## 快速开始

### 1. 安装依赖

```bash
pip install techmanpy
```

### 2. 配置机器人 IP

编辑 `config.py`：

```python
ROBOT_IP = "192.168.1.13"  # 改成你的机器人 IP
```

查看 IP：TMflow → 设置 → 网络

### 3. ⚠️ 机器人端必须配置

**在使用本技能之前，必须在机器人 TMflow 界面完成以下配置：**

#### 3.1 启用 Ethernet Slave（SVR 状态读取，Port 5891）

TMflow → Robot Setting → Ethernet Slave → 开启 → 数据表

**必须添加的变量：**
- `Joint_Angle`（关节角度）
- `Coord_Robot_Flange`（笛卡尔位姿）
- `Error_Code`（错误码）
- `Robot_Error`（错误标志）
- `Project_Run`（项目运行状态）

#### 3.2 运行 Listen Node 项目（SCT 运动控制，Port 5890）

TMflow → 新建项目 → 添加 Listen Node → 运行项目

> **详细配置图解见 `docs/` 目录**

### 4. 连接测试

```bash
# 检测端口是否开放
python scripts/test_ports.py

# 测试 SVR 读取
python tm_robot.py
```

## 使用方法

### 作为 Python 模块导入

```python
from tm_robot import TMRobot
import asyncio

async def demo():
    async with TMRobot("192.168.1.13") as robot:
        # 读取状态
        state = await robot.get_state()
        print(state)
        
        # 读取关节角度
        joints = await robot.get_joints()
        print(f"Joints: {joints}")
        
        # 回零
        await robot.move_joints_zero()

asyncio.run(demo())
```

### 命令行工具

```bash
# 读取状态
python tm_robot.py state

# 读取关节角度
python tm_robot.py joints

# 回零
python tm_robot.py zero

# 停止运动
python tm_robot.py stop
```

## 文件结构

```
skills/tm-robot/
├── SKILL.md              # 技能文档
├── README.md             # 本文件（详细指南）
├── tm_robot.py           # 核心 API
├── config.py             # 配置
├── examples/             # 示例代码
│   └── complete_demo.py  # 完整示例
├── scripts/              # 测试脚本
│   ├── test_ports.py     # 端口检测
│   └── test_connection.py # 连接测试
└── docs/                 # 详细文档
    ├── error_codes.md    # 错误码
    └── ...
```

## 技术细节

### SVR 协议解析

本技能使用**自定义 SVR 解析器**直接解析 TMflow 的原始 socket 数据。

**协议格式：**
```
Header: $TMSVR,3279,1,1,\n (ASCII)
Body: [变量名\x00][类型码][\x00][数据...][标记]
```

**类型码：**
- `0x01`: bool (1 byte)
- `0x04`: int32 (4 bytes, little-endian)
- `0x18`: 6 floats (24 bytes)
- `0x24`: 9 floats (36 bytes)
- `0x0C`: 3 floats (12 bytes)

### 为什么需要自定义解析器？

TMflow 的 SVR 协议是 **ASCII 变量名 + 二进制数据** 的混合格式，不是纯 Binary。

techmanpy 的 `svr_read()` 解析器假设是纯 Binary，导致解析失败。

我们的自定义解析器直接解析原始数据，100% 兼容。

## 故障排除

### SVR 连接失败
1. 检查 Ethernet Slave 是否开启
2. 确认数据表中有变量
3. 运行 `python scripts/test_ports.py`

### SCT 连接失败
1. 确认 Listen Node 项目正在运行
2. 检查机器人 IP 是否正确
3. 确认防火墙未阻止 5890 端口

### 变量读取失败
1. 确认变量已在 TMflow 数据表中添加
2. 检查变量名拼写（区分大小写）
3. 运行 `python tm_robot.py` 测试

## 参考资料

- [TMflow 官方文档](https://www.tm-robot.com/)
- [techmanpy GitHub](https://github.com/TechmanRobotInc/techmanpy)
- [TM Export 工具](https://github.com/TechmanRobotInc/TM_Export)

## 许可证

MIT License

## 联系方式

- **作者**: RobotQu
- **网站**: https://robotqu.com
- **邮箱**: [联系表单](https://robotqu.com/contact)
