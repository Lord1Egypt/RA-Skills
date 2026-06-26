# URSim 仿真器快速测试指南

**目标:** 用 URSim 仿真器测试 UR Robot 技能包

---

## 📋 步骤总览

```
1. 安装 ur_rtde (1 分钟)
2. 启动 URSim 仿真器 (Docker 5 分钟 / Windows 应用 10 分钟)
3. 运行测试脚本 (2 分钟)
4. 查看测试结果
```

---

## 🔧 步骤 1: 安装 ur_rtde

**命令:**
```bash
pip install ur_rtde
```

**验证:**
```bash
pip show ur_rtde
```

---

## 🐳 步骤 2A: 用 Docker 启动 URSim (推荐)

**如果你已经安装了 Docker Desktop:**

### 2.1 拉取镜像
```bash
docker pull universalrobots/ursim_e-series
```

### 2.2 启动仿真器
```bash
docker run --rm -it ^
  -p 8080:8080 ^
  -p 30001-30004:30001-30004 ^
  --name ursim ^
  universalrobots/ursim_e-series
```

### 2.3 等待启动
- 首次启动约 2-3 分钟
- 看到 "Robot is running" 表示启动成功

### 2.4 验证
**浏览器访问:** http://localhost:8080

**或命令行:**
```bash
ping 192.168.56.101
```

---

## 🖥️ 步骤 2B: 用 Windows 应用启动 URSim

### 2.1 下载
**官方下载:** https://www.universal-robots.com/download/

选择：
- Product: URSim
- Series: e-Series
- Version: 5.13+ (最新版)

### 2.2 安装
1. 运行下载的安装程序
2. 按向导完成安装
3. 桌面会创建 URSim 快捷方式

### 2.3 启动
1. 打开 URSim
2. 选择机器人：**UR5e**
3. 点击 **"Start Robot"**
4. 等待 30-60 秒

### 2.4 验证
**浏览器访问:** http://192.168.56.101:8080

**或命令行:**
```bash
ping 192.168.56.101
```

---

## ▶️ 步骤 3: 运行测试脚本

**确认 URSim 已启动后:**

```bash
cd C:\Users\JMO\.openclaw\workspace\skills\ur-robot
python test_ur_real.py
```

---

## 📊 步骤 4: 查看测试结果

**预期输出:**
```
======================================================================
UR Robot - URSim 仿真器真机测试
======================================================================
目标 IP: 192.168.56.101
目标端口：30001
======================================================================

[OK] ur_rtde 已安装

[1/6] 连接 URSim 仿真器...
[OK] 连接成功！

[2/6] 读取当前关节角度...
关节角度 (rad): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
关节角度 (deg): ['0.0', '0.0', '0.0', '0.0', '0.0', '0.0']

[3/6] 读取当前 TCP 位姿...
TCP 位姿：[0.3, 0.3, 0.5, 3.14, 0, 0]
...

[OK] 关节运动成功！
[OK] 笛卡尔运动成功！
[OK] IO 控制成功！

======================================================================
测试报告
======================================================================

总测试数：6
通过：6 [OK]
失败：0 [FAIL]
通过率：100.0%

详细结果:
  [OK] connection: PASS
  [OK] get_joints: PASS
  [OK] get_pose: PASS
  [OK] move_joint: PASS
  [OK] move_line: PASS
  [OK] io_control: PASS

[OK] 测试报告已保存：test_results_real.json
```

---

## ⚠️ 常见问题

### 问题 1: Docker 未安装

**错误:** `'docker' 不是内部或外部命令`

**解决:**
1. 安装 Docker Desktop: https://www.docker.com/products/docker-desktop/
2. 或使用 Windows 应用方式

### 问题 2: 连接被拒绝

**错误:** `ConnectionRefusedError`

**原因:** URSim 未完全启动

**解决:**
1. 等待 1-2 分钟
2. 检查 Docker 容器是否运行：`docker ps`
3. 查看 URSim 日志

### 问题 3: 端口被占用

**错误:** `Address already in use`

**解决:**
```bash
# 停止旧容器
docker stop ursim
docker rm ursim

# 重新启动
docker run --rm -it -p 8080:8080 -p 30001-30004:30001-30004 universalrobots/ursim_e-series
```

---

## 🎯 快速命令参考

```bash
# 安装依赖
pip install ur_rtde

# Docker 方式
docker pull universalrobots/ursim_e-series
docker run --rm -it -p 8080:8080 -p 30001-30004:30001-30004 universalrobots/ursim_e-series

# 运行测试
cd C:\Users\JMO\.openclaw\workspace\skills\ur-robot
python test_ur_real.py
```

---

## 📞 需要帮助？

**文档:**
- `URSIM_TEST_GUIDE.md` - 完整测试指南
- `README.md` - 使用指南
- `INSTALL_URSIM.md` - URSim 安装指南

**外部资源:**
- UR 官方：https://www.universal-robots.com/download/
- RTDE 文档：https://www.universal-robots.com/articles/ur/real-time-data-exchange-rtde-guide/

---

**准备好后，按顺序执行上面的步骤！** 🚀
