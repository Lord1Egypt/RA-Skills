# URSim 安装指南 (Windows)

## 📥 下载 URSim

### 官方下载
**URL:** https://www.universal-robots.com/download/

**步骤:**
1. 访问下载页面
2. 选择 "URSim" 标签
3. 选择 "e-Series" (推荐) 或 "CB3"
4. 下载 Windows 版本

### 推荐版本
- **URSim e-Series 5.13+** (支持 UR3e/UR5e/UR10e/UR16e)
- **URSim CB3 3.15+** (支持 UR3/UR5/UR10)

---

## 🖥️ Windows 安装

### 方法 1: 直接安装 (推荐)

1. **下载 URSim for Windows**
   - 文件名：`URSim_WIN_5.x.x.exe`
   - 大小：约 2GB

2. **运行安装程序**
   ```
   双击 URSim_WIN_5.x.x.exe
   按照安装向导完成安装
   ```

3. **启动 URSim**
   ```
   桌面快捷方式 → URSim
   选择机器人型号：UR5e (推荐)
   点击 "Start Robot"
   ```

4. **确认 IP 地址**
   ```
   默认 IP: 192.168.56.101
   端口：30001-30004
   ```

### 方法 2: Docker (高级用户)

```bash
# 拉取镜像
docker pull universalrobots/ursim_e-series

# 运行容器
docker run --rm -it \
  -p 8080:8080 \
  -p 30001-30004:30001-30004 \
  universalrobots/ursim_e-series
```

**访问:**
- Web 界面：http://localhost:8080
- RTDE 端口：30001-30004

---

## 🔧 网络配置

### Windows 网络设置

1. **启用虚拟网卡**
   ```
   控制面板 → 网络连接
   找到 "VirtualBox Host-Only Network"
   确保已启用
   ```

2. **配置 IP**
   ```
   IP 地址：192.168.56.1
   子网掩码：255.255.255.0
   ```

3. **关闭防火墙 (测试用)**
   ```
   控制面板 → Windows Defender 防火墙
   关闭防火墙 (或添加例外)
   ```

---

## ✅ 验证安装

### 1. Ping 测试
```bash
ping 192.168.56.101
```

**期望结果:**
```
来自 192.168.56.101 的回复：字节=32 时间<1ms TTL=64
```

### 2. Python 连接测试
```bash
cd skills/ur-robot
python test_ur_sim.py
```

**期望结果:**
```
[OK] 连接成功
关节角度：[0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
```

---

## 🐛 常见问题

### 问题 1: 无法连接
**错误:** `Connection refused`

**解决:**
1. 确认 URSim 已启动
2. 检查 IP 地址
3. 关闭防火墙

### 问题 2: 虚拟网卡不存在
**解决:**
```
安装 VirtualBox
https://www.virtualbox.org/
```

### 问题 3: 端口被占用
**解决:**
```bash
# 查看端口占用
netstat -ano | findstr 30001

# 关闭占用程序
taskkill /PID <PID> /F
```

---

## 📚 参考资料

- **UR 官方文档:** https://www.universal-robots.com/how-tos-and-faqs/
- **RTDE 手册:** https://www.universal-robots.com/articles/ur/real-time-data-exchange-rtde-guide/
- **ur_rtde 文档:** https://github.com/UniversalRobots/Universal_Robots_RTDE_Python_Client

---

**安装完成后运行:** `python test_ur_sim.py`

**下一步:** 关节控制测试 → `python test_joint_control.py`
