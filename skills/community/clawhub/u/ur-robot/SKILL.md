# UR Robot - Universal Robots 控制技能

**技能版本:** v1.0.0  
**适用机器人:** Universal Robots (UR3/UR5/UR10/UR10e, CB3/e-Series)  
**仿真器:** URSim Docker  
**通信协议:** RTDE + URScript (Secondary Socket)

---

## 💡 Windows 用户须知

**为符合 ClawHub 平台要求，已移除 2 个 PowerShell 脚本 (`.ps1`)**

| 移除的脚本 | 替代方案 | 位置 |
|-----------|----------|------|
| `fix-and-test.ps1` | Python 测试脚本 | `test_*.py` |
| `setup-docker-d-drive.ps1` | 手动配置 Docker | 见 `WINDOWS_SCRIPTS_NOTE.md` |

**核心功能不受影响** - 所有 Python 脚本和文档保留 ✅

详细说明：`WINDOWS_SCRIPTS_NOTE.md`

---

## ⚠️ 重要安全声明

### 🧪 测试状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **URSim 仿真** | ✅ 已验证 | 所有功能在 URSim e-Series 中测试通过 |
| **真机验证** | ❌ **未验证** | **尚未在真实机器人上测试** |

### ⚠️ 真机使用警告

**本技能包仅在 URSim 仿真器中完成测试，未在真实机器人上验证！**

**在真机使用前必须：**

1. ✅ **重新验证所有命令** - 仿真与真机可能存在差异
2. ✅ **低速测试** - 首次运行使用最低速度 (v=0.1)
3. ✅ **安全检查** - 确认急停按钮、工作范围、碰撞检测
4. ✅ **专业人员监督** - 必须由持证机器人操作员监督
5. ✅ **风险评估** - 进行全面的风险评估和安全分析

**因直接使用本技能包于真机导致的任何损失，作者不承担责任！**

---

## 📋 功能概览

| 功能类别 | 支持命令 | 状态 |
|----------|----------|------|
| **关节运动** | `movej()` | ✅ |
| **直线运动** | `movel()` | ✅ |
| **圆弧运动** | `movec()` | ✅ |
| **速度控制** | `speedj()`, `speedl()` | ✅ |
| **IO 控制** | `set_digital_out()` | ✅ |
| **状态读取** | RTDE 数据订阅 | ✅ |
| **力控模式** | `force_mode()` | ✅ |

---

## 🔄 仿真 → 真机迁移指南

### 配置修改

```python
# 仿真配置 (当前默认)
ROBOT_HOST = "localhost"

# 真机配置 (需要修改)
ROBOT_HOST = "192.168.1.100"  # 机器人实际 IP
```

### 安全参数调整

| 参数 | 仿真值 | 真机建议值 |
|------|--------|------------|
| 速度 (v) | 0.5 m/s | 0.1-0.3 m/s |
| 加速度 (a) | 0.2 m/s² | 0.1-0.2 m/s² |
| 工作范围检查 | 不需要 | 必须 |
| 急停确认 | 不需要 | 必须 |

### 真机使用流程

```bash
# 1. 网络连接确认
ping 192.168.1.100

# 2. 修改配置文件
# 编辑 robot_config.json 设置真机 IP

# 3. 低速测试
python skills/ur-robot/examples/real_robot_test.py

# 4. 确认安全后正式运行
```

### 推荐添加的安全检查

```python
# 真机专用安全检查脚本
def safety_check_before_move():
    """真机运动前安全检查"""
    # 1. 确认机器人状态
    # 2. 确认工作范围
    # 3. 确认急停按钮可用
    # 4. 确认人员安全距离
    # 5. 人工确认签字
    pass
```

---

## 🚀 快速开始

### 1. 启动 URSim 仿真器

```bash
docker run -d --name ursim \
  -p 6080:6080 -p 5900:5900 \
  -p 30001:30001 -p 30002:30002 \
  -p 30003:30003 -p 30004:30004 \
  universalrobots/ursim_e-series
```

### 2. 访问 URSim Web 界面

```
http://localhost:6080/vnc.html
```

### 3. 初始化机器人

1. 点击 **ON** 按钮（启动电源）
2. 点击 **START** 按钮（启动程序）
3. 点击 **Program** → **Empty Program**
4. 点击 **Play** (▶) 按钮

### 4. 运行测试脚本

```bash
# 关节运动测试
python skills/ur-robot/test_motion_simple.py

# RTDE 数据读取
python skills/ur-robot/test_rtde_official.py

# 连续运动测试
python skills/ur-robot/test_continuous_motion.py
```

---

## 📚 URScript 命令参考

### 运动控制

#### `movej()` - 关节空间运动

