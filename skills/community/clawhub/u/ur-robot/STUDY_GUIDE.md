# UR 机器人学习大纲

**版本:** 1.0.0  
**创建时间:** 2026-04-01

---

## 📚 模块 1: UR 机器人基础

### 1.1 UR 机器人型号
- UR3e (3kg) - 小型精密
- UR5e (5kg) - 通用型 ⭐
- UR10e (10kg) - 中型
- UR16e (16kg) - 重载

### 1.2 技术规格 (UR5e)
- **工作半径:** 850mm
- **重复定位精度:** ±0.03mm
- **最大关节速度:** 180°/s
- **负载:** 5kg
- **重量:** 18.4kg

### 1.3 安全特性
- 力限制
- 速度限制
- 工作空间限制
- 急停按钮

---

## 📚 模块 2: URSim 仿真

### 2.1 安装配置
- Windows 安装
- Docker 安装
- 网络配置

### 2.2 界面操作
- 示教器界面
- 程序编辑
- 手动控制

### 2.3 仿真测试
- 连接测试
- 运动测试
- IO 测试

---

## 📚 模块 3: Python SDK

### 3.1 ur_rtde 库
```python
from ur_rtde import RTDEReceiveInterface, RTDESendInterface

rtde_r = RTDEReceiveInterface("192.168.56.101")
rtde_s = RTDESendInterface("192.168.56.101")
```

### 3.2 数据读取
```python
# 关节角度
joints = rtde_r.getActualQ()

# TCP 位姿
pose = rtde_r.getActualTCPPose()

# 速度
speed = rtde_r.getSpeedFraction()

# IO 状态
digital_io = rtde_r.getActualDigitalInputBits()
```

### 3.3 运动控制
```python
# 关节运动
rtde_s.sendJointPosition([0, 0, 0, 0, 0, 0], speed=0.5)

# 笛卡尔运动
rtde_s.sendPose([0.3, 0.3, 0.5, 3.14, 0, 0], speed=0.5)

# 速度控制
rtde_s.sendJointSpeeds([0.1, 0, 0, 0, 0, 0])
```

---

## 📚 模块 4: 运动学

### 4.1 UR 机器人 DH 参数
```
a = [0, -0.425, -0.392, 0, 0, 0]
d = [0.163, 0, 0, 0.134, 0.085, 0.082]
alpha = [π/2, 0, 0, π/2, -π/2, 0]
```

### 4.2 正运动学
```python
def forward_kinematics(q):
    # 根据关节角度计算 TCP 位姿
    T = T1(q[0]) * T2(q[1]) * ... * T6(q[5])
    return T
```

### 4.3 逆运动学
```python
def inverse_kinematics(T):
    # 根据 TCP 位姿计算关节角度
    # 最多 8 组解
    solutions = []
    return solutions
```

---

## 📚 模块 5: 应用案例

### 5.1 拾取放置
```python
def pick_and_place(pick_pose, place_pose):
    # 移动到拾取点上方
    robot.move(pick_pose[0], pick_pose[1], pick_pose[2]+0.1)
    # 下降
    robot.move(pick_pose)
    # 抓取
    robot.gripper.close()
    # 上升
    robot.move(pick_pose[0], pick_pose[1], pick_pose[2]+0.1)
    # 移动到放置点
    robot.move(place_pose)
    # 释放
    robot.gripper.open()
```

### 5.2 码垛应用
```python
def palletizing(rows, cols, layers):
    for layer in range(layers):
        for row in range(rows):
            for col in range(cols):
                x = col * 100
                y = row * 100
                z = layer * 50
                robot.pick_and_place(start_pose, [x, y, z])
```

### 5.3 轨迹绘制
```python
def draw_circle(center, radius):
    points = []
    for angle in range(0, 360, 10):
        x = center[0] + radius * cos(angle)
        y = center[1] + radius * sin(angle)
        points.append([x, y, center[2]])
    
    for point in points:
        robot.move_linear(point)
```

---

## 📚 模块 6: 力控功能

### 6.1 力控模式
```python
# 启用力控
rtde_s.sendForceMode(
    task_frame=[0,0,0,0,0,0],
    selection_vector=[0,0,1,0,0,0],  # Z 轴
    wrench=[0,0,-10,0,0,0],  # 10N 向下力
    bounds=[0.1,0.1,0.1,0.1,0.1,0.1],
    gain=0.5
)
```

### 6.2 应用场景
- 打磨抛光
- 零件装配
- 表面检测

---

## ✅ 实践项目

### 项目 1: 基础运动
- [ ] 关节空间运动
- [ ] 笛卡尔空间运动
- [ ] 6 轴限位测试

### 项目 2: 码垛工作站
- [ ] 创建码垛模式
- [ ] 实现抓取逻辑
- [ ] 完成 3x3x2 码垛

### 项目 3: 轨迹绘制
- [ ] 绘制正方形
- [ ] 绘制圆形
- [ ] 绘制三角形

### 项目 4: 力控应用
- [ ] 力控打磨
- [ ] 力控装配
- [ ] 拖动示教

---

## 📖 参考资源

- **UR 官方:** https://www.universal-robots.com/
- **UR Academy:** https://academy.universal-robots.com/
- **ur_rtde GitHub:** https://github.com/UniversalRobots/Universal_Robots_RTDE_Python_Client

---

**下一步:** 安装 URSim → 运行测试脚本 → 完成实践项目
