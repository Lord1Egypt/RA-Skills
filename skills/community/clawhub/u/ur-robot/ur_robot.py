# UR Robot Python 控制库

**功能：** 封装 URScript 命令发送和 RTDE 数据读取

---

## 🚀 快速使用

```python
from ur_robot import URRobot

# 连接机器人
robot = URRobot(host="localhost", port=30003)

# 关节运动
robot.movej([0, -1.57, 1.57, -1.57, -1.57, 0])

# 直线运动
robot.movel([0.3, 0.3, 0.5, 3.14, 0, 0])

# 速度控制
robot.speedj([0.5, 0, 0, 0, 0, 0], t=3)

# 读取状态
pose = robot.get_tcp_pose()
print("TCP 位姿:", pose)

# 断开
robot.disconnect()
```

---

## 📚 API 参考

### URRobot 类

#### 初始化

```python
robot = URRobot(host="localhost", port=30003, rtde_port=30004)
```

#### 运动控制

```python
# 关节运动
robot.movej(q, a=0.5, v=0.5)

# 直线运动
robot.movel(pose, a=0.2, v=0.2)

# 圆弧运动
robot.movec(pose_via, pose_to, a=0.2, v=0.2)

# 相对运动
robot.move_relative(dx=0.2, dy=0, dz=0)

# 速度控制
robot.speedj(qd, a=0.5, t=3)
robot.speedl(xd, a=0.2, t=2)

# 停止
robot.stopj(a=0.5)
robot.stopl(a=0.5)
```

#### IO 控制

```python
# 数字输出
robot.set_digital_out(pin=0, state=True)
robot.set_tool_digital_out(pin=0, state=True)

# 读取输入
state = robot.get_digital_in(pin=0)
```

#### 力控

```python
# 启动力控
robot.force_mode(selection=[0,0,1,0,0,0], wrench=[0,0,-5,0,0,0])

# 退出力控
robot.end_force_mode()
```

#### 状态读取

```python
# TCP 位姿
pose = robot.get_tcp_pose()

# 关节角度
angles = robot.get_joint_angles()

# 关节速度
speeds = robot.get_joint_speeds()

# 控制器版本
version = robot.get_controller_version()
```

---

## 📝 完整示例

### 示例 1: 基础运动

```python
from ur_robot import URRobot

robot = URRobot()

# Home 位置
robot.movej([0, -1.57, 1.57, -1.57, -1.57, 0])

# 工作位置
robot.movel([0.3, 0.3, 0.5, 3.14, 0, 0])

# 返回 Home
robot.movej([0, -1.57, 1.57, -1.57, -1.57, 0])

robot.disconnect()
```

### 示例 2: 连续轨迹

```python
from ur_robot import URRobot

robot = URRobot()

# 画正方形
positions = [
    [0.3, 0.3, 0.5],
    [0.4, 0.3, 0.5],
    [0.4, 0.4, 0.5],
    [0.3, 0.4, 0.5],
    [0.3, 0.3, 0.5],
]

for pos in positions:
    robot.movel(pos + [3.14, 0, 0])

robot.disconnect()
```

### 示例 3: IO 控制

```python
from ur_robot import URRobot
import time

robot = URRobot()

# 打开夹爪
robot.set_tool_digital_out(0, True)
time.sleep(1)

# 移动到位置
robot.movel([0.3, 0, 0.2, 3.14, 0, 0])

# 关闭夹爪
robot.set_tool_digital_out(0, False)
time.sleep(1)

# 抬起
robot.movel([0.3, 0, 0.4, 3.14, 0, 0])

robot.disconnect()
```

### 示例 4: 状态监控

```python
from ur_robot import URRobot
import time

robot = URRobot()

# 实时监控 10 秒
for i in range(10):
    pose = robot.get_tcp_pose()
    joints = robot.get_joint_angles()
    
    print(f"[{i}] TCP: {pose}")
    print(f"[{i}] Joints: {joints}")
    
    time.sleep(1)

robot.disconnect()
```

---

## 🔧 开发说明

### 依赖

```python
import socket
import time
import rtde.rtde as rtde
```

### 通信方式

1. **URScript 命令** - 端口 30003 (Secondary Socket)
2. **RTDE 数据** - 端口 30004 (RTDE 接口)

### 命令格式

```python
# URScript 命令必须以换行符结尾
command = "movej([0, 0, 0, 0, 0, 0], a=0.5, v=0.5)\n"
sock.sendall(command.encode('utf-8'))
```

---

*Created: 2026-04-02*