```python
# 语法
movej(q, a=1.4, v=1.05, t=0, r=0)

# 参数
# q      - 关节角度 [J1, J2, J3, J4, J5, J6] (弧度)
# a      - 关节加速度 (rad/s²)
# v      - 关节速度 (rad/s)
# t      - 时间 (s)，为 0 表示不限制
# r      -  blends 半径 (m)

# 示例：移动到 Home 位置
movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)

# 示例：J1 旋转 30 度
movej([0.52, 0, 0, 0, 0, 0], a=0.3, v=0.3)
```

#### `movel()` - 笛卡尔空间直线运动

```python
# 语法
movel(pose, a=1.2, v=0.25, t=0, r=0)

# 参数
# pose   - TCP 位姿 [x, y, z, rx, ry, rz] (米和弧度)
# a      - 笛卡尔加速度 (m/s²)
# v      - 笛卡尔速度 (m/s)

# 示例：直线移动到目标位置
movel([0.3, 0.3, 0.5, 3.14, 0, 0], a=0.2, v=0.2)

# 示例：相对当前位置移动 (+200mm X 轴)
movel(pose_trans(get_actual_tcp_pose(), p[0.2, 0, 0, 0, 0, 0]), a=0.2, v=0.2)
```

#### `movec()` - 圆弧运动

```python
# 语法
movec(pose_via, pose_to, a=1.2, v=0.25, t=0, r=0)

# 参数
# pose_via - 圆弧经过的中间点
# pose_to  - 圆弧终点

# 示例：画圆弧
movec(p[0.5, 0, 0.3, 0, 3.14, 0], p[0.6, 0, 0.2, 0, 3.14, 0], a=0.2, v=0.2)
```

#### `speedj()` - 关节速度控制

```python
# 语法
speedj(qd, a=1.4, t=0)

# 参数
# qd     - 关节速度 [J1, J2, J3, J4, J5, J6] (rad/s)
# a      - 关节加速度 (rad/s²)
# t      - 持续时间 (s)，为 0 表示持续运行

# 示例：J1 轴以 0.5 rad/s 旋转 3 秒
speedj([0.5, 0, 0, 0, 0, 0], a=0.5, t=3)

# 示例：停止关节运动
stopj(a=0.5)
```

#### `speedl()` - 笛卡尔速度控制

```python
# 语法
speedl(xd, a=1.2, t=0)

# 参数
# xd     - TCP 速度 [xd, yd, zd, rxd, ryd, rzd] (m/s, rad/s)

# 示例：TCP 沿 X 轴以 0.1 m/s 移动 2 秒
speedl([0.1, 0, 0, 0, 0, 0], a=0.2, t=2)
```

---

### IO 控制

#### `set_digital_out()` - 设置数字输出

```python
# 语法
set_digital_out(pin, state)

# 参数
# pin    - 引脚编号 (0-7 基础 IO, 8-15 工具 IO)
# state  - True (高电平) / False (低电平)

# 示例：设置数字输出 0 为高电平
set_digital_out(0, True)

# 示例：关闭数字输出 0
set_digital_out(0, False)

# 示例：控制工具端数字输出
set_tool_digital_out(0, True)
```

#### `get_digital_in()` - 读取数字输入

```python
# 语法
state = get_digital_in(pin)

# 示例：读取数字输入 0
input_state = get_digital_in(0)
```

---

### 力控模式

#### `force_mode()` - 力控制

```python
# 语法
force_mode(task_frame, selection_vector, wrench, type, limits)

# 参数
# task_frame       - 任务坐标系 [x, y, z, rx, ry, rz]
# selection_vector - 选择向量 [x, y, z, rx, ry, rz] (1=力控，0=位置控)
# wrench          - 目标力/力矩 [Fx, Fy, Fz, Mx, My, Mz] (N, Nm)
# type            - 控制类型 (2=恒力模式)
# limits          - 速度/加速度限制

# 示例：Z 轴向下 5N 恒力
force_mode(p[0,0,0,0,0,0], [0,0,1,0,0,0], [0,0,-5,0,0,0], 2, [0.1,0.1,0.1,0.1,0.1,0.1])

# 退出力控模式
end_force_mode()
```

---

### 状态读取

#### 通过 RTDE 读取

```python
import rtde.rtde as rtde

# 连接
con = rtde.RTDE("localhost", 30004)
con.connect()

# 设置输出
con.send_output_setup(["actual_q", "actual_TCP_pose"], frequency=10)

# 开始同步
con.send_start()

# 读取数据
data = con.receive()
print("关节角度:", data.actual_q)
print("TCP 位姿:", data.actual_TCP_pose)

# 暂停/断开
con.send_pause()
con.disconnect()
```

#### 通过 URScript 读取

