# URSim 仿真器测试指南

**创建日期:** 2026-04-02  
**测试类型:** URSim 仿真器真机测试

---

## 📋 测试前检查清单

### 1. 安装 ur_rtde

```bash
pip install ur_rtde
```

**验证安装:**
```bash
pip show ur_rtde
```

应该显示：
```
Name: ur_rtde
Version: 1.4.x
...
```

---

### 2. 启动 URSim 仿真器

**方式 1: Windows 桌面应用**

1. 打开 URSim 仿真器
2. 选择机器人型号：UR5e
3. 点击 "Start Robot"
4. 确认 IP 地址：192.168.56.101

**方式 2: Docker**

```bash
docker pull universalrobots/ursim_e-series
docker run --rm -it \
  -p 8080:8080 \
  -p 30001-30004:30001-30004 \
  universalrobots/ursim_e-series
```

**访问 Web 界面:**
```
http://localhost:8080
```

---

### 3. 网络配置检查

**Windows 虚拟网卡:**

1. 打开"网络连接"
2. 找到"VirtualBox Host-Only Network"
3. 确保已启用
4. IP 配置：
   - IP 地址：192.168.56.1
   - 子网掩码：255.255.255.0

**Ping 测试:**
```bash
ping 192.168.56.101
```

**期望结果:**
```
来自 192.168.56.101 的回复：字节=32 时间<1ms TTL=64
```

---

### 4. 端口检查

**检查端口占用:**
```bash
netstat -ano | findstr 30001
```

**期望结果:**
```
TCP    0.0.0.0:30001    0.0.0.0:0    LISTENING    12345
```

---

## 🧪 运行测试

### 测试脚本

| 脚本 | 用途 | 命令 |
|------|------|------|
| `test_ur_real.py` | URSim 真机测试 | `python test_ur_real.py` |
| `run_all_tests.py --simulate` | 模拟模式测试 | `python run_all_tests.py --simulate` |
| `test_ur_sim.py` | 基础连接测试 | `python test_ur_sim.py` |

### 运行真机测试

```bash
cd C:\Users\JMO\.openclaw\workspace\skills\ur-robot
python test_ur_real.py
```

---

## 📊 测试项目

### 1. 连接测试
- [ ] 连接 URSim 仿真器
- [ ] 建立 RTDE 通信

### 2. 状态读取
- [ ] 读取关节角度
- [ ] 读取 TCP 位姿

### 3. 运动控制
- [ ] 关节空间运动 (移动到零位)
- [ ] 笛卡尔空间运动 (Z 轴 +50mm)

### 4. IO 控制
- [ ] 数字输出 DO0 控制

---

## ✅ 预期结果

```
总测试数：6
通过：6 [OK]
失败：0 [FAIL]
通过率：100%
```

**详细结果:**
- ✅ connection - 连接成功
- ✅ get_joints - 读取关节角度
- ✅ get_pose - 读取 TCP 位姿
- ✅ move_joint - 关节运动成功
- ✅ move_line - 笛卡尔运动成功
- ✅ io_control - IO 控制成功

---

## ⚠️ 常见问题

### 问题 1: 连接被拒绝

**错误:** `ConnectionRefusedError`

**原因:**
1. URSim 未启动
2. IP 地址不正确
3. 防火墙阻止

**解决:**
1. 启动 URSim 仿真器
2. 检查 IP: 192.168.56.101
3. 关闭防火墙或添加例外

---

### 问题 2: 无法 Ping 通

**错误:** `请求超时`

**原因:**
1. 虚拟网卡未启用
2. IP 配置错误

**解决:**
1. 启用 VirtualBox Host-Only Network
2. 配置 IP: 192.168.56.1

---

### 问题 3: ur_rtde 未安装

**错误:** `ModuleNotFoundError: No module named 'ur_rtde'`

**解决:**
```bash
pip install ur_rtde
```

---

### 问题 4: 运动超时

**原因:**
1. 目标位置超出工作空间
2. 速度设置过快

**解决:**
1. 检查目标位置是否可达
2. 降低速度参数
3. 增加等待时间

---

## 📝 测试报告

测试完成后，报告会保存到：
```
test_results_real.json
```

**报告内容:**
```json
{
  "test_date": "2026-04-02 10:30:00",
  "robot_model": "UR5e",
  "ursim_version": "e-Series 5.13+",
  "test_mode": "real_simulation",
  "results": {
    "connection": true,
    "get_joints": true,
    "get_pose": true,
    "move_joint": true,
    "move_line": true,
    "io_control": true
  },
  "summary": {
    "total": 6,
    "passed": 6,
    "failed": 0,
    "pass_rate": "100.0%"
  }
}
```

---

## 🎯 下一步

测试通过后：

1. ✅ 更新 TEST_REPORT.md
2. ✅ 打包技能包
3. ✅ 发布到 ClawHub

---

## 📞 技术支持

- **UR 官方文档:** https://www.universal-robots.com/download/
- **RTDE 手册:** https://www.universal-robots.com/articles/ur/real-time-data-exchange-rtde-guide/
- **ur_rtde GitHub:** https://github.com/UniversalRobots/Universal_Robots_RTDE_Python_Client

---

**准备好后运行：** `python test_ur_real.py` 🚀