```python
# 获取当前 TCP 位姿
pose = get_actual_tcp_pose()

# 获取当前关节角度
angles = get_actual_q()

# 获取关节速度
speeds = get_speed_q()

# 获取关节电流
currents = get_current()

# 获取 TCP 受力
forces = get_tcp_force()
```

---

## 🛠️ Python 工具函数

### 发送 URScript 命令

```python
import socket

def send_urscript(host="localhost", port=30003, command=""):
    """发送 URScript 命令到机器人"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect((host, port))
        full_command = command + "\n"
        sock.sendall(full_command.encode('utf-8'))
        time.sleep(0.1)
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        return True, response
    except Exception as e:
        return False, str(e)
    finally:
        sock.close()

# 使用示例
success, response = send_urscript(command="movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)")
```

### 关节运动封装

```python
def move_to_home():
    """移动到 Home 位置"""
    send_urscript("movej([0, -1.57, 1.57, -1.57, -1.57, 0], a=0.5, v=0.5)")

def move_joints(j1, j2, j3, j4, j5, j6, a=0.5, v=0.5):
    """关节空间运动"""
    cmd = "movej([{}, {}, {}, {}, {}, {}], a={}, v={})".format(
        j1, j2, j3, j4, j5, j6, a, v
    )
    send_urscript(cmd)

def move_linear(x, y, z, rx, ry, rz, a=0.2, v=0.2):
    """笛卡尔空间直线运动"""
    cmd = "movel([{}, {}, {}, {}, {}, {}], a={}, v={})".format(
        x, y, z, rx, ry, rz, a, v
    )
    send_urscript(cmd)
```

---

## 📊 端口说明

| 端口 | 协议 | 用途 |
|------|------|------|
| 6080 | HTTP | Web VNC 界面 |
| 5900 | VNC | 远程桌面 |
| 30001 | RTDE | 主客户端接口 |
| 30002 | RTDE | 实时客户端接口 |
| 30003 | TCP | Secondary 客户端 (URScript) |
| 30004 | RTDE | RTDE 数据接口 |

---

## ⚠️ 注意事项

### 安全

1. **测试前确保在仿真环境** - 真机操作需要额外的安全措施
2. **运动范围限制** - 确保目标位置在机器人工作范围内
3. **速度设置** - 测试时使用较低速度 (v=0.2-0.5)
4. **急停准备** - 随时准备点击 URSim 的停止按钮

### URSim 使用

1. **程序模式** - 必须点击 Play 按钮启动程序
2. **外部命令** - 通过 30003 端口发送 URScript
3. **程序停止** - 每次命令执行后程序可能停止，需要重新启动
4. **持续运行程序** - 创建 `endless + wait(0.1)` 循环程序可避免频繁重启

### 常见问题

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 机器人不动 | 程序未运行 | 点击 Play 按钮 |
| 连接失败 | 端口未映射 | 检查 Docker 端口配置 |
| 命令不执行 | 保护状态 | 重置安全状态 |
| 运动异常 | 奇异点 | 避开奇异点位置 |

---

## 📁 文件结构

```
skills/ur-robot/
├── SKILL.md                      # 技能文档 (本文件)
├── README.md                     # 快速入门
├── URSIM_TEST_GUIDE.md           # URSim 测试指南
├── URSCRIPT_FEATURES.md          # URScript 功能清单
├── test_motion_simple.py         # 简单运动测试
├── test_rtde_official.py         # RTDE 数据读取测试
├── test_continuous_motion.py     # 连续运动测试
├── test_ur_real.py               # 真机测试 (待开发)
├── ur_robot.py                   # Python 封装库
└── examples/
    ├── basic_move.py             # 基础运动示例
    └── io_control.py             # IO 控制示例
```

---

## 🔗 相关资源

- **UR 官方文档:** https://www.universal-robots.com/articles/ur/programming/
- **URScript 手册:** https://sdurobotics.gitlab.io/ur_rtde/
- **RTDE 库:** https://github.com/UniversalRobots/RTDE_Python_Client_Library
- **URSim 下载:** https://www.universal-robots.com/download/

---

## 📝 更新日志

### v1.0.0 (2026-04-02)

- ✅ URSim Docker 配置完成
- ✅ rtde 模块安装 (UR 官方库)
- ✅ URScript 命令发送 (端口 30003)
- ✅ 关节运动 `movej()` 测试
- ✅ 直线运动 `movel()` 测试
- ✅ 圆弧运动 `movec()` 测试
- ✅ 速度控制 `speedj()` 测试
- ✅ IO 控制 `set_digital_out()` 测试
- ✅ RTDE 状态读取测试
- ✅ 力控模式 `force_mode()` 测试

---

*Created: 2026-04-02*  
*Author: 小橙 (Little Orange) 🍊*
